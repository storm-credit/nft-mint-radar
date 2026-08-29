"""Pure Telegram payload rendering."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Mapping, Sequence
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from nft_mint_radar.decision.gate import DecisionResult
from nft_mint_radar.domain.enums import ActionLinkSafetyState, PriceState
from nft_mint_radar.domain.models import Evidence, MintCampaign, MintStage, Opportunity, Project

try:
    KST = ZoneInfo("Asia/Seoul")
except ZoneInfoNotFoundError:
    KST = timezone(timedelta(hours=9), name="KST")
MAX_TELEGRAM_TEXT_LENGTH = 4096


@dataclass(frozen=True, kw_only=True)
class TelegramRenderInput:
    envelope: Any
    project: Project
    campaign: MintCampaign | None
    stage: MintStage | None
    opportunity: Opportunity | None
    scoring: Any
    decision: DecisionResult
    top_evidence: Sequence[Evidence]
    fingerprint: str = ""
    notification_class: Any = None


@dataclass(frozen=True, kw_only=True)
class TelegramRenderOutput:
    envelope: Any
    text: str
    parse_mode: str | None
    fingerprint: str
    contains_cta: bool
    cta_safety_state: str
    single_source_unconfirmed: bool


def render_telegram(render_input: TelegramRenderInput) -> TelegramRenderOutput:
    """Render a Korean Telegram notification without side effects."""

    decision = render_input.decision
    cta = decision.cta_link
    contains_cta = (
        cta is not None
        and cta.safety_state == ActionLinkSafetyState.CONSISTENT
        and not decision.single_source_unconfirmed
    )

    lines = [
        f"[{_display(_get(render_input.scoring, 'grade'))} / {_display(render_input.notification_class)}]",
        f"프로젝트: {render_input.project.canonical_name}",
        f"캠페인/스테이지: {_campaign_stage(render_input.campaign, render_input.stage)}",
        f"현재 상태: {_current_state(render_input.campaign, render_input.stage, render_input.opportunity)}",
        f"마감(KST): {_format_deadline(_select_deadline(render_input.stage, render_input.opportunity))}",
        f"다음 행동: {_next_action(decision)}",
        "점수: "
        f"Quality {_score(render_input.scoring, 'quality_score')} / "
        f"Alpha {_score(render_input.scoring, 'alpha_score')} / "
        f"Effort {_score(render_input.scoring, 'effort_score')} / "
        f"Risk {_score(render_input.scoring, 'risk_score')}",
        f"증거 신뢰도: {_evidence_confidence(render_input)}",
        f"주요 이유: {_top_reasons(render_input)}",
        f"위험 플래그: {_risk_flags(render_input)}",
    ]

    if decision.single_source_unconfirmed:
        lines.append(
            "주의: 이 주장은 검증되지 않은 단일 공식 계정 하나에 근거합니다. "
            "지갑 연결이나 서명 행동은 안내하지 않습니다."
        )

    if contains_cta:
        lines.append(f"확인 링크: {cta.url}")

    text = "\n".join(lines)
    if len(text) > MAX_TELEGRAM_TEXT_LENGTH:
        text = text[: MAX_TELEGRAM_TEXT_LENGTH - 1].rstrip() + "…"

    return TelegramRenderOutput(
        envelope=render_input.envelope,
        text=text,
        parse_mode=None,
        fingerprint=render_input.fingerprint,
        contains_cta=contains_cta,
        cta_safety_state="CONSISTENT" if contains_cta else "NONE",
        single_source_unconfirmed=decision.single_source_unconfirmed,
    )


def _select_deadline(stage: MintStage | None, opportunity: Opportunity | None) -> datetime | None:
    if opportunity is not None:
        for attr in (
            "registration_close_at",
            "results_at",
            "snapshot_at",
            "registration_open_at",
        ):
            value = getattr(opportunity, attr)
            if value is not None:
                return value

    if stage is not None:
        for attr in ("close_at", "open_at"):
            value = getattr(stage, attr)
            if value is not None:
                return value

    return None


def _format_deadline(value: datetime | None) -> str:
    if value is None:
        return "미확정"
    if value.tzinfo is None or value.utcoffset() is None:
        return "미확정(시간대 없음)"
    return value.astimezone(KST).strftime("%Y-%m-%d %H:%M KST")


def _campaign_stage(campaign: MintCampaign | None, stage: MintStage | None) -> str:
    parts = []
    if campaign is not None:
        parts.append(campaign.id)
    if stage is not None:
        stage_label = stage.label if stage.label is not None else stage.id
        parts.append(stage_label)
    return " / ".join(parts) if parts else "알 수 없음"


def _current_state(
    campaign: MintCampaign | None,
    stage: MintStage | None,
    opportunity: Opportunity | None,
) -> str:
    if opportunity is not None:
        return _display(opportunity.state)
    if stage is not None:
        return _display(stage.state)
    if campaign is not None:
        return _display(campaign.state)
    return "알 수 없음"


def _next_action(decision: DecisionResult) -> str:
    return _display(decision.action)


def _score(scoring: Any, field: str) -> str:
    value = _get(scoring, field)
    if value is None:
        return "알 수 없음"
    if isinstance(value, float):
        return f"{value:.1f}".rstrip("0").rstrip(".")
    if isinstance(value, Decimal):
        return str(value.normalize())
    return str(value)


def _evidence_confidence(render_input: TelegramRenderInput) -> str:
    value = _get(render_input.scoring, "evidence_confidence")
    if value is not None:
        return _display(value)
    if render_input.opportunity is not None:
        return _display(render_input.opportunity.evidence_confidence)
    if render_input.stage is not None:
        return _display(render_input.stage.evidence_confidence)
    if render_input.top_evidence:
        return _display(render_input.top_evidence[0].confidence)
    return "알 수 없음"


def _top_reasons(render_input: TelegramRenderInput) -> str:
    reasons = list(render_input.decision.reasons)
    for component in _get(render_input.scoring, "components") or ():
        reason = _get(component, "reason")
        if reason:
            reasons.append(str(reason))
    if not reasons:
        return "알 수 없음"
    return "; ".join(reasons[:3])


def _risk_flags(render_input: TelegramRenderInput) -> str:
    flags = []
    hard_gate = _get(render_input.scoring, "hard_gate")
    if hard_gate not in (None, "NONE"):
        flags.append(f"hard_gate={_display(hard_gate)}")
    risk_score = _get(render_input.scoring, "risk_score")
    if risk_score is not None and risk_score >= 70:
        flags.append("risk>=70")
    for component in _get(render_input.scoring, "components") or ():
        name = str(_get(component, "name") or "").lower()
        if "risk" in name:
            reason = _get(component, "reason")
            flags.append(str(reason) if reason else name)
    return "; ".join(flags[:3]) if flags else "없음"


def _get(value: Any, field: str) -> Any:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return value.get(field)
    return getattr(value, field, None)


def _display(value: Any) -> str:
    if value is None:
        return "알 수 없음"
    if isinstance(value, Enum):
        return value.value
    return str(value)
