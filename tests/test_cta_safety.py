from __future__ import annotations

from datetime import UTC, datetime

from nft_mint_radar.domain.enums import (
    ActionLinkSafetyState,
    ProjectStatus,
    VerifiedLinkRelation,
    VerifiedLinkVerificationState,
)
from nft_mint_radar.domain.models import Project, VerifiedLink
from nft_mint_radar.safety.cta import assess_action_link

NOW = datetime(2026, 8, 30, tzinfo=UTC)
KNOWN_CONTRACT = "0x1111111111111111111111111111111111111111"


def test_f24_official_identity_does_not_make_unseen_host_safe() -> None:
    """F24: official X posts urgent mint link on an unseen domain."""
    project = _project(
        _link(
            "https://realsite.com",
            relation=VerifiedLinkRelation.OFFICIAL_SITE,
            state=VerifiedLinkVerificationState.OFFICIAL,
        ),
        _link(
            "https://x.com/realproject",
            relation=VerifiedLinkRelation.OFFICIAL_SOCIAL,
            state=VerifiedLinkVerificationState.OFFICIAL,
        ),
    )

    assessment = assess_action_link(
        "https://evil-mint.example/mint",
        project,
        frozenset({KNOWN_CONTRACT}),
        NOW,
    )

    assert assessment.safety_state == ActionLinkSafetyState.QUARANTINED
    assert assessment.reason == "unexpected_host"


def test_f25_disavowed_link_is_revoked_not_consistent() -> None:
    """F25: after disavowal the previously surfaced link is REVOKED."""
    project = _project(
        _link(
            "https://realsite.com/mint",
            relation=VerifiedLinkRelation.OFFICIAL_SITE,
            state=VerifiedLinkVerificationState.REVOKED,
        ),
    )

    assessment = assess_action_link(
        "https://realsite.com/mint",
        project,
        frozenset({KNOWN_CONTRACT}),
        NOW,
    )

    assert assessment.safety_state == ActionLinkSafetyState.REVOKED
    assert assessment.reason == "link_revoked"
    assert assessment.safety_state != ActionLinkSafetyState.CONSISTENT


def test_unknown_contract_on_verified_host_is_quarantined() -> None:
    project = _project(
        _link(
            "https://realsite.com",
            relation=VerifiedLinkRelation.OFFICIAL_SITE,
            state=VerifiedLinkVerificationState.OFFICIAL,
        ),
    )

    assessment = assess_action_link(
        "https://realsite.com/mint?contract=0x2222222222222222222222222222222222222222",
        project,
        frozenset({KNOWN_CONTRACT}),
        NOW,
    )

    assert assessment.safety_state == ActionLinkSafetyState.QUARANTINED
    assert assessment.reason == "unexpected_contract"


def test_adversarial_urls_quarantine_without_exceptions() -> None:
    for url in (
        "https://realsite.com@evil.com/mint",
        "http://realsite.com/mint",
        "javascript:alert(1)",
        "https://ｒealsite.com/mint",
        "https://evil-realsite.com/mint",
        "https://realsite.com.evil.com/mint",
        "https://192.0.2.1/mint",
        "",
        "not a url",
    ):
        project = _project(
            _link(
                "https://realsite.com",
                relation=VerifiedLinkRelation.OFFICIAL_SITE,
                state=VerifiedLinkVerificationState.OFFICIAL,
            ),
        )

        assessment = assess_action_link(url, project, frozenset({KNOWN_CONTRACT}), NOW)

        assert assessment.safety_state == ActionLinkSafetyState.QUARANTINED
        assert assessment.reason is not None


def test_embedded_redirect_targets_and_path_traversal_are_quarantined() -> None:
    project = _project(
        _link(
            "https://realsite.com",
            relation=VerifiedLinkRelation.OFFICIAL_SITE,
            state=VerifiedLinkVerificationState.OFFICIAL,
        ),
    )

    expected_reasons = {
        "https://realsite.com/out?url=https://evil.com/drain": "embedded_redirect_target",
        "https://realsite.com/redirect?target=https%3A%2F%2Fevil.com": (
            "embedded_redirect_target"
        ),
        "https://realsite.com/r?to=%253A%252F%252Fevil.com": (
            "embedded_redirect_target"
        ),
        "https://realsite.com/go?next=//evil.com/drain": "embedded_redirect_target",
        "https://realsite.com/mint#https://evil.com": "embedded_redirect_target",
        "https://realsite.com/../evil": "path_traversal",
    }

    for url, reason in expected_reasons.items():
        assessment = assess_action_link(url, project, frozenset({KNOWN_CONTRACT}), NOW)

        assert assessment.safety_state == ActionLinkSafetyState.QUARANTINED
        assert assessment.reason == reason


def test_ordinary_verified_urls_remain_consistent() -> None:
    project = _project(
        _link(
            "https://realsite.com",
            relation=VerifiedLinkRelation.OFFICIAL_SITE,
            state=VerifiedLinkVerificationState.OFFICIAL,
        ),
    )

    for url in (
        "https://realsite.com/mint",
        "https://realsite.com/mint?stage=gtd&ref=abc123",
        "https://mint.realsite.com/claim",
        "https://realsite.com/out?url=https://realsite.com/mint",
    ):
        assessment = assess_action_link(url, project, frozenset({KNOWN_CONTRACT}), NOW)

        assert assessment.safety_state == ActionLinkSafetyState.CONSISTENT
        assert assessment.reason is None


def test_no_verified_relation_evidence_is_unverified() -> None:
    project = _project()

    assessment = assess_action_link(
        "https://realsite.com/mint",
        project,
        frozenset({KNOWN_CONTRACT}),
        NOW,
    )

    assert assessment.safety_state == ActionLinkSafetyState.UNVERIFIED
    assert assessment.reason == "no_verified_project_relations"


def _project(*links: VerifiedLink) -> Project:
    return Project(
        id="project-1",
        canonical_name="Real Project",
        official_links={"links": tuple(links)},
        contracts=(),
        status=ProjectStatus.ACTIVE,
        created_at=NOW,
        updated_at=NOW,
    )


def _link(
    url: str,
    *,
    relation: VerifiedLinkRelation,
    state: VerifiedLinkVerificationState,
) -> VerifiedLink:
    host = url.split("//", 1)[1].split("/", 1)[0].lower()
    return VerifiedLink(
        url=url,
        normalized_host=host,
        relation=relation,
        verification_state=state,
        evidence_ids=(f"evidence-{host}",),
        checked_at=NOW,
    )
