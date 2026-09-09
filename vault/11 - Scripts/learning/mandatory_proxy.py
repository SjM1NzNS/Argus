#!/usr/bin/env python3
"""urllib opener that cannot bypass the Argus loopback public-egress proxy."""
from __future__ import annotations

import ssl
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import (
    BaseHandler,
    HTTPDefaultErrorHandler,
    HTTPErrorProcessor,
    HTTPHandler,
    HTTPRedirectHandler,
    HTTPSHandler,
    OpenerDirector,
    ProxyHandler,
    Request,
    UnknownHandler,
)

from network_policy import validate_loopback_http_proxy_url


class MandatoryProxyHandler(BaseHandler):
    """Force both HTTP and HTTPS through one validated HTTP proxy.

    Unlike urllib's standard ProxyHandler, this deliberately does not consult
    NO_PROXY/no_proxy. HTTPS uses CONNECT via Request.set_proxy().
    """

    handler_order = 100

    def __init__(self, proxy_url: str) -> None:
        normalized = validate_loopback_http_proxy_url(proxy_url)
        parts = urlsplit(normalized)
        host = parts.hostname or ""
        rendered_host = f"[{host}]" if ":" in host else host
        self.proxy_authority = f"{rendered_host}:{parts.port}"

    def _force(self, request):
        request.set_proxy(self.proxy_authority, "http")
        return request

    http_request = _force
    https_request = _force


class HTTPOnlyRedirectHandler(HTTPRedirectHandler):
    """Reject redirects to schemes that are outside the mandatory proxy lane."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).scheme.lower() not in {"http", "https"}:
            raise HTTPError(req.full_url, code, "redirect scheme blocked", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def build_mandatory_proxy_opener(proxy_url: str) -> OpenerDirector:
    """Build an HTTP(S)-only opener with no direct or environment fallback."""
    opener = OpenerDirector()
    for handler in (
        ProxyHandler({}),
        MandatoryProxyHandler(proxy_url),
        UnknownHandler(),
        HTTPHandler(),
        HTTPSHandler(context=ssl.create_default_context()),
        HTTPDefaultErrorHandler(),
        HTTPOnlyRedirectHandler(),
        HTTPErrorProcessor(),
    ):
        opener.add_handler(handler)
    return opener
