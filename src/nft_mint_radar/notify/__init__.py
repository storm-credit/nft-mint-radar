"""Notification rendering, fingerprinting, and outbox primitives."""

from nft_mint_radar.notify.fingerprint import (
    FingerprintCandidate,
    MaterialSnapshot,
    RealertDecision,
    build_fingerprint,
    canonical_time_bucket,
    decide_realert,
)
from nft_mint_radar.notify.outbox import (
    InMemoryNotificationRepository,
    OutboxProcessor,
    SendOutcome,
    SendResult,
    Transport,
)
from nft_mint_radar.notify.render import (
    TelegramRenderInput,
    TelegramRenderOutput,
    render_telegram,
)

__all__ = [
    "FingerprintCandidate",
    "InMemoryNotificationRepository",
    "MaterialSnapshot",
    "OutboxProcessor",
    "RealertDecision",
    "SendOutcome",
    "SendResult",
    "TelegramRenderInput",
    "TelegramRenderOutput",
    "Transport",
    "build_fingerprint",
    "canonical_time_bucket",
    "decide_realert",
    "render_telegram",
]
