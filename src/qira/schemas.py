from __future__ import annotations

from datetime import datetime, timezone
import math
from typing import Any


INPUT_REQUIRED_FIELDS = (
    "decision_context_id",
    "as_of_timestamp",
    "instrument_id",
    "expected_return_bps",
    "expected_cost_bps",
    "uncertainty_bps",
    "risk_score",
    "liquidity_score",
    "regime_label",
    "config_id",
)

OUTPUT_REQUIRED_FIELDS = (
    "run_id",
    "decision_context_id",
    "instrument_id",
    "decision",
    "gross_ev_bps",
    "net_ev_bps",
    "risk_adjusted_ev_bps",
    "gate_status",
    "gate_reasons",
    "gate_reason_details",
    "explanation",
    "proof_limits",
    "trace_receipt",
    "ev_units",
    "ev_horizon",
    "data_version",
    "model_version",
    "output_contract_version",
    "claim_boundary_policy",
)

NUMERIC_INPUT_FIELDS = (
    "expected_return_bps",
    "expected_cost_bps",
    "uncertainty_bps",
    "risk_score",
    "liquidity_score",
)

NUMERIC_OUTPUT_FIELDS = (
    "gross_ev_bps",
    "net_ev_bps",
    "risk_adjusted_ev_bps",
)

STRING_OUTPUT_FIELDS = (
    "run_id",
    "decision_context_id",
    "instrument_id",
    "ev_units",
    "ev_horizon",
    "data_version",
    "model_version",
    "output_contract_version",
)

CONFIG_REQUIRED_FIELDS = (
    "max_risk_score",
    "min_liquidity_score",
    "min_risk_adjusted_ev_bps",
)

CONFIG_NUMERIC_FIELDS = CONFIG_REQUIRED_FIELDS

VALID_GATE_STATUSES = ("PASS", "BLOCK", "ABSTAIN")
VALID_DECISIONS = ("ACT", "NO_ACTION", "ABSTAIN")

C05_HASH_LINEAGE_CONTRACT_VERSION = "v1"
C05_HASH_LINEAGE_CONTRACT_SHA256 = "7D109EB2024EE505A0DBAE5C75DFE8F8499DD15D066FCECBEB3361EF0F6DA16B"
C05_OPTIONAL_INPUT_LINEAGE_FIELDS = (
    "input_payload_sha256",
    "c05_hash_lineage_contract_version",
    "c05_hash_lineage_contract_sha256",
)
C05_OPTIONAL_OUTPUT_LINEAGE_FIELDS = (
    "final_output_file_sha256",
    "final_error_file_sha256",
)
C05_OPTIONAL_TRACE_RECEIPT_FIELDS = (
    "c05_hash_lineage_contract_version",
    "c05_hash_lineage_contract_sha256",
    "config_payload_sha256",
    "normalized_config_sha256",
    "runtime_loaded_config_sha256",
    "input_payload_sha256",
    "output_payload_pre_trace_sha256",
    "error_payload_pre_trace_sha256",
    "trace_receipt_sha256",
    "manifest_sha256",
    "run_manifest_sha256",
    "command_context_sha256",
    "lineage_bundle_sha256",
    "canonical_hash_lineage_status",
)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_finite_number(value: Any) -> bool:
    return _is_number(value) and math.isfinite(value)


def _is_explicit_utc_timestamp(value: str) -> bool:
    if not (value.endswith("Z") or value.endswith("+00:00")):
        return False
    parse_value = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(parse_value)
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed)



def validate_config(config):
    errors = []

    if not isinstance(config, dict):
        return [
            {
                "field": "config",
                "error": "invalid_config_object",
                "expected": "object",
                "actual": type(config).__name__,
            }
        ]

    for field in CONFIG_REQUIRED_FIELDS:
        if field not in config:
            errors.append(
                {
                    "field": field,
                    "error": "missing_config_field",
                    "expected": "required numeric config field",
                    "actual": "missing",
                }
            )
            continue

        value = config[field]
        if not _is_finite_number(value):
            errors.append(
                {
                    "field": field,
                    "error": "invalid_config_numeric_field",
                    "expected": "finite int or float excluding bool",
                    "actual": type(value).__name__,
                }
            )
            continue
        if field in ("max_risk_score", "min_liquidity_score") and not 0 <= value <= 1:
            errors.append(
                {
                    "field": field,
                    "error": "invalid_config_domain_field",
                    "expected": "finite numeric value between 0 and 1 inclusive",
                    "actual": value,
                }
            )

    return errors


def validate_input(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for field in INPUT_REQUIRED_FIELDS:
        if field not in payload:
            errors.append(f"missing_input_field:{field}")
    for field in NUMERIC_INPUT_FIELDS:
        if field in payload and not _is_finite_number(payload[field]):
            errors.append(f"invalid_numeric_input_field:{field}")
    for field in ("risk_score", "liquidity_score"):
        if field in payload and _is_finite_number(payload[field]) and not 0 <= payload[field] <= 1:
            errors.append(f"invalid_domain_input_field:{field}")
    if (
        "uncertainty_bps" in payload
        and _is_finite_number(payload["uncertainty_bps"])
        and payload["uncertainty_bps"] < 0
    ):
        errors.append("invalid_domain_input_field:uncertainty_bps")
    for field in ("decision_context_id", "as_of_timestamp", "instrument_id", "regime_label", "config_id"):
        if field in payload and not isinstance(payload[field], str):
            errors.append(f"invalid_string_input_field:{field}")
    for field in C05_OPTIONAL_INPUT_LINEAGE_FIELDS:
        if field in payload and not isinstance(payload[field], str):
            errors.append(f"invalid_string_input_field:{field}")
    if "as_of_timestamp" in payload and isinstance(payload["as_of_timestamp"], str):
        if not _is_explicit_utc_timestamp(payload["as_of_timestamp"]):
            errors.append("invalid_timestamp_input_field:as_of_timestamp")
    return not errors, errors


def validate_output(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for field in OUTPUT_REQUIRED_FIELDS:
        if field not in payload:
            errors.append(f"missing_output_field:{field}")
    for field in NUMERIC_OUTPUT_FIELDS:
        if field in payload and not _is_number(payload[field]):
            errors.append(f"invalid_numeric_output_field:{field}")
    for field in STRING_OUTPUT_FIELDS:
        if field in payload and not isinstance(payload[field], str):
            errors.append(f"invalid_string_output_field:{field}")
    if payload.get("gate_status") not in VALID_GATE_STATUSES:
        errors.append("invalid_gate_status")
    if payload.get("decision") not in VALID_DECISIONS:
        errors.append("invalid_decision")
    if "gate_reasons" in payload and not isinstance(payload["gate_reasons"], list):
        errors.append("invalid_gate_reasons")
    if "gate_reason_details" in payload:
        if not isinstance(payload["gate_reason_details"], list):
            errors.append("invalid_gate_reason_details")
        else:
            for detail in payload["gate_reason_details"]:
                if not isinstance(detail, dict):
                    errors.append("invalid_gate_reason_detail")
                    continue
                if "reason_code" not in detail or "severity" not in detail:
                    errors.append("invalid_gate_reason_detail")
    if "proof_limits" in payload and not isinstance(payload["proof_limits"], dict):
        errors.append("invalid_proof_limits")
    if "trace_receipt" in payload and not isinstance(payload["trace_receipt"], dict):
        errors.append("invalid_trace_receipt")
    if isinstance(payload.get("trace_receipt"), dict):
        trace_receipt = payload["trace_receipt"]
        for field in C05_OPTIONAL_TRACE_RECEIPT_FIELDS:
            if field in trace_receipt and not isinstance(trace_receipt[field], (str, dict)):
                errors.append(f"invalid_trace_receipt_field:{field}")
    for field in C05_OPTIONAL_OUTPUT_LINEAGE_FIELDS:
        if field in payload and not isinstance(payload[field], str):
            errors.append(f"invalid_string_output_field:{field}")
    if "claim_boundary_policy" in payload and not isinstance(
        payload["claim_boundary_policy"], dict
    ):
        errors.append("invalid_claim_boundary_policy")
    return not errors, errors
