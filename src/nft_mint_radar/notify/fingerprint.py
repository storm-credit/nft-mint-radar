"""Deterministic notification fingerprinting and re-alert decisions."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

from nft_mint_radar.domain.models import Notification

DEFAULT_BUCKET_GRID = timedelta(minutes=15)
MATERIAL_VERSION_START = 1
MATERIAL_DEADLINE_NEAR_THRESHOLD = timedelta(minutes=15)
MATERIAL_DEADLINE_FAR_THRESHOLD = timedelta(hours=2)
MATERIAL_DEADLINE_NEAR_WINDOW = timedelta(days=1)


@dataclass(frozen=True, kw_only=True)
class FingerprintCandidate:
    project_id: str
    campaign_id: str | None
    stage_id: str | None
    opportunity_id: str | None
    notification_class: Any
    normalized_action: Any
    canonical_claim_time_utc: datetime | None
    material_version: int = MATERIAL_VERSION_START


@dataclass(frozen=True, kw_only=True)
class MaterialSnapshot:
    state: Any = None
    deadline: datetime | None = None
    price: Any = None
    supply: int | None = None
    max_per_wallet: int | None = None
    action_url: str | None = None
    contract_address: str | None = None
    cta_safety_state: Any = None
    risk_score: int | float | None = None
    allocation_type: Any = None
    required_quest: Any = None


@dataclass(frozen=True, kw_only=True)
class RealertDecision:
    should_alert: bool
    material_version: int
    fingerprint: str
    reason: str
    material_change_keys: tuple[str, ...]


def build_fingerprint(
    candidate: FingerprintCandidate,
    *,
    grid: timedelta = DEFAULT_BUCKET_GRID,
) -> str:
    """Build the documented fingerprint from canonical claim time."""

    return " | ".join(
        (
            _part(candidate.project_id),
            _part(candidate.campaign_id),
            _part(candidate.stage_id),
            _part(candidate.opportunity_id),
            _part(candidate.notification_class),
            _part(candidate.normalized_action),
            canonical_time_bucket(candidate.canonical_claim_time_utc, grid=grid),
            str(candidate.material_version),
        )
    )


def canonical_time_bucket(
    canonical_claim_time_utc: datetime | None,
    *,
    grid: timedelta = DEFAULT_BUCKET_GRID,
) -> str:
    """Floor a canonical UTC claim time to a fixed grid."""

    if canonical_claim_time_utc is None:
        return "unresolved"
    if (
        canonical_claim_time_utc.tzinfo is None
        or canonical_claim_time_utc.utcoffset() is None
    ):
        return "unresolved"
    if grid.total_seconds() <= 0:
        raise ValueError("grid must be positive")

    claim_time = canonical_claim_time_utc.astimezone(UTC)
    seconds = int(claim_time.timestamp())
    grid_seconds = int(grid.total_seconds())
    bucket_seconds = seconds - (seconds % grid_seconds)
    bucket = datetime.fromtimestamp(bucket_seconds, tz=UTC)
    return bucket.strftime("%Y-%m-%dT%H:%M:%SZ")


def decide_realert(
    previous_notification: Notification | None,
    new_candidate: FingerprintCandidate,
    *,
    previous_material: MaterialSnapshot | None = None,
    new_material: MaterialSnapshot | None = None,
    reference_time_utc: datetime | None = None,
    grid: timedelta = DEFAULT_BUCKET_GRID,
) -> RealertDecision:
    """Decide whether a candidate should create a notification or be suppressed."""

    if previous_notification is None:
        fingerprint = build_fingerprint(new_candidate, grid=grid)
        return RealertDecision(
            should_alert=True,
            material_version=new_candidate.material_version,
            fingerprint=fingerprint,
            reason="new_notification",
            material_change_keys=(),
        )

    previous_version = _fingerprint_material_version(previous_notification.fingerprint)
    base_candidate = replace(new_candidate, material_version=previous_version)
    same_identity_fingerprint = build_fingerprint(base_candidate, grid=grid)

    if previous_notification.fingerprint == same_identity_fingerprint:
        changes = _material_change_keys(
            previous_material,
            new_material,
            reference_time_utc=reference_time_utc,
        )
        if not changes:
            return RealertDecision(
                should_alert=False,
                material_version=previous_version,
                fingerprint=previous_notification.fingerprint,
                reason="no_material_change",
                material_change_keys=(),
            )

        material_version = previous_version + 1
        fingerprint = build_fingerprint(
            replace(new_candidate, material_version=material_version),
            grid=grid,
        )
        return RealertDecision(
            should_alert=True,
            material_version=material_version,
            fingerprint=fingerprint,
            reason="material_change",
            material_change_keys=changes,
        )

    fingerprint = build_fingerprint(new_candidate, grid=grid)
    return RealertDecision(
        should_alert=True,
        material_version=new_candidate.material_version,
        fingerprint=fingerprint,
        reason="fingerprint_identity_changed",
        material_change_keys=(),
    )


def _material_change_keys(
    previous: MaterialSnapshot | None,
    new: MaterialSnapshot | None,
    *,
    reference_time_utc: datetime | None,
) -> tuple[str, ...]:
    if previous is None or new is None:
        return ()

    changes: list[str] = []
    if previous.state != new.state:
        changes.append("state")
    if _deadline_materially_moved(previous.deadline, new.deadline, reference_time_utc):
        changes.append("deadline")
    if previous.price != new.price:
        changes.append("price")
    if previous.supply != new.supply:
        changes.append("supply")
    if previous.max_per_wallet != new.max_per_wallet:
        changes.append("max_per_wallet")
    if previous.action_url != new.action_url:
        changes.append("action_url")
    if previous.contract_address != new.contract_address:
        changes.append("contract")
    if previous.cta_safety_state != new.cta_safety_state:
        changes.append("cta_safety")
    if _risk_materially_changed(previous.risk_score, new.risk_score):
        changes.append("risk")
    if previous.allocation_type != new.allocation_type:
        changes.append("allocation")
    if previous.required_quest != new.required_quest:
        changes.append("required_quest")
    return tuple(changes)


def _deadline_materially_moved(
    previous: datetime | None,
    new: datetime | None,
    reference_time_utc: datetime | None,
) -> bool:
    if previous == new:
        return False
    if previous is None or new is None:
        return True
    if _datetime_unusable(previous) or _datetime_unusable(new):
        return True

    previous_utc = previous.astimezone(UTC)
    new_utc = new.astimezone(UTC)
    delta = abs(new_utc - previous_utc)
    threshold = MATERIAL_DEADLINE_FAR_THRESHOLD
    if reference_time_utc is not None and not _datetime_unusable(reference_time_utc):
        now = reference_time_utc.astimezone(UTC)
        if min(previous_utc, new_utc) - now <= MATERIAL_DEADLINE_NEAR_WINDOW:
            threshold = MATERIAL_DEADLINE_NEAR_THRESHOLD
    return delta >= threshold


def _risk_materially_changed(
    previous: int | float | None,
    new: int | float | None,
) -> bool:
    if previous == new:
        return False
    if previous is None or new is None:
        return True
    if abs(new - previous) >= 15:
        return True
    return _risk_bucket(previous) != _risk_bucket(new)


def _risk_bucket(score: int | float) -> str:
    if score >= 70:
        return "hard"
    if score >= 50:
        return "elevated"
    return "normal"


def _datetime_unusable(value: datetime) -> bool:
    return value.tzinfo is None or value.utcoffset() is None


def _fingerprint_material_version(fingerprint: str) -> int:
    try:
        return int(fingerprint.rsplit(" | ", 1)[1])
    except (IndexError, ValueError):
        return MATERIAL_VERSION_START


def _part(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, Enum):
        return value.value
    return str(value).strip()
