"""Frozen canonical domain data models from DEEP_DESIGN section 2."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Mapping

from nft_mint_radar.domain.enums import (
    ActionLinkSafetyState,
    AllocationType,
    AssetKind,
    CampaignState,
    Confidence,
    ContractRelationState,
    DeliveryState,
    NotificationAction,
    NotificationClass,
    NotificationSeverity,
    OnchainExistenceState,
    OpportunityState,
    OpportunityType,
    PriceState,
    ProjectStatus,
    SourceAvailability,
    StageState,
    StageType,
    TrustTier,
    VerificationState,
    VerifiedLinkRelation,
    VerifiedLinkVerificationState,
)

# The DEEP_DESIGN doc field is `class`; `class` is a Python keyword, so this
# map is the single place the divergence is recorded.
DOC_FIELD_ALIASES: dict[str, dict[str, str]] = {
    "Notification": {"notification_class": "class"},
}


def _validate_utc_datetime(value: datetime, field_name: str) -> None:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware UTC")
    if value.utcoffset() != timedelta(0):
        raise ValueError(f"{field_name} must be timezone-aware UTC")


def _validate_optional_utc_datetime(
    value: datetime | None,
    field_name: str,
) -> None:
    if value is not None:
        _validate_utc_datetime(value, field_name)


def _validate_enum(value: object, enum_type: type, field_name: str) -> None:
    if not isinstance(value, enum_type):
        raise ValueError(f"{field_name} must be a {enum_type.__name__}")


def _freeze_tuple_field(instance: object, field_name: str) -> None:
    value = getattr(instance, field_name)
    if not isinstance(value, tuple):
        object.__setattr__(instance, field_name, tuple(value))


@dataclass(frozen=True, kw_only=True)
class ChainIdentity:
    chain_key: str
    eip155_chain_id: int | None = None
    display_name: str
    native_symbol: str | None = None


@dataclass(frozen=True, kw_only=True)
class ContractIdentity:
    chain: ChainIdentity
    address: str
    relation_state: ContractRelationState
    onchain_existence: OnchainExistenceState
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    first_seen_at: datetime
    checked_at: datetime

    def __post_init__(self) -> None:
        _validate_enum(
            self.relation_state,
            ContractRelationState,
            "relation_state",
        )
        _validate_enum(
            self.onchain_existence,
            OnchainExistenceState,
            "onchain_existence",
        )
        _freeze_tuple_field(self, "evidence_ids")
        _validate_utc_datetime(self.first_seen_at, "first_seen_at")
        _validate_utc_datetime(self.checked_at, "checked_at")


@dataclass(frozen=True, kw_only=True)
class AssetAmount:
    amount: Decimal
    asset_kind: AssetKind
    chain_key: str
    token_address: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    usd_estimate: Decimal | None = None
    usd_estimate_at: datetime | None = None

    def __post_init__(self) -> None:
        _validate_enum(self.asset_kind, AssetKind, "asset_kind")
        _validate_optional_utc_datetime(
            self.usd_estimate_at,
            "usd_estimate_at",
        )


@dataclass(frozen=True, kw_only=True)
class VerifiedLink:
    url: str
    normalized_host: str
    relation: VerifiedLinkRelation
    verification_state: VerifiedLinkVerificationState
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    checked_at: datetime

    def __post_init__(self) -> None:
        _validate_enum(self.relation, VerifiedLinkRelation, "relation")
        _validate_enum(
            self.verification_state,
            VerifiedLinkVerificationState,
            "verification_state",
        )
        _freeze_tuple_field(self, "evidence_ids")
        _validate_utc_datetime(self.checked_at, "checked_at")


@dataclass(frozen=True, kw_only=True)
class Evidence:
    id: str
    project_id: str | None = None
    campaign_id: str | None = None
    stage_id: str | None = None
    opportunity_id: str | None = None
    source_id: str
    source_event_id: str | None = None
    captured_at: datetime
    source_published_at: datetime | None = None
    claim_key: str
    normalized_value: Any
    raw_excerpt_or_hash: str | None = None
    canonical_url: str | None = None
    trust_tier: TrustTier
    confidence: Confidence
    verification_state: VerificationState
    source_availability: SourceAvailability
    source_unavailable_since: datetime | None = None
    valid_until: datetime | None = None
    supersedes_evidence_id: str | None = None

    def __post_init__(self) -> None:
        _validate_utc_datetime(self.captured_at, "captured_at")
        _validate_optional_utc_datetime(
            self.source_published_at,
            "source_published_at",
        )
        _validate_enum(self.trust_tier, TrustTier, "trust_tier")
        _validate_enum(self.confidence, Confidence, "confidence")
        _validate_enum(
            self.verification_state,
            VerificationState,
            "verification_state",
        )
        _validate_enum(
            self.source_availability,
            SourceAvailability,
            "source_availability",
        )
        _validate_optional_utc_datetime(
            self.source_unavailable_since,
            "source_unavailable_since",
        )
        _validate_optional_utc_datetime(self.valid_until, "valid_until")


@dataclass(frozen=True, kw_only=True)
class Project:
    id: str
    canonical_name: str
    aliases: tuple[str, ...] = field(default_factory=tuple)
    chains: tuple[ChainIdentity, ...] = field(default_factory=tuple)
    official_links: Mapping[str, tuple[VerifiedLink, ...]]
    contracts: tuple[ContractIdentity, ...] = field(default_factory=tuple)
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        _freeze_tuple_field(self, "aliases")
        _freeze_tuple_field(self, "chains")
        _freeze_tuple_field(self, "contracts")
        _validate_enum(self.status, ProjectStatus, "status")
        _validate_utc_datetime(self.created_at, "created_at")
        _validate_utc_datetime(self.updated_at, "updated_at")


@dataclass(frozen=True, kw_only=True)
class MintCampaign:
    id: str
    project_id: str
    chain_key: str
    contract_address: str | None = None
    supply: int | None = None
    source_campaign_id: str | None = None
    state: CampaignState
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        _validate_enum(self.state, CampaignState, "state")
        _validate_utc_datetime(self.created_at, "created_at")
        _validate_utc_datetime(self.updated_at, "updated_at")


# MintStage.official_action_url is source evidence and is never rendered to a
# user; only an ActionLinkAssessment with safety_state = CONSISTENT may render.
@dataclass(frozen=True, kw_only=True)
class MintStage:
    id: str
    campaign_id: str
    label: str | None = None
    stage_type: StageType
    allocation_type: AllocationType
    state: StageState
    open_at: datetime | None = None
    close_at: datetime | None = None
    price_state: PriceState
    price: AssetAmount | None = None
    max_per_wallet: int | None = None
    eligibility_ref: str | None = None
    official_action_url: VerifiedLink | None = None
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_confidence: Confidence

    def __post_init__(self) -> None:
        _validate_enum(self.stage_type, StageType, "stage_type")
        _validate_enum(
            self.allocation_type,
            AllocationType,
            "allocation_type",
        )
        _validate_enum(self.state, StageState, "state")
        _validate_optional_utc_datetime(self.open_at, "open_at")
        _validate_optional_utc_datetime(self.close_at, "close_at")
        _validate_enum(self.price_state, PriceState, "price_state")
        _freeze_tuple_field(self, "evidence_ids")
        _validate_enum(
            self.evidence_confidence,
            Confidence,
            "evidence_confidence",
        )


# Opportunity.official_action_url is source evidence and is never rendered to a
# user; only an ActionLinkAssessment with safety_state = CONSISTENT may render.
@dataclass(frozen=True, kw_only=True)
class Opportunity:
    id: str
    project_id: str
    type: OpportunityType
    state: OpportunityState
    campaign_id: str | None = None
    stage_id: str | None = None
    registration_open_at: datetime | None = None
    registration_close_at: datetime | None = None
    snapshot_at: datetime | None = None
    results_at: datetime | None = None
    official_action_url: VerifiedLink | None = None
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_confidence: Confidence
    updated_at: datetime

    def __post_init__(self) -> None:
        _validate_enum(self.type, OpportunityType, "type")
        _validate_enum(self.state, OpportunityState, "state")
        _validate_optional_utc_datetime(
            self.registration_open_at,
            "registration_open_at",
        )
        _validate_optional_utc_datetime(
            self.registration_close_at,
            "registration_close_at",
        )
        _validate_optional_utc_datetime(self.snapshot_at, "snapshot_at")
        _validate_optional_utc_datetime(self.results_at, "results_at")
        _freeze_tuple_field(self, "evidence_ids")
        _validate_enum(
            self.evidence_confidence,
            Confidence,
            "evidence_confidence",
        )
        _validate_utc_datetime(self.updated_at, "updated_at")


@dataclass(frozen=True, kw_only=True)
class ActionLinkAssessment:
    url: str
    safety_state: ActionLinkSafetyState
    checked_at: datetime
    project_id: str
    campaign_id: str | None = None
    stage_id: str | None = None
    contract_address: str | None = None
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    reason: str | None = None

    def __post_init__(self) -> None:
        _validate_enum(
            self.safety_state,
            ActionLinkSafetyState,
            "safety_state",
        )
        _validate_utc_datetime(self.checked_at, "checked_at")
        _freeze_tuple_field(self, "evidence_ids")


@dataclass(frozen=True, kw_only=True)
class Notification:
    id: str
    fingerprint: str
    project_id: str
    campaign_id: str | None = None
    stage_id: str | None = None
    opportunity_id: str | None = None
    notification_class: NotificationClass
    severity: NotificationSeverity
    action: NotificationAction
    material_change_keys: tuple[str, ...] = field(default_factory=tuple)
    rendered_payload_hash: str
    delivery_state: DeliveryState
    attempt_count: int
    next_attempt_at: datetime | None = None
    claimed_until: datetime | None = None
    provider_message_id: str | None = None
    last_error: str | None = None
    sent_at: datetime | None = None

    def __post_init__(self) -> None:
        _validate_enum(
            self.notification_class,
            NotificationClass,
            "notification_class",
        )
        _validate_enum(self.severity, NotificationSeverity, "severity")
        _validate_enum(self.action, NotificationAction, "action")
        _freeze_tuple_field(self, "material_change_keys")
        _validate_enum(self.delivery_state, DeliveryState, "delivery_state")
        _validate_optional_utc_datetime(
            self.next_attempt_at,
            "next_attempt_at",
        )
        _validate_optional_utc_datetime(
            self.claimed_until,
            "claimed_until",
        )
        _validate_optional_utc_datetime(self.sent_at, "sent_at")


__all__ = [
    "ActionLinkAssessment",
    "AssetAmount",
    "ChainIdentity",
    "ContractIdentity",
    "DOC_FIELD_ALIASES",
    "Evidence",
    "MintCampaign",
    "MintStage",
    "Notification",
    "Opportunity",
    "Project",
    "VerifiedLink",
]
