#!/usr/bin/env python3
"""Parse an already-acquired OpenAPI/Swagger document into a local inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

VERSION = "1.0.0"
METHODS = ("get", "post", "put", "patch", "delete", "options", "head", "trace")


def load_document(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        return json.loads(text), "json"
    except json.JSONDecodeError:
        try:
            import yaml  # optional, never installed by this script
        except ImportError as exc:
            raise ValueError("input is not JSON and PyYAML is not installed") from exc
        data = yaml.safe_load(text)
        return data, "yaml"


def ref_or_type(schema):
    if not isinstance(schema, dict):
        return None
    if "$ref" in schema:
        return {"ref": schema["$ref"]}
    out = {}
    for key in ("type", "format", "nullable", "readOnly", "writeOnly"):
        if key in schema:
            out[key] = schema[key]
    if "items" in schema:
        out["items"] = ref_or_type(schema["items"])
    if "oneOf" in schema:
        out["oneOf"] = [ref_or_type(x) for x in schema["oneOf"]]
    if "anyOf" in schema:
        out["anyOf"] = [ref_or_type(x) for x in schema["anyOf"]]
    if "allOf" in schema:
        out["allOf"] = [ref_or_type(x) for x in schema["allOf"]]
    return out or None


def parameters(path_item, operation):
    merged = []
    for source in (path_item.get("parameters", []), operation.get("parameters", [])):
        if not isinstance(source, list):
            continue
        for param in source:
            if not isinstance(param, dict):
                continue
            if "$ref" in param:
                merged.append({"ref": param["$ref"]})
                continue
            merged.append({
                "name": param.get("name"),
                "in": param.get("in"),
                "required": bool(param.get("required", False)),
                "schema": ref_or_type(param.get("schema", {})),
            })
    return merged


def request_body(operation):
    body = operation.get("requestBody")
    if not isinstance(body, dict):
        return None
    if "$ref" in body:
        return {"ref": body["$ref"]}
    content = body.get("content", {})
    media = []
    if isinstance(content, dict):
        for content_type, item in sorted(content.items()):
            item = item if isinstance(item, dict) else {}
            media.append({"content_type": content_type, "schema": ref_or_type(item.get("schema", {}))})
    return {"required": bool(body.get("required", False)), "media": media}


def responses(operation):
    out = []
    source = operation.get("responses", {})
    if not isinstance(source, dict):
        return out
    for status_code, response in sorted(source.items(), key=lambda x: str(x[0])):
        response = response if isinstance(response, dict) else {}
        record = {"status": str(status_code)}
        if "$ref" in response:
            record["ref"] = response["$ref"]
        content = response.get("content", {})
        media = []
        if isinstance(content, dict):
            for content_type, item in sorted(content.items()):
                item = item if isinstance(item, dict) else {}
                media.append({"content_type": content_type, "schema": ref_or_type(item.get("schema", {}))})
        if media:
            record["media"] = media
        out.append(record)
    return out


def security_schemes(document):
    if not isinstance(document, dict):
        return {}
    components = document.get("components", {})
    if isinstance(components, dict) and isinstance(components.get("securitySchemes"), dict):
        return components["securitySchemes"]
    definitions = document.get("securityDefinitions", {})
    return definitions if isinstance(definitions, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    source = args.input.expanduser().resolve()
    if not source.is_file() or source.is_symlink():
        parser.error("input must be an existing non-symlink file")
    raw = source.read_bytes()
    try:
        document, input_format = load_document(source)
    except (ValueError, Exception) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not isinstance(document, dict):
        print("ERROR: specification root must be an object", file=sys.stderr)
        return 2
    paths = document.get("paths")
    if not isinstance(paths, dict):
        print("ERROR: specification has no object-valued paths field", file=sys.stderr)
        return 2

    operations = []
    for path_name, path_item in sorted(paths.items()):
        if not isinstance(path_item, dict):
            continue
        for method in METHODS:
            operation = path_item.get(method)
            if not isinstance(operation, dict):
                continue
            operations.append({
                "method": method.upper(),
                "path": path_name,
                "operation_id": operation.get("operationId"),
                "tags": operation.get("tags", []),
                "deprecated": bool(operation.get("deprecated", False)),
                "security": operation.get("security", document.get("security", [])),
                "parameters": parameters(path_item, operation),
                "request_body": request_body(operation),
                "responses": responses(operation),
            })

    inventory = {
        "schema_version": 1,
        "tool": "extract_openapi_inventory.py",
        "tool_version": VERSION,
        "network_performed": False,
        "source": {
            "path": str(source),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "format": input_format,
        },
        "specification": {
            "openapi": document.get("openapi"),
            "swagger": document.get("swagger"),
            "title": document.get("info", {}).get("title") if isinstance(document.get("info"), dict) else None,
            "version": document.get("info", {}).get("version") if isinstance(document.get("info"), dict) else None,
            "servers": document.get("servers", []),
            "security_schemes": security_schemes(document),
        },
        "operations": operations,
        "summary": {
            "operations": len(operations),
            "methods": {method: sum(1 for op in operations if op["method"] == method) for method in sorted({op["method"] for op in operations})},
            "paths": len({op["path"] for op in operations}),
        },
        "notice": "Inventory only. Specification exposure and privileged-looking fields are not vulnerabilities without demonstrated unauthorized capability.",
    }

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(inventory, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRUSR | stat.S_IWUSR)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(payload)
    os.chmod(output, 0o600)
    print(json.dumps({"output": str(output), **inventory["summary"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
