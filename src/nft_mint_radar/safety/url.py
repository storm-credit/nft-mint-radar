"""Pure URL normalization primitives for wallet-impacting CTA checks."""

from __future__ import annotations

import ipaddress
import re
import unicodedata
from urllib.parse import unquote, urlparse


class UrlSafetyError(ValueError):
    """Raised when a URL cannot pass deterministic safety normalization."""

    def __init__(self, reason: str, message: str | None = None) -> None:
        self.reason = reason
        super().__init__(message or reason)


_SCRIPT_MARKERS = (
    "LATIN",
    "GREEK",
    "CYRILLIC",
    "HEBREW",
    "ARABIC",
    "DEVANAGARI",
    "HIRAGANA",
    "KATAKANA",
    "HANGUL",
)
_ABSOLUTE_URL_RE = re.compile(
    r"(?i)\b[a-z][a-z0-9+.-]*://[^\s\"'<>\\]+"
)
_PROTOCOL_RELATIVE_URL_RE = re.compile(r"(?<![:/])//[^\s\"'<>\\]+")
_MALFORMED_SCHEME_RELATIVE_RE = re.compile(r"(?<![a-z0-9+.-])://[^\s\"'<>\\]+", re.I)


def normalize_host(url: str) -> str:
    """Return the lowercased IDNA-normalized host, or raise UrlSafetyError."""

    if not isinstance(url, str) or not url.strip():
        raise UrlSafetyError("unparseable_url")

    try:
        parsed = urlparse(url)
    except ValueError as exc:
        raise UrlSafetyError("unparseable_url") from exc

    if parsed.scheme.lower() != "https":
        raise UrlSafetyError("bad_scheme")
    if parsed.username is not None or parsed.password is not None:
        raise UrlSafetyError("userinfo")

    try:
        raw_host = parsed.hostname
    except ValueError as exc:
        raise UrlSafetyError("unparseable_url") from exc

    if raw_host is None or not raw_host.strip():
        raise UrlSafetyError("missing_host")

    host = raw_host.strip().rstrip(".").lower()
    if not host or ".." in host:
        raise UrlSafetyError("invalid_host")

    _reject_ip_literal(host)
    return _idna_normalize_host(host)


def embedded_redirect_hosts(url: str) -> tuple[str | None, ...]:
    """Return embedded destination hosts in query/fragment, or None for unsafe parse failures."""

    try:
        parsed = urlparse(url)
    except ValueError:
        return (None,)

    embedded_hosts: list[str | None] = []
    for component in (parsed.query, parsed.fragment):
        decoded = _decode_until_stable(component)
        embedded_hosts.extend(_extract_embedded_hosts(decoded))
    return tuple(embedded_hosts)


def has_path_traversal(url: str) -> bool:
    """Return True when the URL path contains literal or encoded '..' segments."""

    try:
        parsed = urlparse(url)
    except ValueError:
        return False

    decoded_path = _decode_until_stable(parsed.path).replace("\\", "/")
    return any(segment == ".." for segment in decoded_path.split("/"))


def is_same_or_subdomain(candidate_host: str, verified_host: str) -> bool:
    """Return True for exact host matches or real label subdomains only."""

    candidate_labels = _host_labels(candidate_host)
    verified_labels = _host_labels(verified_host)
    if not candidate_labels or not verified_labels:
        return False
    if candidate_labels == verified_labels:
        return True
    if len(candidate_labels) <= len(verified_labels):
        return False
    return candidate_labels[-len(verified_labels) :] == verified_labels


def _decode_until_stable(value: str) -> str:
    decoded = value
    while True:
        next_decoded = unquote(decoded)
        if next_decoded == decoded:
            return decoded
        decoded = next_decoded


def _extract_embedded_hosts(value: str) -> tuple[str | None, ...]:
    hosts: list[str | None] = []

    for match in _ABSOLUTE_URL_RE.finditer(value):
        hosts.append(_embedded_host(match.group(0)))

    for match in _PROTOCOL_RELATIVE_URL_RE.finditer(value):
        hosts.append(_embedded_host(f"https:{match.group(0)}"))

    if _MALFORMED_SCHEME_RELATIVE_RE.search(value):
        hosts.append(None)

    return tuple(hosts)


def _embedded_host(target_url: str) -> str | None:
    try:
        return normalize_host(target_url)
    except UrlSafetyError:
        return None


def _reject_ip_literal(host: str) -> None:
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return
    raise UrlSafetyError("ip_literal")


def _idna_normalize_host(host: str) -> str:
    try:
        ascii_host = host.encode("idna").decode("ascii").lower()
        decoded_host = ascii_host.encode("ascii").decode("idna").lower()
        roundtrip_host = decoded_host.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise UrlSafetyError("invalid_idna") from exc

    if not ascii_host or ascii_host != roundtrip_host:
        raise UrlSafetyError("idna_roundtrip_mismatch")

    # Fullwidth and other compatibility lookalikes must not silently normalize.
    if not _is_ascii(host) and decoded_host != host:
        raise UrlSafetyError("idna_roundtrip_mismatch")

    if _has_invalid_ascii_host_syntax(ascii_host):
        raise UrlSafetyError("invalid_host")
    if _contains_mixed_script(decoded_host):
        raise UrlSafetyError("mixed_script_confusable")
    return ascii_host


def _has_invalid_ascii_host_syntax(host: str) -> bool:
    for label in host.split("."):
        if not label:
            return True
        if label.startswith("-") or label.endswith("-"):
            return True
        if not all(char.isascii() and (char.isalnum() or char == "-") for char in label):
            return True
    return False


def _contains_mixed_script(host: str) -> bool:
    scripts = {
        script
        for char in host
        if (script := _unicode_script(char)) is not None
    }
    return len(scripts) > 1


def _unicode_script(char: str) -> str | None:
    if char in ".-" or char.isdigit():
        return None
    name = unicodedata.name(char, "")
    for marker in _SCRIPT_MARKERS:
        if marker in name:
            return marker
    if char.isalpha():
        return "OTHER"
    return None


def _host_labels(host: str) -> tuple[str, ...]:
    normalized = host.strip().rstrip(".").lower()
    if not normalized:
        return ()
    return tuple(label for label in normalized.split(".") if label)


def _is_ascii(value: str) -> bool:
    return all(ord(char) < 128 for char in value)
