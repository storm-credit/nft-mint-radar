from __future__ import annotations

from datetime import UTC, datetime

from nft_mint_radar.decision.gate import (
    DecisionResult,
    UrgencyCorroboration,
    decide,
)
from nft_mint_radar.domain.enums import (
    ActionLinkSafetyState,
    Confidence,
    NotificationAction,
    NotificationSeverity,
)
from nft_mint_radar.domain.models import ActionLinkAssessment

NOW = datetime(2026, 8, 30, tzinfo=UTC)
WALLET_ACTIONS = {
    NotificationAction.APPLY_WL,
    NotificationAction.PREPARE,
    NotificationAction.MINT_RECHECK,
}


def test_f24_quarantined_unseen_domain_cannot_carry_cta_or_wallet_action() -> None:
    """F24: official identity cannot make a quarantined unseen host clickable."""
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.QUARANTINED),
        evidence_confidence=Confidence.HIGH,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.CORROBORATED,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.APPLY_WL,
        proposed_severity=NotificationSeverity.WARNING,
    )

    assert result.cta_link is None
    assert result.action not in WALLET_ACTIONS
    assert "cta_safety_not_consistent" in result.reasons
    assert "unsafe_cta_blocks_wallet_action" in result.reasons


def test_f25_revoked_link_invalidates_previously_consistent_url() -> None:
    """F25: REVOKED links cannot survive into the decision CTA."""
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.REVOKED),
        evidence_confidence=Confidence.HIGH,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.CORROBORATED,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.MINT_RECHECK,
        proposed_severity=NotificationSeverity.WARNING,
    )

    assert result.cta_link is None
    assert result.action not in WALLET_ACTIONS
    assert "unsafe_cta_blocks_wallet_action" in result.reasons


def test_f29_deleted_single_account_evidence_caps_alert_and_suppresses_cta() -> None:
    """F29: deleted account-source announcement cannot stay urgent or actionable."""
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.CONSISTENT),
        evidence_confidence=Confidence.HIGH,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.SINGLE_ACCOUNT_SOURCE,
        has_unavailable_only_evidence=True,
        proposed_action=NotificationAction.APPLY_WL,
        proposed_severity=NotificationSeverity.URGENT,
    )

    assert result.severity == NotificationSeverity.WATCH
    assert result.cta_link is None
    assert result.action not in WALLET_ACTIONS
    assert result.single_source_unconfirmed is True
    assert "single_account_source_unconfirmed" in result.reasons
    assert "unavailable_only_evidence_caps_output" in result.reasons


def test_f30_single_account_source_suppresses_valid_known_good_url() -> None:
    """F30: known-good URL still loses CTA when urgency is single-source."""
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.CONSISTENT),
        evidence_confidence=Confidence.HIGH,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.SINGLE_ACCOUNT_SOURCE,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.MINT_RECHECK,
        proposed_severity=NotificationSeverity.URGENT,
    )

    assert result.severity != NotificationSeverity.URGENT
    assert result.cta_link is None
    assert result.single_source_unconfirmed is True
    assert "single_account_source_unconfirmed" in result.reasons


def test_f35_official_action_url_without_consistent_assessment_has_no_cta() -> None:
    """F35: stage official_action_url is not renderable without CONSISTENT assessment."""
    stage_official_action_url_exists = True

    result = decide(
        assessment=None,
        evidence_confidence=Confidence.HIGH,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.NOT_APPLICABLE,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.APPLY_WL,
        proposed_severity=NotificationSeverity.ACTION,
    )

    assert stage_official_action_url_exists
    assert result.cta_link is None
    assert "cta_requires_consistent_assessment" in result.reasons


def test_unverified_assessment_cannot_be_cta() -> None:
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.UNVERIFIED),
        evidence_confidence=Confidence.HIGH,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.NOT_APPLICABLE,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.WATCH,
        proposed_severity=NotificationSeverity.WATCH,
    )

    assert result.cta_link is None
    assert "cta_safety_not_consistent" in result.reasons


def test_risk_score_70_blocks_wallet_action_without_upgrading() -> None:
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.CONSISTENT),
        evidence_confidence=Confidence.HIGH,
        risk_score=70,
        urgency_corroboration=UrgencyCorroboration.CORROBORATED,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.PREPARE,
        proposed_severity=NotificationSeverity.ACTION,
    )

    assert result.action == NotificationAction.WATCH
    assert result.severity == NotificationSeverity.ACTION
    assert "risk_score_blocks_wallet_action" in result.reasons


def test_low_confidence_caps_wallet_action_not_severity() -> None:
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.CONSISTENT),
        evidence_confidence=Confidence.LOW,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.CORROBORATED,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.PREPARE,
        proposed_severity=NotificationSeverity.URGENT,
    )

    assert result.action == NotificationAction.WATCH
    assert result.severity == NotificationSeverity.URGENT
    assert "low_confidence_caps_action" in result.reasons


def test_warning_survives_low_single_source_and_unavailable_caps_without_cta() -> None:
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.CONSISTENT),
        evidence_confidence=Confidence.LOW,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.SINGLE_ACCOUNT_SOURCE,
        has_unavailable_only_evidence=True,
        proposed_action=NotificationAction.AVOID,
        proposed_severity=NotificationSeverity.WARNING,
    )

    assert result.action == NotificationAction.AVOID
    assert result.severity == NotificationSeverity.WARNING
    assert result.cta_link is None
    assert result.single_source_unconfirmed is True
    assert "single_account_source_unconfirmed" in result.reasons
    assert "unavailable_only_evidence_caps_output" in result.reasons


def test_warning_never_carries_consistent_cta() -> None:
    result = decide(
        assessment=_assessment(ActionLinkSafetyState.CONSISTENT),
        evidence_confidence=Confidence.HIGH,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.CORROBORATED,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.AVOID,
        proposed_severity=NotificationSeverity.WARNING,
    )

    assert result.severity == NotificationSeverity.WARNING
    assert result.cta_link is None
    assert "warning_suppresses_cta" in result.reasons


def test_consistent_assessment_can_carry_cta_when_no_hard_rule_blocks_it() -> None:
    assessment = _assessment(ActionLinkSafetyState.CONSISTENT)

    result = decide(
        assessment=assessment,
        evidence_confidence=Confidence.HIGH,
        risk_score=10,
        urgency_corroboration=UrgencyCorroboration.CORROBORATED,
        has_unavailable_only_evidence=False,
        proposed_action=NotificationAction.APPLY_WL,
        proposed_severity=NotificationSeverity.ACTION,
    )

    assert isinstance(result, DecisionResult)
    assert result.action == NotificationAction.APPLY_WL
    assert result.severity == NotificationSeverity.ACTION
    assert result.cta_link == assessment
    assert result.single_source_unconfirmed is False
    assert result.reasons == ()


def _assessment(state: ActionLinkSafetyState) -> ActionLinkAssessment:
    return ActionLinkAssessment(
        url="https://realsite.com/mint",
        safety_state=state,
        checked_at=NOW,
        project_id="project-1",
        evidence_ids=("evidence-realsite.com",),
        reason=None if state == ActionLinkSafetyState.CONSISTENT else state.value.lower(),
    )
