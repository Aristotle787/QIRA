#!/usr/bin/env python3
"""Stdlib-only claim-boundary scanner for exact QIRA Phase 3 artifacts."""

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

REQUIRED_SAFE_TOKENS = [
    "TOOLS_FULLY_INSTALLED_CLAIM = NOT_PROVEN",
    "TOOLS_FULLY_APPROVED_CLAIM = NOT_PROVEN",
    "CI_CONFIGURED_CLAIM = NOT_PROVEN",
    "REMOTE_CI_RUN_CLAIM = NOT_PROVEN",
    "GITHUB_ACTIONS_PARSER_ACCEPTANCE_CLAIM = NOT_PROVEN",
    "TESTS_PASS_CLAIM = NOT_PROVEN",
    "VALIDATION_READINESS_CLAIM = NOT_PROVEN",
    "DD_READINESS_CLAIM = NOT_PROVEN",
    "SALE_READINESS_CLAIM = NOT_PROVEN",
    "VALUATION_SUPPORT_CLAIM = NOT_PROVEN",
    "TARGET_TRANSACTION_OBJECTIVE_15M_SUPPORT_CLAIM = NOT_PROVEN",
]

FORBIDDEN_POSITIVE_PATTERNS = [
    r"\bCI " + r"configured\b",
    r"\bremote CI (?:ran|passed|succeeded)\b",
    r"\btests " + r"pass\b",
    r"\bvalidation " + r"ready\b",
    r"\bDD " + r"ready\b",
    r"\bsale " + r"ready\b",
    r"\bvaluation " + r"supported\b",
    r"\b15M " + r"supported\b",
    r"\bEV correctness (?:proven|validated)\b",
    r"\bproduction " + r"ready\b",
]


def scan_file(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    positives = []
    for line in text.splitlines():
        stripped = line.strip()
        if "NOT_PROVEN" in stripped or stripped.lower().startswith(("- no ", "no ")):
            continue
        for pattern in FORBIDDEN_POSITIVE_PATTERNS:
            if re.search(pattern, stripped, flags=re.IGNORECASE):
                positives.append(pattern)
    safe_hits = [token for token in REQUIRED_SAFE_TOKENS if token in text]
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "forbidden_positive_patterns": positives,
        "safe_token_count": len(safe_hits),
        "status": "PASS" if not positives else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = [scan_file(ROOT / rel) for rel in ALLOWLIST]
    status = "PASS" if all(item["status"] == "PASS" for item in results) else "FAIL"
    payload = {"check": "claim_boundary_scan", "status": status, "results": results}
    print(json.dumps(payload, indent=2 if not args.json else None, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
