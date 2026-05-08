#!/usr/bin/env python3
"""Stdlib-only exact artifact integrity checker for QIRA Phase 3."""

from __future__ import annotations

import argparse
import hashlib
import json
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

TOOLS_CI_EXPECTED = {
    "README.md",
    "qira_ci_local_static_runner.py",
    "qira_claim_boundary_scan.py",
    "qira_secret_surface_scan.py",
    "qira_json_semantic_check.py",
    "qira_artifact_integrity_check.py",
}
PHASE_3_EXPECTED = {
    "README.md",
    "PHASE_3_CI_QUALITY_LOOP_REGISTER_v1.json",
    "CI_TOOL_ADOPTION_BOUNDARY_v1.md",
    "NEXT_ROUTE_AFTER_PHASE_3_CI_v1.md",
    "PHASE_3_LOCAL_STATIC_CHECK_RECEIPT_v1.md",
}
WORKFLOW_EXPECTED = {
    "qira-governance-static.yml",
    "qira-python-quality-candidate.yml",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def root_names(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {item.name for item in path.iterdir()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    files = []
    missing = []
    for rel in ALLOWLIST:
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        raw = path.read_bytes()
        raw.decode("utf-8")
        files.append({"path": rel, "size_bytes": len(raw), "sha256": sha256(path)})
    checks = {
        "missing": missing,
        "tools_ci_exact": root_names(ROOT / "tools" / "ci") == TOOLS_CI_EXPECTED,
        "phase_3_exact": root_names(ROOT / "factory_acceleration" / "phase_3_ci") == PHASE_3_EXPECTED,
        "target_workflows_present": WORKFLOW_EXPECTED.issubset(root_names(ROOT / ".github" / "workflows")),
    }
    status = "PASS" if not missing and all(checks[key] for key in ["tools_ci_exact", "phase_3_exact", "target_workflows_present"]) else "FAIL"
    payload = {"check": "artifact_integrity_check", "status": status, "checks": checks, "files": files}
    print(json.dumps(payload, indent=2 if not args.json else None, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

