from __future__ import annotations

import re
from dataclasses import fields
from datetime import datetime
from pathlib import Path

import pytest

from nft_mint_radar.domain import enums, models
from nft_mint_radar.domain.enums import (
    CampaignState,
    Confidence,
    DeliveryState,
    NotificationAction,
    NotificationClass,
    NotificationSeverity,
    OpportunityState,
    SourceAvailability,
    SourceHealth,
    TrustTier,
)


ROOT = Path(__file__).resolve().parents[1]
DEEP_DESIGN = ROOT / "docs" / "DEEP_DESIGN.md"


def _deep_design_text() -> str:
    return DEEP_DESIGN.read_text(encoding="utf-8")


def _yaml_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for match in re.finditer(r"```yaml\n(.*?)\n```", text, re.DOTALL):
        block = match.group(1)
        first_line = block.splitlines()[0]
        name_match = re.fullmatch(r"([A-Z][A-Za-z0-9_]*):", first_line)
        if name_match:
            blocks[name_match.group(1)] = block
    return blocks


def _deep_design_blocks() -> dict[str, str]:
    return _yaml_blocks(_deep_design_text())


def _field_type(block_name: str, field_name: str) -> str:
    block = _deep_design_blocks()[block_name]
    for line in block.splitlines()[1:]:
        match = re.fullmatch(r"  ([A-Za-z_][A-Za-z0-9_]*):\s*(.+)", line)
        if match and match.group(1) == field_name:
            return match.group(2)
    raise AssertionError(f"{block_name}.{field_name} not found in DEEP_DESIGN")


def _enum_values(block_name: str, field_name: str) -> set[str]:
    return set(_field_type(block_name, field_name).split("|"))


def _top_level_field_names(block_name: str) -> list[str]:
    block = _deep_design_blocks()[block_name]
    names = []
    for line in block.splitlines()[1:]:
        match = re.fullmatch(r"  ([A-Za-z_][A-Za-z0-9_]*):.*", line)
        if match:
            names.append(match.group(1))
    return names


def _python_enum_values(enum_class: type) -> set[str]:
    return {member.value for member in enum_class}


@pytest.mark.parametrize(
    ("enum_class", "block_name", "field_name"),
    [
        (TrustTier, "Source", "trust_tier"),
        (Confidence, "Evidence", "confidence"),
        (enums.VerificationState, "Evidence", "verification_state"),
        (SourceAvailability, "Evidence", "source_availability"),
        (enums.PriceState, "MintStage", "price_state"),
        (enums.AssetKind, "AssetAmount", "asset_kind"),
        (CampaignState, "MintCampaign", "state"),
        (enums.StageState, "MintStage", "state"),
        (OpportunityState, "Opportunity", "state"),
        (enums.OpportunityType, "Opportunity", "type"),
        (enums.ActionLinkSafetyState, "ActionLinkAssessment", "safety_state"),
        (NotificationClass, "Notification", "class"),
        (NotificationSeverity, "Notification", "severity"),
        (NotificationAction, "Notification", "action"),
        (DeliveryState, "Notification", "delivery_state"),
        (SourceHealth, "Source", "health"),
    ],
)
def test_enum_values_match_deep_design(
    enum_class: type,
    block_name: str,
    field_name: str,
) -> None:
    assert _python_enum_values(enum_class) == _enum_values(block_name, field_name)


@pytest.mark.parametrize(
    ("model_class", "block_name"),
    [
        (models.ChainIdentity, "ChainIdentity"),
        (models.ContractIdentity, "ContractIdentity"),
        (models.AssetAmount, "AssetAmount"),
        (models.Evidence, "Evidence"),
        (models.Project, "Project"),
        (models.MintCampaign, "MintCampaign"),
        (models.MintStage, "MintStage"),
        (models.Opportunity, "Opportunity"),
        (models.VerifiedLink, "VerifiedLink"),
        (models.ActionLinkAssessment, "ActionLinkAssessment"),
        (models.Notification, "Notification"),
    ],
)
def test_dataclass_fields_match_deep_design_order(
    model_class: type,
    block_name: str,
) -> None:
    aliases = models.DOC_FIELD_ALIASES.get(block_name, {})
    python_field_names = [
        aliases.get(field.name, field.name) for field in fields(model_class)
    ]
    assert python_field_names == _top_level_field_names(block_name)


def test_doc_field_aliases_are_explicit_and_narrow() -> None:
    assert models.DOC_FIELD_ALIASES == {
        "Notification": {"notification_class": "class"},
    }


def test_notification_supports_equality_and_useful_repr() -> None:
    args = {
        "id": "notification-1",
        "fingerprint": "fingerprint-1",
        "project_id": "project-1",
        "notification_class": NotificationClass.DISCOVERY,
        "severity": NotificationSeverity.INFO,
        "action": NotificationAction.WATCH,
        "rendered_payload_hash": "payload-hash-1",
        "delivery_state": DeliveryState.PENDING,
        "attempt_count": 0,
    }

    first = models.Notification(**args)
    second = models.Notification(**args)

    assert first == second
    assert "Notification" in repr(first)


def test_naive_datetime_raises_value_error() -> None:
    with pytest.raises(ValueError):
        models.MintCampaign(
            id="campaign-1",
            project_id="project-1",
            chain_key="ethereum",
            state=CampaignState.DISCOVERED,
            created_at=datetime(2026, 8, 29, 0, 0, 0),
            updated_at=datetime(2026, 8, 29, 0, 0, 0),
        )


def test_deep_design_yaml_type_closure() -> None:
    blocks = _yaml_blocks(_deep_design_text())
    defined_names = set(blocks)
    missing_refs = set()

    for block_name, block in blocks.items():
        for line in block.splitlines()[1:]:
            stripped = line.strip()
            if ":" not in stripped:
                continue
            _, type_spec = stripped.split(":", 1)
            type_spec = type_spec.strip()
            if not type_spec:
                continue
            for token in type_spec.replace("[", "").replace("]", "").split("|"):
                token = token.strip()
                if token and token[0].isupper() and not token.isupper():
                    if token not in defined_names:
                        missing_refs.add(f"{block_name}: {token}")

    assert missing_refs == set()
