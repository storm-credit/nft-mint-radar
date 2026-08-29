"""Deterministic notification outbox with protocol-based transport."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Protocol

from nft_mint_radar.domain.enums import DeliveryState
from nft_mint_radar.domain.models import Notification


class SendOutcome(str, Enum):
    SENT = "SENT"
    FAILED = "FAILED"
    AMBIGUOUS = "AMBIGUOUS"


@dataclass(frozen=True, kw_only=True)
class SendResult:
    outcome: SendOutcome
    provider_message_id: str | None = None
    error: str | None = None

    @classmethod
    def sent(cls, provider_message_id: str) -> "SendResult":
        if not provider_message_id:
            raise ValueError("provider_message_id is required for SENT")
        return cls(outcome=SendOutcome.SENT, provider_message_id=provider_message_id)

    @classmethod
    def failed(cls, error: str) -> "SendResult":
        return cls(outcome=SendOutcome.FAILED, error=error)

    @classmethod
    def ambiguous(cls, error: str = "possible_delivery_timeout") -> "SendResult":
        return cls(outcome=SendOutcome.AMBIGUOUS, error=error)


class Transport(Protocol):
    def send(self, chat_id: str, text: str) -> SendResult:
        """Send one message and return provider evidence or an explicit outcome."""


class NotificationRepository(Protocol):
    def add(self, notification: Notification) -> bool:
        """Store a notification, returning False when its fingerprint already exists."""

    def get(self, notification_id: str) -> Notification | None:
        """Return one notification by id."""

    def save(self, notification: Notification) -> None:
        """Persist a replacement notification."""

    def list(self) -> tuple[Notification, ...]:
        """Return all notifications."""


class InMemoryNotificationRepository:
    """Small in-memory repository for tests and dry runs."""

    def __init__(self, notifications: tuple[Notification, ...] = ()) -> None:
        self._rows: dict[str, Notification] = {}
        self._fingerprints: set[str] = set()
        for notification in notifications:
            self.add(notification)

    def add(self, notification: Notification) -> bool:
        if notification.fingerprint in self._fingerprints:
            return False
        self._rows[notification.id] = notification
        self._fingerprints.add(notification.fingerprint)
        return True

    def get(self, notification_id: str) -> Notification | None:
        return self._rows.get(notification_id)

    def save(self, notification: Notification) -> None:
        existing = self._rows.get(notification.id)
        if existing is None:
            if notification.fingerprint in self._fingerprints:
                raise ValueError("duplicate fingerprint")
            self._fingerprints.add(notification.fingerprint)
        elif existing.fingerprint != notification.fingerprint:
            if notification.fingerprint in self._fingerprints:
                raise ValueError("duplicate fingerprint")
            self._fingerprints.remove(existing.fingerprint)
            self._fingerprints.add(notification.fingerprint)
        self._rows[notification.id] = notification

    def list(self) -> tuple[Notification, ...]:
        return tuple(self._rows.values())


@dataclass(frozen=True, kw_only=True)
class OutboxProcessor:
    repository: NotificationRepository
    transport: Transport
    max_attempts: int = 3
    claim_ttl: timedelta = timedelta(minutes=5)
    base_backoff: timedelta = timedelta(minutes=1)

    def claim_one(self, now: datetime) -> Notification | None:
        _validate_aware(now, "now")
        current_time = now.astimezone(UTC)

        for notification in sorted(self.repository.list(), key=lambda row: row.id):
            if self._is_duplicate_after_delivery(notification):
                abandoned = replace(
                    notification,
                    delivery_state=DeliveryState.ABANDONED,
                    last_error="duplicate_fingerprint_already_delivered",
                    claimed_until=None,
                )
                self.repository.save(abandoned)
                continue

            if notification.delivery_state == DeliveryState.CLAIMED:
                if (
                    notification.claimed_until is not None
                    and notification.claimed_until <= current_time
                ):
                    reclaimed = replace(
                        notification,
                        delivery_state=DeliveryState.CLAIMED,
                        claimed_until=current_time + self.claim_ttl,
                    )
                    self.repository.save(reclaimed)
                    return reclaimed
                continue

            if notification.delivery_state not in {
                DeliveryState.PENDING,
                DeliveryState.FAILED,
            }:
                continue

            if (
                notification.next_attempt_at is not None
                and notification.next_attempt_at > current_time
            ):
                continue

            claimed = replace(
                notification,
                delivery_state=DeliveryState.CLAIMED,
                claimed_until=current_time + self.claim_ttl,
                last_error=None,
            )
            self.repository.save(claimed)
            return claimed

        return None

    def deliver_claimed(
        self,
        notification_id: str,
        *,
        chat_id: str,
        text: str,
        now: datetime,
    ) -> Notification:
        _validate_aware(now, "now")
        current_time = now.astimezone(UTC)
        notification = self.repository.get(notification_id)
        if notification is None:
            raise KeyError(notification_id)
        if notification.delivery_state != DeliveryState.CLAIMED:
            return notification

        result = self.transport.send(chat_id, text)
        attempt_count = notification.attempt_count + 1

        if result.outcome == SendOutcome.SENT:
            if not result.provider_message_id:
                updated = self._failed_or_abandoned(
                    notification,
                    attempt_count=attempt_count,
                    now=current_time,
                    error="sent_without_provider_message_id",
                )
            else:
                updated = replace(
                    notification,
                    delivery_state=DeliveryState.SENT,
                    attempt_count=attempt_count,
                    provider_message_id=result.provider_message_id,
                    last_error=None,
                    sent_at=current_time,
                    next_attempt_at=None,
                    claimed_until=None,
                )
        elif result.outcome == SendOutcome.AMBIGUOUS:
            updated = replace(
                notification,
                delivery_state=DeliveryState.AMBIGUOUS,
                attempt_count=attempt_count,
                provider_message_id=None,
                last_error=result.error or "ambiguous_possible_delivery",
                next_attempt_at=current_time + self._backoff(attempt_count),
                claimed_until=None,
            )
        else:
            updated = self._failed_or_abandoned(
                notification,
                attempt_count=attempt_count,
                now=current_time,
                error=result.error or "send_failed",
            )

        self.repository.save(updated)
        return updated

    def _failed_or_abandoned(
        self,
        notification: Notification,
        *,
        attempt_count: int,
        now: datetime,
        error: str,
    ) -> Notification:
        if attempt_count >= self.max_attempts:
            return replace(
                notification,
                delivery_state=DeliveryState.ABANDONED,
                attempt_count=attempt_count,
                last_error=error,
                next_attempt_at=None,
                claimed_until=None,
            )
        return replace(
            notification,
            delivery_state=DeliveryState.FAILED,
            attempt_count=attempt_count,
            last_error=error,
            next_attempt_at=now + self._backoff(attempt_count),
            claimed_until=None,
        )

    def _backoff(self, attempt_count: int) -> timedelta:
        return self.base_backoff * (2 ** max(attempt_count - 1, 0))

    def _is_duplicate_after_delivery(self, notification: Notification) -> bool:
        for other in self.repository.list():
            if other.id == notification.id:
                continue
            if other.fingerprint != notification.fingerprint:
                continue
            if other.delivery_state in {DeliveryState.SENT, DeliveryState.AMBIGUOUS}:
                return True
        return False


def _validate_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
