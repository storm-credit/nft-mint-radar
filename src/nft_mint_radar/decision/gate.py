"""Pure decision-stage hard-rule enforcement."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from nft_mint_radar.domain.enums import (
    ActionLinkSafetyState,
    Confidence,
    NotificationAction,
    NotificationSeverity,
)
from nft_mint_radar.domain.models import ActionLinkAssessment


class UrgencyCorroboration(str, Enum):
    SINGLE_ACCOUNT_SOURCE = "SINGLE_ACCOUNT_SOURCE"
    CORROBORATED = "CORROBORATED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, kw_only=True)
class DecisionResult:
    action: NotificationAction
    severity: NotificationSeverity
    cta_link: ActionLinkAssessment | None
    single_source_unconfirmed: bool
    reasons: tuple[str, ...]


_WALLET_ACTIONS = {
    NotificationAction.APPLY_WL,
    NotificationAction.PREPARE,
    NotificationAction.MINT_RECHECK,
}
_SEVERITY_RANK = {
    NotificationSeverity.INFO: 0,
    NotificationSeverity.WATCH: 1,
    NotificationSeverity.ACTION: 2,
    NotificationSeverity.URGENT: 3,
}


def decide(
    assessment: ActionLinkAssessment | None,
    evidence_confidence: Confidence,
    risk_score: int,
    urgency_corroboration: UrgencyCorroboration,
    has_unavailable_only_evidence: bool,
    proposed_action: NotificationAction,
    proposed_severity: NotificationSeverity,
) -> DecisionResult:
    """Apply deterministic hard-rule downgrades without fetching anything."""

    action = proposed_action
    severity = proposed_severity
    reasons: list[str] = []

    if assessment is not None and assessment.safety_state == ActionLinkSafetyState.CONSISTENT:
        cta_link: ActionLinkAssessment | None = assessment
    else:
        cta_link = None
        if assessment is None:
            reasons.append("cta_requires_consistent_assessment")
        else:
            reasons.append("cta_safety_not_consistent")

    if (
        assessment is not None
        and assessment.safety_state
        in {ActionLinkSafetyState.QUARANTINED, ActionLinkSafetyState.REVOKED}
        and action in _WALLET_ACTIONS
    ):
        action = NotificationAction.WATCH
        reasons.append("unsafe_cta_blocks_wallet_action")

    if risk_score >= 70 and action in _WALLET_ACTIONS:
        action = NotificationAction.WATCH
        reasons.append("risk_score_blocks_wallet_action")

    if evidence_confidence == Confidence.LOW and action in _WALLET_ACTIONS:
        action = NotificationAction.WATCH
        reasons.append("low_confidence_caps_action")

    single_source_unconfirmed = (
        urgency_corroboration == UrgencyCorroboration.SINGLE_ACCOUNT_SOURCE
    )
    if single_source_unconfirmed:
        if severity == NotificationSeverity.URGENT:
            severity = NotificationSeverity.ACTION
        if cta_link is not None:
            cta_link = None
        reasons.append("single_account_source_unconfirmed")

    if has_unavailable_only_evidence:
        if action in _WALLET_ACTIONS:
            action = NotificationAction.WATCH
        if _exceeds_watch(severity):
            severity = NotificationSeverity.WATCH
        if cta_link is not None:
            cta_link = None
        reasons.append("unavailable_only_evidence_caps_output")

    if severity == NotificationSeverity.WARNING and cta_link is not None:
        cta_link = None
        reasons.append("warning_suppresses_cta")

    return DecisionResult(
        action=action,
        severity=severity,
        cta_link=cta_link,
        single_source_unconfirmed=single_source_unconfirmed,
        reasons=tuple(reasons),
    )


def _exceeds_watch(severity: NotificationSeverity) -> bool:
    rank = _SEVERITY_RANK.get(severity)
    return rank is not None and rank > _SEVERITY_RANK[NotificationSeverity.WATCH]
