"""Deterministic CTA safety gate."""

from __future__ import annotations

import re
from datetime import datetime
from urllib.parse import urlparse

from nft_mint_radar.domain.enums import (
    ActionLinkSafetyState,
    VerifiedLinkRelation,
    VerifiedLinkVerificationState,
)
from nft_mint_radar.domain.models import ActionLinkAssessment, Project, VerifiedLink
from nft_mint_radar.safety.url import (
    UrlSafetyError,
    embedded_redirect_hosts,
    has_path_traversal,
    is_same_or_subdomain,
    normalize_host,
)

_EVM_ADDRESS_RE = re.compile(r"0x[a-fA-F0-9]{40}")
_VERIFIED_STATES = {
    VerifiedLinkVerificationState.CORROBORATED,
    VerifiedLinkVerificationState.OFFICIAL,
}
_VERIFIED_RELATIONS = {
    VerifiedLinkRelation.OFFICIAL_SITE,
    VerifiedLinkRelation.OFFICIAL_SOCIAL,
    VerifiedLinkRelation.OFFICIAL_CAMPAIGN,
    VerifiedLinkRelation.OFFICIAL_MARKETPLACE,
    VerifiedLinkRelation.OFFICIAL_CONTRACT,
}


def assess_action_link(
    url: str,
    project: Project,
    known_contract_addresses: frozenset[str],
    now: datetime,
) -> ActionLinkAssessment:
    """Assess whether a wallet-impacting URL is safe to render."""

    try:
        candidate_host = normalize_host(url)
    except UrlSafetyError as exc:
        return _assessment(
            url=url,
            project=project,
            now=now,
            state=ActionLinkSafetyState.QUARANTINED,
            reason=f"url_{exc.reason}",
        )
    except Exception:
        return _assessment(
            url=url,
            project=project,
            now=now,
            state=ActionLinkSafetyState.QUARANTINED,
            reason="url_unparseable_url",
        )

    if has_path_traversal(url):
        return _assessment(
            url=url,
            project=project,
            now=now,
            state=ActionLinkSafetyState.QUARANTINED,
            reason="path_traversal",
        )

    revoked_links = tuple(_iter_links_by_state(project, {VerifiedLinkVerificationState.REVOKED}))
    if any(_same_url_or_path(url, candidate_host, link) for link in revoked_links):
        return _assessment(
            url=url,
            project=project,
            now=now,
            state=ActionLinkSafetyState.REVOKED,
            reason="link_revoked",
            evidence_ids=_evidence_ids(revoked_links),
        )

    verified_links = tuple(_iter_links_by_state(project, _VERIFIED_STATES))
    if not verified_links:
        return _assessment(
            url=url,
            project=project,
            now=now,
            state=ActionLinkSafetyState.UNVERIFIED,
            reason="no_verified_project_relations",
        )

    matching_links = tuple(
        link
        for link in verified_links
        if link.relation in _VERIFIED_RELATIONS
        and is_same_or_subdomain(candidate_host, _verified_link_host(link))
    )
    if not matching_links:
        return _assessment(
            url=url,
            project=project,
            now=now,
            state=ActionLinkSafetyState.QUARANTINED,
            reason="unexpected_host",
        )

    embedded_hosts = embedded_redirect_hosts(url)
    if any(
        embedded_host is None
        or not any(
            is_same_or_subdomain(embedded_host, _verified_link_host(link))
            for link in matching_links
        )
        for embedded_host in embedded_hosts
    ):
        return _assessment(
            url=url,
            project=project,
            now=now,
            state=ActionLinkSafetyState.QUARANTINED,
            reason="embedded_redirect_target",
            evidence_ids=_evidence_ids(matching_links),
        )

    contract_address = _first_contract_address(url)
    if contract_address is not None and contract_address.lower() not in {
        address.lower() for address in known_contract_addresses
    }:
        return _assessment(
            url=url,
            project=project,
            now=now,
            state=ActionLinkSafetyState.QUARANTINED,
            reason="unexpected_contract",
            contract_address=contract_address,
            evidence_ids=_evidence_ids(matching_links),
        )

    return _assessment(
        url=url,
        project=project,
        now=now,
        state=ActionLinkSafetyState.CONSISTENT,
        contract_address=contract_address.lower() if contract_address else None,
        evidence_ids=_evidence_ids(matching_links),
    )


def _assessment(
    *,
    url: str,
    project: Project,
    now: datetime,
    state: ActionLinkSafetyState,
    reason: str | None = None,
    contract_address: str | None = None,
    evidence_ids: tuple[str, ...] = (),
) -> ActionLinkAssessment:
    return ActionLinkAssessment(
        url=url,
        safety_state=state,
        checked_at=now,
        project_id=project.id,
        contract_address=contract_address,
        evidence_ids=evidence_ids,
        reason=reason,
    )


def _iter_links_by_state(
    project: Project,
    states: set[VerifiedLinkVerificationState],
) -> tuple[VerifiedLink, ...]:
    links: list[VerifiedLink] = []
    for relation_links in project.official_links.values():
        for link in relation_links:
            if link.verification_state in states:
                links.append(link)
    return tuple(links)


def _verified_link_host(link: VerifiedLink) -> str:
    try:
        return normalize_host(link.url)
    except UrlSafetyError:
        return link.normalized_host.strip().rstrip(".").lower()


def _same_url_or_path(url: str, candidate_host: str, link: VerifiedLink) -> bool:
    link_host = _verified_link_host(link)
    if candidate_host != link_host:
        return False
    try:
        candidate = urlparse(url)
        known = urlparse(link.url)
    except ValueError:
        return False
    return _normalized_path(candidate.path) == _normalized_path(known.path)


def _normalized_path(path: str) -> str:
    normalized = path or "/"
    if len(normalized) > 1:
        normalized = normalized.rstrip("/")
    return normalized


def _first_contract_address(url: str) -> str | None:
    match = _EVM_ADDRESS_RE.search(url)
    return match.group(0) if match else None


def _evidence_ids(links: tuple[VerifiedLink, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for link in links:
        for evidence_id in link.evidence_ids:
            if evidence_id not in seen:
                seen.add(evidence_id)
                ordered.append(evidence_id)
    return tuple(ordered)
