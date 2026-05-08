#!/usr/bin/env python3
"""Stdlib-only orchestrator for QIRA Phase 3 local static checks."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "factory_acceleration" / "phase_3_ci" / "PHASE_3_LOCAL_STATIC_CHECK_RECEIPT_v1.md"
SCRIPTS = [
    "tools/ci/qira_artifact_integrity_check.py",
    "tools/ci/qira_json_semantic_check.py",
    "tools/ci/qira_claim_boundary_scan.py",
    "tools/ci/qira_secret_surface_scan.py",
]
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_script(rel: str) -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", str(ROOT / rel), "--json"],
        cwd=str(ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    parsed = None
    if proc.stdout.strip():
        parsed = json.loads(proc.stdout)
    return {
        "script": rel,
        "exit_code": proc.returncode,
        "stdout_json": parsed,
        "stderr_size": len(proc.stderr.encode("utf-8")),
    }


def workflow_dormant(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "push_trigger_present": "push:" in lowered,
        "pull_request_trigger_present": "pull_request:" in lowered,
        "schedule_trigger_present": "schedule:" in lowered,
        "workflow_run_trigger_present": "workflow_run:" in lowered,
        "disabled_gate_present": "if: ${{ false }}" in text,
        "manual_dispatch_present": "workflow_dispatch:" in text,
    }


def main() -> int:
    script_results = [run_script(rel) for rel in SCRIPTS]
    file_register = []
    for rel in ALLOWLIST:
        path = ROOT / rel
        raw = path.read_bytes()
        raw.decode("utf-8")
        file_register.append({"path": rel, "size_bytes": len(raw), "sha256": sha256(path)})
    workflow_results = [
        workflow_dormant(ROOT / ".github/workflows/qira-governance-static.yml"),
        workflow_dormant(ROOT / ".github/workflows/qira-python-quality-candidate.yml"),
    ]
    pass_status = all(item["exit_code"] == 0 for item in script_results)
    pass_status = pass_status and all(not item["push_trigger_present"] and not item["pull_request_trigger_present"] for item in workflow_results)
    receipt = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_WITH_LIMITS" if pass_status else "FAIL",
        "proof_ceiling": "PHASE_3_CI_QUALITY_LOOP_CANDIDATE_CREATED_AND_LOCAL_STATIC_SELF_VERIFIED_WITH_LIMITS_NO_REMOTE_CI_RUN_NO_INSTALL_NO_TESTS_NO_VALIDATION_NO_READINESS_PROOF",
        "self_verifier_proof_limit": "LOCAL_STATIC_SELF_VERIFIER_NOT_INDEPENDENT_PROOF",
        "yaml_syntax_validity": "NOT_PROVEN",
        "github_parser_acceptance": "NOT_PROVEN",
        "remote_ci_execution": "NOT_PROVEN",
        "untracked_safe_preflight": "NO_UNRELATED_UNTRACKED_PATH_NAMES_EMITTED_BY_RUNNER",
        "scripts": script_results,
        "files": file_register,
        "workflows": workflow_results,
        "claims_not_proven": [
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
        ],
    }
    text = "# QIRA Phase 3 Local Static Check Receipt\n\n"
    text += "```json\n"
    text += json.dumps(receipt, indent=2, sort_keys=True)
    text += "\n```\n"
    RECEIPT.write_text(text, encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "receipt": RECEIPT.relative_to(ROOT).as_posix()}, sort_keys=True))
    return 0 if pass_status else 1


if __name__ == "__main__":
    sys.exit(main())

