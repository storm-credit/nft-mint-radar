"""Canonical enum values copied from DEEP_DESIGN section 2."""

from enum import Enum


class TrustTier(str, Enum):
    T0 = "T0"
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"


class Confidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class VerificationState(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    CORROBORATED = "CORROBORATED"
    OFFICIAL = "OFFICIAL"
    CONFLICTED = "CONFLICTED"
    REVOKED = "REVOKED"
    STALE = "STALE"


class SourceAvailability(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class ProjectStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    ACTIVE = "ACTIVE"
    DORMANT = "DORMANT"
    REACTIVATED = "REACTIVATED"
    ENDED = "ENDED"
    SUSPECT = "SUSPECT"
    BLOCKED = "BLOCKED"


class SourceType(str, Enum):
    X = "X"
    WEBSITE = "WEBSITE"
    DISCORD = "DISCORD"
    TELEGRAM = "TELEGRAM"
    OPENSEA = "OPENSEA"
    PREMINT = "PREMINT"
    GALXE = "GALXE"
    GUILD = "GUILD"
    DUNE = "DUNE"
    ONCHAIN = "ONCHAIN"
    REDDIT = "REDDIT"
    OTHER = "OTHER"


class SourceRole(str, Enum):
    DISCOVERY = "DISCOVERY"
    VERIFICATION = "VERIFICATION"
    ONCHAIN = "ONCHAIN"
    SENTIMENT = "SENTIMENT"
    BEHAVIOR = "BEHAVIOR"


class SourceHealth(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"


class AssetKind(str, Enum):
    NATIVE = "NATIVE"
    ERC20 = "ERC20"
    OTHER = "OTHER"


class PriceState(str, Enum):
    FREE = "FREE"
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"
    VARIABLE = "VARIABLE"


class CampaignState(str, Enum):
    DISCOVERED = "DISCOVERED"
    SCHEDULED = "SCHEDULED"
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"


class StageType(str, Enum):
    ALLOWLIST = "ALLOWLIST"
    HOLDER = "HOLDER"
    COMMUNITY = "COMMUNITY"
    FCFS = "FCFS"
    RAFFLE = "RAFFLE"
    PUBLIC = "PUBLIC"
    TEAM = "TEAM"
    OTHER = "OTHER"


class AllocationType(str, Enum):
    FCFS = "FCFS"
    RAFFLE = "RAFFLE"
    GUARANTEED = "GUARANTEED"
    HOLDER = "HOLDER"
    PUBLIC = "PUBLIC"
    UNKNOWN = "UNKNOWN"


class StageState(str, Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"


class OpportunityType(str, Enum):
    ALLOWLIST = "ALLOWLIST"
    RAFFLE = "RAFFLE"
    HOLDER_MINT = "HOLDER_MINT"
    FREE_MINT = "FREE_MINT"
    PAID_MINT = "PAID_MINT"
    PUBLIC_MINT = "PUBLIC_MINT"
    AIRDROP = "AIRDROP"
    LEGACY_HOLDER_ACCESS = "LEGACY_HOLDER_ACCESS"
    OTHER = "OTHER"


class OpportunityState(str, Enum):
    RUMORED = "RUMORED"
    DISCOVERED = "DISCOVERED"
    REGISTRATION_PENDING = "REGISTRATION_PENDING"
    REGISTRATION_OPEN = "REGISTRATION_OPEN"
    REGISTRATION_CLOSED = "REGISTRATION_CLOSED"
    RESULTS_PENDING = "RESULTS_PENDING"
    MINT_SCHEDULED = "MINT_SCHEDULED"
    MINT_OPEN = "MINT_OPEN"
    ENDED = "ENDED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class QuestActionType(str, Enum):
    FOLLOW_X = "FOLLOW_X"
    LIKE_X = "LIKE_X"
    REPOST_X = "REPOST_X"
    COMMENT_X = "COMMENT_X"
    TAG_FRIEND = "TAG_FRIEND"
    JOIN_DISCORD = "JOIN_DISCORD"
    DISCORD_ROLE = "DISCORD_ROLE"
    DISCORD_LEVEL = "DISCORD_LEVEL"
    GALXE = "GALXE"
    GUILD = "GUILD"
    PREMINT_REGISTER = "PREMINT_REGISTER"
    HOLD_NFT = "HOLD_NFT"
    HOLD_TOKEN = "HOLD_TOKEN"
    ONCHAIN_ACTION = "ONCHAIN_ACTION"
    REFERRAL = "REFERRAL"
    CUSTOM = "CUSTOM"


class QuestExecutionMode(str, Enum):
    MANUAL = "MANUAL"
    EXTERNAL_PLATFORM = "EXTERNAL_PLATFORM"
    READ_ONLY_VERIFY = "READ_ONLY_VERIFY"


class QuestSafetyClass(str, Enum):
    SAFE_MANUAL = "SAFE_MANUAL"
    WALLET_SIGNATURE_REQUIRED = "WALLET_SIGNATURE_REQUIRED"
    SOCIAL_ACTION = "SOCIAL_ACTION"
    DISCORD_ACTIVITY = "DISCORD_ACTIVITY"
    UNKNOWN = "UNKNOWN"


class UserProgressState(str, Enum):
    UNKNOWN = "UNKNOWN"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    VERIFIED = "VERIFIED"
    WON = "WON"
    WAITLISTED = "WAITLISTED"
    LOST = "LOST"
    EXPIRED = "EXPIRED"
    SKIPPED = "SKIPPED"


class ProgressProvenance(str, Enum):
    USER_CONFIRMED = "USER_CONFIRMED"
    PROVIDER_VERIFIED = "PROVIDER_VERIFIED"
    SYSTEM_OBSERVED = "SYSTEM_OBSERVED"
    UNKNOWN = "UNKNOWN"


class WalletCategory(str, Enum):
    COLLECTOR = "COLLECTOR"
    TRADER = "TRADER"
    ARTIST = "ARTIST"
    FUND = "FUND"
    DEPLOYER = "DEPLOYER"
    INFLUENCER = "INFLUENCER"
    UNKNOWN = "UNKNOWN"


class InfluencerCategory(str, Enum):
    ANALYST = "ANALYST"
    COLLECTOR = "COLLECTOR"
    ARTIST = "ARTIST"
    FOUNDER = "FOUNDER"
    TRADER = "TRADER"
    SECURITY_RESEARCHER = "SECURITY_RESEARCHER"
    OTHER = "OTHER"


class NotificationClass(str, Enum):
    DISCOVERY = "DISCOVERY"
    WL_OPEN = "WL_OPEN"
    DEADLINE = "DEADLINE"
    COHORT_HIT = "COHORT_HIT"
    CONTRACT_LINKED = "CONTRACT_LINKED"
    RISK_DOWNGRADE = "RISK_DOWNGRADE"
    WL_RESULT = "WL_RESULT"
    MINT_RECHECK = "MINT_RECHECK"
    REACTIVATION = "REACTIVATION"


class NotificationSeverity(str, Enum):
    INFO = "INFO"
    WATCH = "WATCH"
    ACTION = "ACTION"
    URGENT = "URGENT"
    WARNING = "WARNING"


class NotificationAction(str, Enum):
    WATCH = "WATCH"
    APPLY_WL = "APPLY_WL"
    PREPARE = "PREPARE"
    MINT_RECHECK = "MINT_RECHECK"
    AVOID = "AVOID"
    NO_ALERT = "NO_ALERT"


class DeliveryState(str, Enum):
    PENDING = "PENDING"
    CLAIMED = "CLAIMED"
    SENT = "SENT"
    AMBIGUOUS = "AMBIGUOUS"
    FAILED = "FAILED"
    ABANDONED = "ABANDONED"


class VerifiedLinkRelation(str, Enum):
    OFFICIAL_SITE = "OFFICIAL_SITE"
    OFFICIAL_SOCIAL = "OFFICIAL_SOCIAL"
    OFFICIAL_CAMPAIGN = "OFFICIAL_CAMPAIGN"
    OFFICIAL_MARKETPLACE = "OFFICIAL_MARKETPLACE"
    OFFICIAL_CONTRACT = "OFFICIAL_CONTRACT"
    OTHER = "OTHER"


class VerifiedLinkVerificationState(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    CORROBORATED = "CORROBORATED"
    OFFICIAL = "OFFICIAL"
    REVOKED = "REVOKED"
    SUSPICIOUS = "SUSPICIOUS"


class ActionLinkSafetyState(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    CONSISTENT = "CONSISTENT"
    QUARANTINED = "QUARANTINED"
    REVOKED = "REVOKED"


class ContractRelationState(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    CORROBORATED = "CORROBORATED"
    OFFICIAL = "OFFICIAL"
    CONFLICTED = "CONFLICTED"
    REVOKED = "REVOKED"


class OnchainExistenceState(str, Enum):
    CONFIRMED = "CONFIRMED"
    NOT_FOUND = "NOT_FOUND"
    UNKNOWN = "UNKNOWN"


__all__ = [
    "ActionLinkSafetyState",
    "AllocationType",
    "AssetKind",
    "CampaignState",
    "Confidence",
    "ContractRelationState",
    "DeliveryState",
    "InfluencerCategory",
    "NotificationAction",
    "NotificationClass",
    "NotificationSeverity",
    "OnchainExistenceState",
    "OpportunityState",
    "OpportunityType",
    "PriceState",
    "ProgressProvenance",
    "ProjectStatus",
    "QuestActionType",
    "QuestExecutionMode",
    "QuestSafetyClass",
    "SourceAvailability",
    "SourceHealth",
    "SourceRole",
    "SourceType",
    "StageState",
    "StageType",
    "TrustTier",
    "UserProgressState",
    "VerificationState",
    "VerifiedLinkRelation",
    "VerifiedLinkVerificationState",
    "WalletCategory",
]
