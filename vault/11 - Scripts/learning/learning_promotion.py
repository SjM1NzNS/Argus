#!/usr/bin/env python3
"""Explicit knowledge-class and promotion gates for Argus learning proposals."""
from __future__ import annotations

import re


KNOWLEDGE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("vulnerability_pattern", re.compile(r"\b(vulnerab|bypass|exploit|authorization|injection|reentr|ssrf|xss|idor|bola|race condition)\b", re.I)),
    ("validation_technique", re.compile(r"\b(validat|verify|replay|proof|poc|control|test case|reproduce)\b", re.I)),
    ("architecture_trust_boundary", re.compile(r"\b(trust[- ]boundary|architecture|boundary mismatch|confused deputy|identity binding|control plane|data plane)\b", re.I)),
    ("false_positive_condition", re.compile(r"\b(false positive|not exploitable|reject|downgrade|same tenant|intended behavior|precondition)\b", re.I)),
    ("evidence_requirement", re.compile(r"\b(evidence|capture|artifact|response|request|log|trace|quantif|demonstrat)\b", re.I)),
    ("reportability_criterion", re.compile(r"\b(reportab|severity|triage|impact|bounty|out[- ]of[- ]scope|duplicate)\b", re.I)),
    ("hunting_methodology", re.compile(r"\b(hunt|workflow|methodology|recon|source[- ]first|hypothesis|triage process)\b", re.I)),
    ("tooling_procedure", re.compile(r"\b(tooling|tool|parser|compiler|script|automation|procedure|instrumentation)\b", re.I)),
)


def classify_knowledge_types(text: str) -> list[str]:
    """Return bounded multi-label proposal classes; never a trust decision."""
    text = text or ""
    return [label for label, pattern in KNOWLEDGE_PATTERNS if pattern.search(text)]


def promotion_requirements(source: dict) -> dict:
    """Materialize review gates from categorical source policy.

    Every input remains proposal-only. Authority changes corroboration needs, not
    the requirement for a deliberate promotion review.
    """
    return {
        "promotion_status": "proposal_only",
        "manual_review_required": True,
        "original_source_resolution_required": bool(source.get("original_source_required")),
        "corroboration_required": source.get("independent_corroboration", "required"),
        "promotion_policy": source.get("promotion_policy", "proposals_only"),
        "source_role": source.get("role", "unknown"),
        "source_trust": source.get("trust", "contextual"),
    }
