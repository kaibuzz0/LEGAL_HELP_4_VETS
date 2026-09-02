#!/usr/bin/env python3
"""Validate production legal-dataset registration and validator discovery."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "datasets.json"
STATE_DIR = ROOT / "data" / "states"
EXCLUDED_STATE_FILES = {"schema.json", "_template.json"}
KNOWN_SUBJECT_FILES = {ROOT / "data" / "california-foreclosure.json"}
LEGACY_STATE_DATASET_IDS = {"texas-housing"}


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def production_legal_files() -> set[Path]:
    files = {p.resolve() for p in STATE_DIR.glob("*.json") if p.name not in EXCLUDED_STATE_FILES}
    files.update(p.resolve() for p in KNOWN_SUBJECT_FILES if p.exists())
    return files


def validate_registry(registry: dict) -> list[str]:
    errors: list[str] = []
    entries = registry.get("datasets", [])
    ids = [e.get("id") for e in entries]
    paths = [e.get("path") for e in entries]

    for values, label in ((ids, "dataset ID"), (paths, "dataset path")):
        duplicates = sorted({x for x in values if x and values.count(x) > 1})
        if duplicates:
            errors.append(f"duplicate {label}s: {duplicates}")

    by_id = {e.get("id"): e for e in entries if e.get("id")}
    registered_paths: set[Path] = set()

    for entry in entries:
        did = entry.get("id", "<missing-id>")
        path_value = entry.get("path")
        validator_value = entry.get("validator")
        if not path_value:
            errors.append(f"{did}: missing dataset path")
            continue
        path = (ROOT / path_value).resolve()
        registered_paths.add(path)
        if not path.exists():
            errors.append(f"{did}: registered dataset does not exist: {path_value}")
        if not validator_value:
            errors.append(f"{did}: missing semantic validator")
        elif not (ROOT / validator_value).exists():
            errors.append(f"{did}: validator does not exist: {validator_value}")
        for field in ("state", "subject", "schema_version", "status", "last_verified"):
            if not entry.get(field):
                errors.append(f"{did}: missing {field}")
        if entry.get("last_verified"):
            try:
                datetime.strptime(entry["last_verified"], "%Y-%m-%d")
            except ValueError:
                errors.append(f"{did}: malformed last_verified")

        if path_value.startswith("data/states/") and did not in LEGACY_STATE_DATASET_IDS:
            if entry.get("schema_version") != "1.2":
                errors.append(f"{did}: new/current state datasets must use schema 1.2; Texas is the only 1.1 legacy exception")
            if path.exists():
                try:
                    actual = json.loads(path.read_text(encoding="utf-8")).get("schema_version")
                except json.JSONDecodeError:
                    actual = None
                if actual != "1.2":
                    errors.append(f"{did}: registered current state file does not declare schema 1.2")

        for dep in entry.get("cross_dataset_dependencies", []):
            if dep not in by_id:
                errors.append(f"{did}: unknown dataset dependency {dep!r}")

    missing = sorted(str(p.relative_to(ROOT)) for p in production_legal_files() - registered_paths)
    if missing:
        errors.append(f"production legal datasets are not registered: {missing}")

    return errors


def main() -> int:
    errors = validate_registry(load_registry())
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: production legal dataset registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
