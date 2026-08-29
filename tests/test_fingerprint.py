from __future__ import annotations

from datetime import UTC, datetime

from nft_mint_radar.domain.enums import (
    DeliveryState,
    NotificationAction,
    NotificationClass,
    NotificationSeverity,
)
from nft_mint_radar.domain.models import Notification
from nft_mint_radar.notify.fingerprint import (
    FingerprintCandidate,
    MaterialSnapshot,
    build_fingerprint,
    canonical_time_bucket,
    decide_realert,
)
from nft_mint_radar.notify.outbox import InMemoryNotificationRepository

NOW = datetime(2026, 8, 30, 0, 0, tzinfo=UTC)
CLAIMED_DEADLINE = datetime(2026, 8, 30, 12, 40, tzinfo=UTC)


def test_f36_claim_times_inside_same_bucket_have_one_fingerprint() -> None:
    first = _candidate(datetime(2026, 8, 30, 12, 31, tzinfo=UTC))
    second = _candidate(datetime(2026, 8, 30, 12, 44, 59, tzinfo=UTC))

    assert build_fingerprint(first) == build_fingerprint(second)

    repository = InMemoryNotificationRepository()
    assert repository.add(_notification("notification-1", build_fingerprint(first))) is True
    assert repository.add(_notification("notification-2", build_fingerprint(second))) is False
    assert len(repository.list()) == 1


def test_f36_claim_times_straddling_bucket_boundary_have_different_fingerprints() -> None:
    before_boundary = _candidate(datetime(2026, 8, 30, 12, 44, 59, tzinfo=UTC))
    at_boundary = _candidate(datetime(2026, 8, 30, 12, 45, tzinfo=UTC))

    assert build_fingerprint(before_boundary) != build_fingerprint(at_boundary)


def test_f36_wording_only_correction_does_not_increment_material_version_or_realert() -> None:
    candidate = _candidate(CLAIMED_DEADLINE)
    notification = _notification("notification-1", build_fingerprint(candidate))
    previous_material = MaterialSnapshot(
        state="REGISTRATION_OPEN",
        deadline=CLAIMED_DEADLINE,
        price="FREE",
        supply=1000,
        action_url=None,
        contract_address=None,
        cta_safety_state="NONE",
        risk_score=20,
    )
    wording_only_correction = MaterialSnapshot(
        state="REGISTRATION_OPEN",
        deadline=CLAIMED_DEADLINE,
        price="FREE",
        supply=1000,
        action_url=None,
        contract_address=None,
        cta_safety_state="NONE",
        risk_score=20,
    )

    decision = decide_realert(
        notification,
        candidate,
        previous_material=previous_material,
        new_material=wording_only_correction,
        reference_time_utc=NOW,
    )

    assert decision.should_alert is False
    assert decision.material_version == 1
    assert decision.fingerprint == notification.fingerprint
    assert decision.material_change_keys == ()
    assert decision.reason == "no_material_change"


def test_bucket_boundary_rounds_down() -> None:
    assert canonical_time_bucket(datetime(2026, 8, 30, 12, 45, tzinfo=UTC)) == (
        "2026-08-30T12:45:00Z"
    )


def _candidate(claim_time: datetime) -> FingerprintCandidate:
    return FingerprintCandidate(
        project_id="project-1",
        campaign_id="campaign-1",
        stage_id="stage-1",
        opportunity_id="opportunity-1",
        notification_class=NotificationClass.DEADLINE,
        normalized_action=NotificationAction.APPLY_WL,
        canonical_claim_time_utc=claim_time,
    )


def _notification(notification_id: str, fingerprint: str) -> Notification:
    return Notification(
        id=notification_id,
        fingerprint=fingerprint,
        project_id="project-1",
        campaign_id="campaign-1",
        stage_id="stage-1",
        opportunity_id="opportunity-1",
        notification_class=NotificationClass.DEADLINE,
        severity=NotificationSeverity.ACTION,
        action=NotificationAction.APPLY_WL,
        rendered_payload_hash="hash-1",
        delivery_state=DeliveryState.PENDING,
        attempt_count=0,
    )
