from __future__ import annotations

from typing import Any

from qira.ev_output import compute_ev
from qira.gating import evaluate_gate
from qira.repro_trace import make_run_id, make_trace_receipt, sha256_payload
from qira.schemas import validate_input, validate_output

OUTPUT_CONTRACT_VERSION = "QIRA_C02_C02B_OUTPUT_CONTRACT_AND_MINIMUM_SPINE_CONTRACT_v1"


def build_decision(input_payload: dict[str, Any], config: dict[str, Any], command: str) -> dict[str, Any]:
    valid, errors = validate_input(input_payload)
    if not valid:
        raise ValueError("input_validation_failed:" + ",".join(errors))
    ev_payload = compute_ev(input_payload)
    gate_payload = evaluate_gate(input_payload, ev_payload, config)
    gate_status = gate_payload["gate_status"]
    if gate_status == "PASS":
        decision = "ACT"
    elif gate_status == "BLOCK":
        decision = "NO_ACTION"
    else:
        decision = "ABSTAIN"
    run_id = make_run_id(input_payload, config)
    output = {
        "run_id": run_id,
        "decision_context_id": input_payload["decision_context_id"],
        "instrument_id": input_payload["instrument_id"],
        "decision": decision,
        "gross_ev_bps": ev_payload["gross_ev_bps"],
        "net_ev_bps": ev_payload["net_ev_bps"],
        "risk_adjusted_ev_bps": ev_payload["risk_adjusted_ev_bps"],
        "gate_status": gate_status,
        "gate_reasons": gate_payload["gate_reasons"],
        "gate_reason_details": gate_payload["gate_reason_details"],
        "ev_units": str(config.get("ev_units", "BPS")),
        "ev_horizon": str(config.get("ev_horizon", "EV_HORIZON_UNSPECIFIED_WITH_LIMITS")),
        "data_version": str(input_payload.get("data_version", "DATA_VERSION_ABSENT")),
        "model_version": str(config.get("model_version", "MODEL_VERSION_ABSENT")),
        "output_contract_version": OUTPUT_CONTRACT_VERSION,
        "claim_boundary_policy": {
            "technical_readiness": "NOT_PROVEN",
            "runtime_behavior": "NOT_PROVEN",
            "validation": "NOT_PROVEN",
            "ev_correctness": "NOT_PROVEN",
            "sale_readiness": "NOT_PROVEN",
            "support_15m": "NOT_PROVEN",
        },
        "explanation": {
            "advisory_only": True,
            "units": "bps",
            "summary": "Wave 01 deterministic skeleton output from synthetic input and local config; runtime behavior and readiness remain NOT_PROVEN.",
        },
        "proof_limits": {
            "technical_readiness": "NOT_PROVEN",
            "dd_readiness": "NOT_PROVEN",
            "sale_grade_readiness": "NOT_PROVEN",
            "sale_value_defensibility": "NOT_PROVEN",
            "support_15m": "NOT_PROVEN",
            "ev_validity": "NOT_PROVEN",
            "predictive_validity": "NOT_PROVEN",
            "live_trading_capability": "NOT_PROVEN",
            "scope": "Wave 01 output construction is contract-mapped with limits; runtime behavior, validation, EV correctness, and readiness remain NOT_PROVEN.",
        },
        "trace_receipt": {},
    }
    provisional_hash = sha256_payload(output)
    output["trace_receipt"] = make_trace_receipt(
        run_id=run_id,
        timestamp_utc=input_payload["as_of_timestamp"],
        command=command,
        input_payload=input_payload,
        config=config,
        output_hash_sha256=provisional_hash,
    )
    valid_output, output_errors = validate_output(output)
    if not valid_output:
        raise ValueError("output_validation_failed:" + ",".join(output_errors))
    return output
