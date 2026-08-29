from __future__ import annotations

from datetime import UTC, datetime

from nft_mint_radar.decision.gate import DecisionResult
from nft_mint_radar.domain.enums import (
    AllocationType,
    CampaignState,
    Confidence,
    NotificationAction,
    NotificationSeverity,
    OpportunityState,
    OpportunityType,
    PriceState,
    ProjectStatus,
    StageState,
    StageType,
    VerifiedLinkRelation,
    VerifiedLinkVerificationState,
)
from nft_mint_radar.domain.models import (
    MintCampaign,
    MintStage,
    Opportunity,
    Project,
    VerifiedLink,
)
from nft_mint_radar.notify.render import TelegramRenderInput, render_telegram

NOW = datetime(2026, 8, 30, 0, 0, tzinfo=UTC)


def test_f35_stage_official_action_url_is_not_rendered_without_decision_cta() -> None:
    stage = _stage(
        official_action_url=VerifiedLink(
            url="https://realsite.com/mint",
            normalized_host="realsite.com",
            relation=VerifiedLinkRelation.OFFICIAL_CAMPAIGN,
            verification_state=VerifiedLinkVerificationState.OFFICIAL,
            evidence_ids=("evidence-link",),
            checked_at=NOW,
        )
    )
    decision = DecisionResult(
        action=NotificationAction.APPLY_WL,
        severity=NotificationSeverity.ACTION,
        cta_link=None,
        single_source_unconfirmed=False,
        reasons=("cta_requires_consistent_assessment",),
    )

    output = render_telegram(
        TelegramRenderInput(
            envelope={"run_id": "run-1"},
            project=_project(),
            campaign=_campaign(),
            stage=stage,
            opportunity=_opportunity(),
            scoring=_scoring(),
            decision=decision,
            top_evidence=(),
            fingerprint="fp-1",
            notification_class="WL_OPEN",
        )
    )

    assert output.contains_cta is False
    assert output.cta_safety_state == "NONE"
    assert "https://" not in output.text
    assert "realsite.com" not in output.text


def test_naive_deadline_renders_unresolved_not_kst() -> None:
    stage = _stage()
    object.__setattr__(stage, "close_at", datetime(2026, 8, 30, 12, 0))

    output = render_telegram(
        TelegramRenderInput(
            envelope=None,
            project=_project(),
            campaign=_campaign(),
            stage=stage,
            opportunity=None,
            scoring=_scoring(),
            decision=_watch_decision(),
            top_evidence=(),
            fingerprint="fp-naive",
            notification_class="DEADLINE",
        )
    )

    assert "마감(KST): 미확정(시간대 없음)" in output.text
    assert "2026-08-30 21:00 KST" not in output.text


def test_single_source_unconfirmed_plainly_warns_and_suppresses_cta() -> None:
    decision = DecisionResult(
        action=NotificationAction.WATCH,
        severity=NotificationSeverity.ACTION,
        cta_link=None,
        single_source_unconfirmed=True,
        reasons=("single_account_source_unconfirmed",),
    )

    output = render_telegram(
        TelegramRenderInput(
            envelope=None,
            project=_project(),
            campaign=_campaign(),
            stage=_stage(),
            opportunity=_opportunity(),
            scoring={"quality_score": None, "risk_score": 25, "grade": "B"},
            decision=decision,
            top_evidence=(),
            fingerprint="fp-single",
            notification_class="DEADLINE",
        )
    )

    assert output.single_source_unconfirmed is True
    assert output.contains_cta is False
    assert "검증되지 않은 단일 공식 계정 하나" in output.text
    assert "Quality 알 수 없음" in output.text


def _project() -> Project:
    return Project(
        id="project-1",
        canonical_name="Real Project",
        official_links={},
        contracts=(),
        status=ProjectStatus.ACTIVE,
        created_at=NOW,
        updated_at=NOW,
    )


def _campaign() -> MintCampaign:
    return MintCampaign(
        id="campaign-1",
        project_id="project-1",
        chain_key="ethereum",
        state=CampaignState.ACTIVE,
        created_at=NOW,
        updated_at=NOW,
    )


def _stage(official_action_url: VerifiedLink | None = None) -> MintStage:
    return MintStage(
        id="stage-1",
        campaign_id="campaign-1",
        label="Allowlist",
        stage_type=StageType.ALLOWLIST,
        allocation_type=AllocationType.RAFFLE,
        state=StageState.OPEN,
        open_at=NOW,
        close_at=datetime(2026, 8, 30, 12, 0, tzinfo=UTC),
        price_state=PriceState.FREE,
        official_action_url=official_action_url,
        evidence_confidence=Confidence.HIGH,
    )


def _opportunity() -> Opportunity:
    return Opportunity(
        id="opportunity-1",
        project_id="project-1",
        type=OpportunityType.ALLOWLIST,
        state=OpportunityState.REGISTRATION_OPEN,
        campaign_id="campaign-1",
        stage_id="stage-1",
        registration_close_at=datetime(2026, 8, 30, 12, 0, tzinfo=UTC),
        evidence_confidence=Confidence.HIGH,
        updated_at=NOW,
    )


def _scoring() -> dict[str, object]:
    return {
        "quality_score": 81,
        "alpha_score": 63,
        "effort_score": 20,
        "risk_score": 15,
        "evidence_confidence": Confidence.HIGH,
        "grade": "A",
        "hard_gate": "NONE",
        "components": (),
    }


def _watch_decision() -> DecisionResult:
    return DecisionResult(
        action=NotificationAction.WATCH,
        severity=NotificationSeverity.WATCH,
        cta_link=None,
        single_source_unconfirmed=False,
        reasons=(),
    )
