from __future__ import annotations

import hashlib
import json
from typing import Any

C05_HASH_LINEAGE_CONTRACT_VERSION = "v1"
C05_HASH_LINEAGE_CONTRACT_SHA256 = "7D109EB2024EE505A0DBAE5C75DFE8F8499DD15D066FCECBEB3361EF0F6DA16B"


def canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_payload(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def canonical_sha256_payload(payload: Any) -> str:
    return sha256_payload(payload).upper()


def c05_contract_reference() -> dict[str, str]:
    return {
        "c05_hash_lineage_contract_version": C05_HASH_LINEAGE_CONTRACT_VERSION,
        "c05_hash_lineage_contract_sha256": C05_HASH_LINEAGE_CONTRACT_SHA256,
    }


def make_run_id(input_payload: dict[str, Any], config: dict[str, Any]) -> str:
    return "QIRA-WAVE01-" + sha256_payload({"input": input_payload, "config": config})[:16].upper()


def make_trace_receipt(
    run_id: str,
    timestamp_utc: str,
    command: str,
    input_payload: dict[str, Any],
    config: dict[str, Any],
    output_hash_sha256: str,
) -> dict[str, Any]:
    input_hash_sha256 = sha256_payload(input_payload)
    config_hash_sha256 = sha256_payload(config)
    canonical_output_hash = output_hash_sha256.upper()
    return {
        "run_id": run_id,
        "timestamp_utc": timestamp_utc,
        "command": command,
        "input_hash_sha256": input_hash_sha256,
        "config_hash_sha256": config_hash_sha256,
        "output_hash_sha256": output_hash_sha256,
        "input_payload_sha256": input_hash_sha256.upper(),
        "config_payload_sha256": config_hash_sha256.upper(),
        "output_payload_pre_trace_sha256": canonical_output_hash,
        "c05_hash_lineage_contract_version": C05_HASH_LINEAGE_CONTRACT_VERSION,
        "c05_hash_lineage_contract_sha256": C05_HASH_LINEAGE_CONTRACT_SHA256,
        "canonical_hash_lineage_status": {
            "normalized_config_sha256": "DEFERRED_NOT_EMITTED",
            "runtime_loaded_config_sha256": "DEFERRED_NOT_EMITTED",
            "trace_receipt_sha256": "DEFERRED_NOT_EMITTED",
            "manifest_sha256": "DEFERRED_NOT_EMITTED",
            "run_manifest_sha256": "DEFERRED_NOT_EMITTED",
            "command_context_sha256": "DEFERRED_NOT_EMITTED",
            "lineage_bundle_sha256": "DEFERRED_NOT_EMITTED",
            "replay_lite": "NOT_PROVEN",
            "reproducibility": "NOT_PROVEN",
        },
        "output_hash_semantics": {
            "output_hash_sha256": "provisional_payload_hash_before_trace_receipt_insertion",
            "output_payload_pre_trace_sha256": "canonical uppercase alias of provisional payload hash before trace receipt insertion",
            "final_artifact_hash_surface": "runtime execution_manifest.json decision_output_file_sha256",
            "final_artifact_hash_note": "final artifact hash covers run-variant trace metadata such as command/output directory and is not expected to be replay-stable when those metadata differ",
        },
        "config_version": config.get("config_version", "CONFIG_VERSION_ABSENT"),
        "repo_relative_surfaces": [
            "src/qira/decision_unit.py",
            "src/qira/ev_output.py",
            "src/qira/gating.py",
            "src/qira/repro_trace.py",
            "src/qira/schemas.py",
            "src/qira/run_active_core.py",
            "schemas/qira_decision_input.schema.json",
            "schemas/qira_decision_output.schema.json",
            "configs/qira_wave01_default_config.json",
            "samples/wave01/sample_decision_input.json",
        ],
        "proof_limits": {
            "full_reproducibility": "NOT_PROVEN",
            "scope": "Wave 01 trace skeleton only; bounded local environment capture may exist in runtime manifest, but no git provenance, dependency lock, clean-environment replay, installed-package replay, or independent reproduction proof.",
        },
    }


def make_failure_trace_receipt(
    run_id: str,
    input_hash_sha256: str,
    config_hash_sha256: str,
    pre_trace_payload_hash_sha256: str,
    error_type: str,
    error_stage: str,
    *,
    error_field: str | None = None,
    error_code: str | None = None,
    config_version: str = "CONFIG_VERSION_ABSENT",
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "run_id": run_id,
        "input_hash_sha256": input_hash_sha256,
        "config_hash_sha256": config_hash_sha256,
        "input_payload_sha256": input_hash_sha256.upper(),
        "config_payload_sha256": config_hash_sha256.upper(),
        "trace_scope": "FAILURE_ENVELOPE_TRACE_ATTRIBUTION_WITH_LIMITS",
        "trace_limit": "Artifact attribution only; NOT_FULL_REPLAY; not deterministic replay, independent reproducibility, data admissibility, leakage cleanliness, runtime correctness, EV correctness, readiness, DD, sale, valuation, buyer readiness, or 15M support.",
        "pre_trace_payload_hash_sha256": pre_trace_payload_hash_sha256,
        "error_payload_pre_trace_sha256": pre_trace_payload_hash_sha256.upper(),
        "c05_hash_lineage_contract_version": C05_HASH_LINEAGE_CONTRACT_VERSION,
        "c05_hash_lineage_contract_sha256": C05_HASH_LINEAGE_CONTRACT_SHA256,
        "canonical_hash_lineage_status": {
            "final_error_file_sha256": "DEFERRED_NOT_EMITTED",
            "trace_receipt_sha256": "DEFERRED_NOT_EMITTED",
            "manifest_sha256": "DEFERRED_NOT_EMITTED",
            "run_manifest_sha256": "DEFERRED_NOT_EMITTED",
            "command_context_sha256": "DEFERRED_NOT_EMITTED",
            "lineage_bundle_sha256": "DEFERRED_NOT_EMITTED",
            "replay_lite": "NOT_PROVEN",
            "reproducibility": "NOT_PROVEN",
        },
        "error_type": error_type,
        "error_stage": error_stage,
        "config_version": config_version,
    }
    if error_field is not None:
        receipt["error_field"] = error_field
    if error_code is not None:
        receipt["error_code"] = error_code
    return receipt
