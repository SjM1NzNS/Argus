#!/usr/bin/env python3
"""Shared strict public-IP policy for Argus acquisition and browser egress."""
from __future__ import annotations

import ipaddress
from urllib.parse import urlsplit, urlunsplit

IPAddress = ipaddress.IPv4Address | ipaddress.IPv6Address
NAT64_WELL_KNOWN = ipaddress.ip_network("64:ff9b::/96")
NAT64_LOCAL_USE = ipaddress.ip_network("64:ff9b:1::/48")


def validate_loopback_http_proxy_url(value: str) -> str:
    """Normalize a credential-free loopback HTTP proxy URL or fail closed."""
    try:
        parts = urlsplit((value or "").strip())
        host = parts.hostname
        port = parts.port
    except (TypeError, ValueError) as error:
        raise ValueError("proxy must be a credential-free loopback HTTP proxy") from error
    if (
        parts.scheme.lower() != "http"
        or host not in {"127.0.0.1", "::1"}
        or port is None
        or not 1 <= port <= 65_535
        or parts.username is not None
        or parts.password is not None
        or parts.path not in {"", "/"}
        or parts.query
        or parts.fragment
    ):
        raise ValueError("proxy must be a credential-free loopback HTTP proxy")
    rendered_host = f"[{host}]" if ":" in host else host
    return urlunsplit(("http", f"{rendered_host}:{port}", "", "", ""))


def _embedded_nat64_ipv4(address: ipaddress.IPv6Address) -> ipaddress.IPv4Address | None:
    if address in NAT64_WELL_KNOWN:
        return ipaddress.IPv4Address(int(address) & 0xFFFFFFFF)
    return None


def is_strict_public_ip(value: str | IPAddress) -> bool:
    """Return true only for ordinary globally routable unicast addresses.

    ``ipaddress.is_global`` alone is intentionally insufficient: Python classifies
    multicast, deprecated IPv6 site-local, and some transition addresses as global.
    Transition mechanisms that can encode a non-public IPv4 destination are also
    rejected or recursively validated.
    """
    try:
        address = value if isinstance(value, (ipaddress.IPv4Address, ipaddress.IPv6Address)) else ipaddress.ip_address(value)
    except ValueError:
        return False

    if (
        not address.is_global
        or address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_unspecified
        or address.is_reserved
    ):
        return False

    if isinstance(address, ipaddress.IPv6Address):
        if address.is_site_local or address in NAT64_LOCAL_USE:
            return False
        if address.ipv4_mapped is not None:
            return is_strict_public_ip(address.ipv4_mapped)
        embedded = _embedded_nat64_ipv4(address)
        if embedded is not None:
            return is_strict_public_ip(embedded)
        # These transition forms are unnecessary for the browser-learning lane and
        # can obscure the ultimate IPv4 destination from policy enforcement.
        if address.sixtofour is not None or address.teredo is not None:
            return False

    return True
