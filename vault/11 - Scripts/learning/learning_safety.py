#!/usr/bin/env python3
"""Conservative staging-scope guard for Argus learning candidates.

This is intentionally a review gate, not a semantic trust engine. It only diverts
material that explicitly advertises operational abuse workflows. Defensive analysis,
mitigation, detection, reporting, and authorized validation remain staged normally.
"""
from __future__ import annotations

import re

DEFENSIVE = re.compile(
    r"\b(detect(?:ion)?|defen[cs]e|mitigat(?:e|ion)|prevent(?:ion)?|awareness|training|report(?:ing)?|"
    r"incident response|threat intelligence|authorized|safe proof|false positive|remediation)\b",
    re.I,
)
ABUSE_WORKFLOW = re.compile(
    r"\b(turnkey|ready[- ]to[- ]use|step[- ]by[- ]step|operator(?:'s)? guide|payload pack|builder|kit)\b.{0,80}"
    r"\b(phish(?:ing)?|credential harvester|credential theft|keylogger|c2|command and control|persistence|ransomware|destructive|post[- ]exploitation)\b|"
    r"\b(phish(?:ing)? kit|credential harvester|c2 infrastructure setup|persistence payload pack|ransomware builder)\b",
    re.I | re.S,
)


def scope_disposition(text: str) -> str:
    value = text or ""
    if ABUSE_WORKFLOW.search(value) and not DEFENSIVE.search(value):
        return "scope_review_required"
    return "staged_untrusted"
