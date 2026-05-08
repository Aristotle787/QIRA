from __future__ import annotations

from typing import Any


def compute_ev(input_payload: dict[str, Any]) -> dict[str, Any]:
    expected_return_bps = float(input_payload["expected_return_bps"])
    expected_cost_bps = float(input_payload["expected_cost_bps"])
    uncertainty_bps = float(input_payload["uncertainty_bps"])
    risk_score = float(input_payload["risk_score"])
    net_ev_bps = expected_return_bps - expected_cost_bps
    risk_adjusted_ev_bps = net_ev_bps - uncertainty_bps * risk_score
    return {
        "gross_ev_bps": expected_return_bps,
        "net_ev_bps": net_ev_bps,
        "risk_adjusted_ev_bps": risk_adjusted_ev_bps,
        "units": "bps",
        "proof_limits": {
            "ev_validity": "NOT_PROVEN",
            "scope": "Wave 01 skeleton functional proof only; not EV correctness, predictive validity, or investment validity.",
        },
    }

