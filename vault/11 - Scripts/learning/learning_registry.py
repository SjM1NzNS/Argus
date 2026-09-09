#!/usr/bin/env python3
"""Configuration-driven source registry for Argus learning ingestion.

The registry is intentionally categorical: source role/trust/promotion semantics
are explicit, while ingestion still produces proposals rather than trusted facts.
"""
from __future__ import annotations

import hashlib
import ipaddress
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit

import yaml

from learning_state import canonical_url


ALLOWED_ROLES = {
    "authority",
    "primary_research",
    "discovery_index",
    "report_repository",
    "practitioner_commentary",
    "watchlist",
    "foundational_reference",
}
ALLOWED_DOMAINS = {"web2", "web3", "ai_security", "platform_specific", "cross_domain", "other"}
ALLOWED_ACQUISITION = {
    "static",
    "browser_dom",
    "deep_link_discovery",
    "feed",
    "repository",
    "single_page",
    "transcript",
}
ALLOWED_CADENCES = {"daily", "weekly", "periodic", "on_demand"}
ALLOWED_TRUST = {"authority", "primary", "curated_secondary", "discovery_only", "contextual"}
ALLOWED_PROMOTION_POLICIES = {
    "review_required",
    "corroboration_required",
    "original_source_required",
    "proposals_only",
    "context_only",
}
ALLOWED_CORROBORATION = {"required", "conditional", "not_required"}
REQUIRED_FIELDS = {
    "id",
    "name",
    "url",
    "type",
    "priority",
    "role",
    "domain",
    "acquisition",
    "cadence",
    "trust",
    "promotion_policy",
    "original_source_required",
    "independent_corroboration",
    "refetch_interval_days",
    "expected_content_type",
}
NON_SOURCE_KEYS = {"registry", "source_group_policies", "appsec_fyi_discovery_rule"}


class RegistryValidationError(ValueError):
    """Raised when source policy is incomplete or contradictory."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silent duplicate-key overrides."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise RegistryValidationError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


@dataclass(frozen=True)
class LearningRegistry:
    path: Path
    schema_version: int
    metadata: dict
    group_policies: dict[str, dict]
    sources: tuple[dict, ...]
    discovery_rules: dict
    digest: str


def _stable_digest(metadata: dict, group_policies: dict, sources: list[dict], discovery_rules: dict) -> str:
    payload = {
        "metadata": metadata,
        "group_policies": group_policies,
        "sources": sorted(sources, key=lambda s: s["id"]),
        "discovery_rules": discovery_rules,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_source(source: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(k for k in REQUIRED_FIELDS if k not in source or source[k] is None or source[k] == "")
    label = source.get("id") if isinstance(source.get("id"), str) else source.get("name")
    label = label if isinstance(label, str) and label else "<unnamed>"
    if missing:
        errors.append(f"{label}: missing {', '.join(missing)}")
        return errors
    sensitive_keys = sorted(key for key in source if re.search(r"(?:api[_-]?key|authorization|password|secret|token|cookie|credential)", str(key), re.I))
    if sensitive_keys:
        errors.append(f"{label}: inline secret/credential fields are forbidden: {', '.join(sensitive_keys)}")

    string_fields = {
        "id", "name", "url", "type", "priority", "role", "domain", "acquisition",
        "cadence", "trust", "promotion_policy", "independent_corroboration", "expected_content_type",
    }
    for key in sorted(string_fields):
        if not isinstance(source.get(key), str):
            errors.append(f"{label}: {key} must be a string")
    if errors:
        return errors
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source["id"]):
        errors.append(f"{label}: id must be lowercase kebab-case")

    parsed = urlsplit(source["url"])
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        errors.append(f"{label}: url must be an absolute http(s) URL")
    if parsed.username or parsed.password:
        errors.append(f"{label}: url must not contain credentials")
    host = (parsed.hostname or "").lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".localhost"):
        errors.append(f"{label}: url must not target localhost")
    try:
        address = ipaddress.ip_address(host)
        if not address.is_global:
            errors.append(f"{label}: url must not target a non-public IP literal")
    except ValueError:
        pass

    enum_checks = [
        ("role", ALLOWED_ROLES),
        ("domain", ALLOWED_DOMAINS),
        ("acquisition", ALLOWED_ACQUISITION),
        ("cadence", ALLOWED_CADENCES),
        ("trust", ALLOWED_TRUST),
        ("promotion_policy", ALLOWED_PROMOTION_POLICIES),
        ("independent_corroboration", ALLOWED_CORROBORATION),
    ]
    for key, allowed in enum_checks:
        if source[key] not in allowed:
            errors.append(f"{source['id']}: invalid {key}={source[key]!r}; expected one of {sorted(allowed)}")
    if source["priority"] not in {"high", "medium", "low"}:
        errors.append(f"{source['id']}: invalid priority={source['priority']!r}")
    if not isinstance(source["original_source_required"], bool):
        errors.append(f"{source['id']}: original_source_required must be boolean")
    if not isinstance(source["refetch_interval_days"], int) or isinstance(source["refetch_interval_days"], bool):
        errors.append(f"{source['id']}: refetch_interval_days must be an integer")
    elif source["refetch_interval_days"] < 0:
        errors.append(f"{source['id']}: refetch_interval_days must be >= 0")
    if source.get("deep_link_limit") is not None:
        if not isinstance(source["deep_link_limit"], int) or isinstance(source["deep_link_limit"], bool):
            errors.append(f"{source['id']}: deep_link_limit must be an integer")
        elif source["deep_link_limit"] < 0:
            errors.append(f"{source['id']}: deep_link_limit must be >= 0")
    if source["role"] == "discovery_index":
        if source["trust"] != "discovery_only":
            errors.append(f"{source['id']}: discovery_index must use trust=discovery_only")
        if not source["original_source_required"]:
            errors.append(f"{source['id']}: discovery_index must require original-source resolution")
        if source["promotion_policy"] != "original_source_required":
            errors.append(f"{source['id']}: discovery_index must use promotion_policy=original_source_required")
    return errors


def load_registry(path: str | Path) -> LearningRegistry:
    path = Path(path).expanduser()
    try:
        raw = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader) or {}
    except RegistryValidationError:
        raise
    except yaml.YAMLError as exc:
        raise RegistryValidationError(f"invalid registry YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise RegistryValidationError("registry root must be a mapping")
    metadata = raw.get("registry") or {}
    if not isinstance(metadata, dict):
        raise RegistryValidationError("registry metadata must be a mapping")
    schema_version = metadata.get("schema_version")
    if schema_version != 2:
        raise RegistryValidationError(f"registry.schema_version must be 2, got {schema_version!r}")
    group_policies = raw.get("source_group_policies") or {}
    if not isinstance(group_policies, dict):
        raise RegistryValidationError("source_group_policies must be a mapping")

    sources: list[dict] = []
    errors: list[str] = []
    for group, items in raw.items():
        if group in NON_SOURCE_KEYS:
            continue
        if items is None:
            continue
        if not isinstance(items, list):
            errors.append(f"{group}: source group must be a list")
            continue
        defaults = group_policies.get(group) or {}
        if not isinstance(defaults, dict):
            errors.append(f"{group}: group policy must be a mapping")
            continue
        for item in items:
            if not isinstance(item, dict):
                errors.append(f"{group}: source entry must be a mapping")
                continue
            source = {**defaults, **item, "group": group}
            errors.extend(_validate_source(source))
            sources.append(source)

    ids = [str(s.get("id")) for s in sources if s.get("id")]
    names = [str(s.get("name")) for s in sources if s.get("name")]
    urls = [canonical_url(str(s.get("url"))) for s in sources if s.get("url")]
    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1})
    duplicate_names = sorted({x for x in names if names.count(x) > 1})
    duplicate_urls = sorted({x for x in urls if urls.count(x) > 1})
    if duplicate_ids:
        errors.append(f"duplicate source ids: {', '.join(duplicate_ids)}")
    if duplicate_names:
        errors.append(f"duplicate source names: {', '.join(duplicate_names)}")
    if duplicate_urls:
        errors.append(f"duplicate source urls: {', '.join(duplicate_urls)}")
    if not sources:
        errors.append("registry contains no sources")
    if errors:
        raise RegistryValidationError("; ".join(errors))

    discovery_rules = raw.get("appsec_fyi_discovery_rule") or {}
    digest = _stable_digest(metadata, group_policies, sources, discovery_rules)
    return LearningRegistry(
        path=path,
        schema_version=schema_version,
        metadata=metadata,
        group_policies=group_policies,
        sources=tuple(sources),
        discovery_rules=discovery_rules,
        digest=digest,
    )


def select_sources(
    registry: LearningRegistry,
    *,
    cadence: str,
    lane: str | None = None,
    source_ids: set[str] | None = None,
    priorities: set[str] | None = None,
) -> list[dict]:
    cadence_map = {
        "daily": {"daily"},
        "weekly": {"daily", "weekly"},
        "periodic": {"periodic"},
        "backfill": {"periodic", "on_demand"},
        "on_demand": {"on_demand"},
        "all": ALLOWED_CADENCES,
    }
    if cadence not in cadence_map:
        raise RegistryValidationError(f"unknown selection cadence {cadence!r}")
    if lane not in {None, "static", "browser_dom"}:
        raise RegistryValidationError(f"unknown acquisition lane {lane!r}")
    known = {s["id"] for s in registry.sources}
    if source_ids is not None:
        unknown = sorted(source_ids - known)
        if unknown:
            raise RegistryValidationError(f"unknown source ids: {', '.join(unknown)}")

    selected: list[dict] = []
    for source in registry.sources:
        exact_targeted_backfill = cadence == "backfill" and source_ids is not None
        if not exact_targeted_backfill and source["cadence"] not in cadence_map[cadence]:
            continue
        if source_ids is not None and source["id"] not in source_ids:
            continue
        if priorities and source["priority"] not in priorities:
            continue
        if lane == "browser_dom" and source["acquisition"] != "browser_dom":
            continue
        if lane == "static" and source["acquisition"] == "browser_dom":
            continue
        selected.append(dict(source))
    return selected


def provenance_fields(
    registry: LearningRegistry,
    source: dict,
    *,
    run_cadence: str,
    record_kind: str,
    run_id: str | None = None,
) -> dict:
    fields = {
        "source_id": source["id"],
        "source_role": source["role"],
        "source_domain": source["domain"],
        "source_acquisition": source["acquisition"],
        "source_cadence": source["cadence"],
        "source_trust": source["trust"],
        "source_quality_default": {"authority": 10, "primary": 9, "curated_secondary": 7, "discovery_only": 4, "contextual": 5}[source["trust"]],
        "promotion_policy": source["promotion_policy"],
        "original_source_required": source["original_source_required"],
        "independent_corroboration": source["independent_corroboration"],
        "refetch_interval_days": int(source["refetch_interval_days"]),
        "expected_content_type": source["expected_content_type"],
        "run_cadence": run_cadence,
        "record_kind": record_kind,
        "registry_schema_version": registry.schema_version,
        "registry_digest": registry.digest,
    }
    if run_id:
        fields["run_id"] = run_id
    return fields


def grouped_sources(registry: LearningRegistry, sources: Iterable[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for source in sources:
        grouped.setdefault(source["group"], []).append(source)
    return grouped
