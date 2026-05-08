#!/usr/bin/env python3
"""Stdlib-only conservative secret-surface scanner for exact QIRA Phase 3 artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST = [
    ".github/workflows/qira-governance-static.yml",
    ".github/workflows/qira-python-quality-candidate.yml",
    "tools/ci/README.md",
    "tools/ci/qira_ci_local_static_runner.py",
    "tools/ci/qira_claim_boundary_scan.py",
    "tools/ci/qira_secret_surface_scan.py",
    "tools/ci/qira_json_semantic_check.py",
    "tools/ci/qira_artifact_integrity_check.py",
    "factory_acceleration/phase_3_ci/README.md",
    "factory_acceleration/phase_3_ci/PHASE_3_CI_QUALITY_LOOP_REGISTER_v1.json",
    "factory_acceleration/phase_3_ci/CI_TOOL_ADOPTION_BOUNDARY_v1.md",
    "factory_acceleration/phase_3_ci/NEXT_ROUTE_AFTER_PHASE_3_CI_v1.md",
    "factory_acceleration/phase_3_ci/PHASE_3_LOCAL_STATIC_CHECK_RECEIPT_v1.md",
]

OLD_ROOT_PATTERN = re.escape("C:" + "\\" + "cog-ci" + "\\" + "CAF-Release")
PATTERNS = {
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "token_assignment": r"(?i)\b(?:token|api[_-]?key|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",
    "env_file_reference": "(?i)" + re.escape("." + "env") + r"\b",
    "old_root": OLD_ROOT_PATTERN,
}


def scan_file(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    hits = {name: len(re.findall(pattern, text)) for name, pattern in PATTERNS.items()}
    total = sum(hits.values())
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "hit_classes": {key: value for key, value in hits.items() if value},
        "status": "PASS" if total == 0 else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = [scan_file(ROOT / rel) for rel in ALLOWLIST]
    status = "PASS" if all(item["status"] == "PASS" for item in results) else "FAIL"
    payload = {"check": "secret_surface_scan", "status": status, "results": results}
    print(json.dumps(payload, indent=2 if not args.json else None, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
