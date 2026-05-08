from __future__ import annotations

from typing import Any


def evaluate_gate(input_payload: dict[str, Any], ev_payload: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    reason_details: list[dict[str, Any]] = []
    risk_score = float(input_payload["risk_score"])
    liquidity_score = float(input_payload["liquidity_score"])
    risk_adjusted_ev_bps = float(ev_payload["risk_adjusted_ev_bps"])
    max_risk_score = float(config["max_risk_score"])
    min_liquidity_score = float(config["min_liquidity_score"])
    min_risk_adjusted_ev_bps = float(config["min_risk_adjusted_ev_bps"])
    if risk_score > max_risk_score:
        reasons.append("BLOCK_RISK_SCORE_GT_MAX")
        reason_details.append(
            {
                "reason_code": "BLOCK_RISK_SCORE_GT_MAX",
                "severity": "BLOCK",
                "observed_field": "risk_score",
                "observed_value": risk_score,
                "comparator": ">",
                "threshold_field": "max_risk_score",
                "threshold_value": max_risk_score,
                "source": "qira.gating.evaluate_gate",
            }
        )
    if liquidity_score < min_liquidity_score:
        reasons.append("BLOCK_LIQUIDITY_SCORE_LT_MIN")
        reason_details.append(
            {
                "reason_code": "BLOCK_LIQUIDITY_SCORE_LT_MIN",
                "severity": "BLOCK",
                "observed_field": "liquidity_score",
                "observed_value": liquidity_score,
                "comparator": "<",
                "threshold_field": "min_liquidity_score",
                "threshold_value": min_liquidity_score,
                "source": "qira.gating.evaluate_gate",
            }
        )
    if reasons:
        status = "BLOCK"
    elif risk_adjusted_ev_bps < min_risk_adjusted_ev_bps:
        status = "ABSTAIN"
        reasons.append("ABSTAIN_RISK_ADJUSTED_EV_LT_MIN")
        reason_details.append(
            {
                "reason_code": "ABSTAIN_RISK_ADJUSTED_EV_LT_MIN",
                "severity": "ABSTAIN",
                "observed_field": "risk_adjusted_ev_bps",
                "observed_value": risk_adjusted_ev_bps,
                "comparator": "<",
                "threshold_field": "min_risk_adjusted_ev_bps",
                "threshold_value": min_risk_adjusted_ev_bps,
                "source": "qira.gating.evaluate_gate",
            }
        )
    else:
        status = "PASS"
        reasons.append("PASS_ALL_WAVE01_THRESHOLDS")
        reason_details.append(
            {
                "reason_code": "PASS_ALL_WAVE01_THRESHOLDS",
                "severity": "PASS",
                "observed_field": None,
                "observed_value": None,
                "comparator": "all_thresholds_satisfied",
                "threshold_field": None,
                "threshold_value": None,
                "source": "qira.gating.evaluate_gate",
            }
        )
    return {
        "gate_status": status,
        "gate_reasons": reasons,
        "gate_reason_details": reason_details,
        "proof_limits": {
            "risk_model_sufficiency": "NOT_PROVEN",
            "scope": "Wave 01 skeleton gating proof only; not risk-model sufficiency, liquidity realism, or production gating readiness.",
        },
    }
