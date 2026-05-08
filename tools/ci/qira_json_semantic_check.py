#!/usr/bin/env python3
"""Stdlib-only JSON semantic checker with duplicate-key detection."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
JSON_ALLOWLIST = [
    "factory_acceleration/phase_3_ci/PHASE_3_CI_QUALITY_LOOP_REGISTER_v1.json",
]


class DuplicateKeyError(ValueError):
    pass


def object_pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise DuplicateKeyError(key)
        seen.add(key)
        out[key] = value
    return out


def check_json(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    try:
        data = json.loads(text, object_pairs_hook=object_pairs_no_duplicates)
        canonical = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return {
            "path": path.relative_to(ROOT).as_posix(),
            "parse_status": "PASS",
            "duplicate_keys_detected": "NO",
            "canonical_json_semantic_sha256": hashlib.sha256(canonical).hexdigest(),
            "status": "PASS",
        }
    except DuplicateKeyError as exc:
        return {
            "path": path.relative_to(ROOT).as_posix(),
            "parse_status": "FAIL",
            "duplicate_keys_detected": f"YES:{exc}",
            "status": "FAIL",
        }
    except Exception as exc:
        return {
            "path": path.relative_to(ROOT).as_posix(),
            "parse_status": f"FAIL:{type(exc).__name__}",
            "duplicate_keys_detected": "UNKNOWN",
            "status": "FAIL",
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = [check_json(ROOT / rel) for rel in JSON_ALLOWLIST]
    status = "PASS" if all(item["status"] == "PASS" for item in results) else "FAIL"
    payload = {"check": "json_semantic_check", "status": status, "results": results}
    print(json.dumps(payload, indent=2 if not args.json else None, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

