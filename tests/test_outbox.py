from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

from nft_mint_radar.domain.enums import (
    DeliveryState,
    NotificationAction,
    NotificationClass,
    NotificationSeverity,
)
from nft_mint_radar.domain.models import Notification
from nft_mint_radar.notify.outbox import (
    InMemoryNotificationRepository,
    OutboxProcessor,
    SendOutcome,
    SendResult,
)

NOW = datetime(2026, 8, 30, 0, 0, tzinfo=UTC)


def test_f32_ambiguous_delivery_is_not_resent_from_null_sent_at() -> None:
    notification = _notification(
        delivery_state=DeliveryState.CLAIMED,
        claimed_until=NOW + timedelta(minutes=5),
    )
    repository = InMemoryNotificationRepository((notification,))
    transport = FakeTransport((SendResult.ambiguous(),))
    processor = OutboxProcessor(repository=repository, transport=transport)

    delivered = processor.deliver_claimed(
        notification.id,
        chat_id="chat-1",
        text="message",
        now=NOW,
    )

    assert delivered.delivery_state == DeliveryState.AMBIGUOUS
    assert delivered.attempt_count == 1
    assert delivered.next_attempt_at is not None
    assert delivered.provider_message_id is None
    assert delivered.sent_at is None
    assert len(transport.messages) == 1

    reclaimed = processor.claim_one(delivered.next_attempt_at + timedelta(seconds=1))

    assert reclaimed is None
    assert len(transport.messages) == 1
    assert repository.get(notification.id).delivery_state == DeliveryState.AMBIGUOUS


def test_sent_requires_provider_message_id() -> None:
    notification = _notification(
        delivery_state=DeliveryState.CLAIMED,
        claimed_until=NOW + timedelta(minutes=5),
    )
    repository = InMemoryNotificationRepository((notification,))
    transport = FakeTransport((SendResult(outcome=SendOutcome.SENT),))
    processor = OutboxProcessor(repository=repository, transport=transport)

    delivered = processor.deliver_claimed(
        notification.id,
        chat_id="chat-1",
        text="message",
        now=NOW,
    )

    assert delivered.delivery_state == DeliveryState.FAILED
    assert delivered.provider_message_id is None
    assert delivered.sent_at is None
    assert delivered.last_error == "sent_without_provider_message_id"


def test_crashed_claim_expires_and_can_be_reclaimed() -> None:
    notification = _notification(
        delivery_state=DeliveryState.CLAIMED,
        claimed_until=NOW + timedelta(minutes=5),
    )
    repository = InMemoryNotificationRepository((notification,))
    processor = OutboxProcessor(
        repository=repository,
        transport=FakeTransport((SendResult.sent("msg-1"),)),
    )

    assert processor.claim_one(NOW + timedelta(minutes=1)) is None

    reclaimed = processor.claim_one(NOW + timedelta(minutes=6))

    assert reclaimed is not None
    assert reclaimed.id == notification.id
    assert reclaimed.delivery_state == DeliveryState.CLAIMED
    assert reclaimed.claimed_until == NOW + timedelta(minutes=11)


def test_failed_retries_stop_at_bounded_maximum_and_abandon() -> None:
    notification = _notification(delivery_state=DeliveryState.PENDING)
    repository = InMemoryNotificationRepository((notification,))
    processor = OutboxProcessor(
        repository=repository,
        transport=FakeTransport(
            (
                SendResult.failed("first"),
                SendResult.failed("second"),
            )
        ),
        max_attempts=2,
        base_backoff=timedelta(seconds=1),
    )

    first_claim = processor.claim_one(NOW)
    assert first_claim is not None
    first_result = processor.deliver_claimed(
        first_claim.id,
        chat_id="chat-1",
        text="message",
        now=NOW,
    )
    assert first_result.delivery_state == DeliveryState.FAILED

    second_claim = processor.claim_one(NOW + timedelta(seconds=2))
    assert second_claim is not None
    second_result = processor.deliver_claimed(
        second_claim.id,
        chat_id="chat-1",
        text="message",
        now=NOW + timedelta(seconds=2),
    )

    assert second_result.delivery_state == DeliveryState.ABANDONED
    assert second_result.attempt_count == 2
    assert processor.claim_one(NOW + timedelta(minutes=5)) is None


class FakeTransport:
    def __init__(self, results: tuple[SendResult, ...]) -> None:
        self._results = list(results)
        self.messages: list[tuple[str, str]] = []

    def send(self, chat_id: str, text: str) -> SendResult:
        self.messages.append((chat_id, text))
        return self._results.pop(0)


def _notification(
    *,
    delivery_state: DeliveryState,
    claimed_until: datetime | None = None,
) -> Notification:
    return Notification(
        id="notification-1",
        fingerprint="fingerprint-1",
        project_id="project-1",
        campaign_id="campaign-1",
        stage_id="stage-1",
        opportunity_id="opportunity-1",
        notification_class=NotificationClass.DEADLINE,
        severity=NotificationSeverity.ACTION,
        action=NotificationAction.APPLY_WL,
        rendered_payload_hash="hash-1",
        delivery_state=delivery_state,
        attempt_count=0,
        claimed_until=claimed_until,
    )
