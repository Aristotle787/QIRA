from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path

OUTPUT_CONTRACT_VERSION = "QIRA_C02_C02B_OUTPUT_CONTRACT_AND_MINIMUM_SPINE_CONTRACT_v1"
C05_HASH_LINEAGE_CONTRACT_VERSION = "v1"
C05_HASH_LINEAGE_CONTRACT_SHA256 = "7D109EB2024EE505A0DBAE5C75DFE8F8499DD15D066FCECBEB3361EF0F6DA16B"


def _repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def _not_proven_limits() -> dict[str, str]:
    return {
        "technical_readiness": "NOT_PROVEN",
        "dd_readiness": "NOT_PROVEN",
        "sale_grade_readiness": "NOT_PROVEN",
        "sale_value_defensibility": "NOT_PROVEN",
        "support_15m": "NOT_PROVEN",
        "predictive_validity": "NOT_PROVEN",
        "ev_validity": "NOT_PROVEN",
        "live_trading_capability": "NOT_PROVEN",
    }


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_file_sha256(path: Path) -> str:
    try:
        return _file_sha256(path)
    except (FileNotFoundError, PermissionError, OSError):
        return "UNAVAILABLE_WITH_LIMITS"


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(path)


def _local_environment_snapshot() -> dict[str, object]:
    modules = {}
    for module_name in ("build", "setuptools", "wheel"):
        modules[module_name] = "AVAILABLE" if importlib.util.find_spec(module_name) else "UNAVAILABLE"
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "local_module_availability": modules,
        "proof_limit": "Current local source-tree environment only; no raw environment variables, package install, clean-environment replay, installed-package replay, or independent reproduction proof.",
    }


def _failure_error_marker(error_message: str, details=None) -> tuple[str | None, str | None]:
    if details and isinstance(details, dict):
        errors = details.get("errors")
        if isinstance(errors, list) and errors:
            first = errors[0]
            if isinstance(first, dict):
                error_code = first.get("error")
                error_field = first.get("field")
                return (
                    str(error_field) if error_field is not None else None,
                    str(error_code) if error_code is not None else None,
                )
    parts = error_message.split(":")
    if len(parts) >= 3:
        return parts[-1], parts[-2]
    return None, None


def _failure_payload(error_type, error_message, error_stage, details=None, trace_context=None):
    input_payload = trace_context.get("input_payload") if isinstance(trace_context, dict) else {}
    config = trace_context.get("config") if isinstance(trace_context, dict) else {}
    if not isinstance(input_payload, dict):
        input_payload = {}
    if not isinstance(config, dict):
        config = {}
    payload = {
        "status": "FAIL",
        "error_type": error_type,
        "error_message": error_message,
        "error_stage": error_stage,
        "decision": "ABSTAIN",
        "gate_status": "ABSTAIN",
        "abstain_reason": "FAILURE_ENVELOPE_ABSTAIN_WITH_LIMITS",
        "validation_status": "NOT_PROVEN",
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
        "proof_limits": _not_proven_limits(),
    }
    if details is not None:
        payload["details"] = details
    if trace_context is not None:
        from qira.repro_trace import make_failure_trace_receipt, make_run_id, sha256_payload

        input_hash = trace_context.get("input_hash_sha256")
        config_hash = trace_context.get("config_hash_sha256")
        config_version = "CONFIG_VERSION_ABSENT"
        if isinstance(config, dict):
            config_version = str(config.get("config_version", "CONFIG_VERSION_ABSENT"))
            config_hash = sha256_payload(config)
        if isinstance(input_payload, dict):
            input_hash = sha256_payload(input_payload)
        if isinstance(input_payload, dict) and isinstance(config, dict):
            run_id = make_run_id(input_payload, config)
        else:
            run_id = "QIRA-WAVE01-FAILURE-" + sha256_payload(
                {
                    "error_type": error_type,
                    "error_stage": error_stage,
                    "input_hash_sha256": input_hash,
                    "config_hash_sha256": config_hash,
                }
            )[:16].upper()
        pre_trace_payload_hash = sha256_payload(payload)
        error_field, error_code = _failure_error_marker(error_message, details)
        payload["run_id"] = run_id
        payload["error_payload_without_trace_hash_sha256"] = pre_trace_payload_hash
        payload["trace_receipt"] = make_failure_trace_receipt(
            run_id,
            str(input_hash or "UNAVAILABLE_WITH_LIMITS"),
            str(config_hash or "UNAVAILABLE_WITH_LIMITS"),
            pre_trace_payload_hash,
            error_type,
            error_stage,
            error_field=error_field,
            error_code=error_code,
            config_version=config_version,
        )
    return payload



def _write_failure_outputs(output_dir: Path, error_output: dict[str, object]) -> None:
    error_output_path = output_dir / "error_output.json"
    with error_output_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(error_output, f, indent=2, sort_keys=True)
        f.write("\n")
    final_error_file_sha256 = _file_sha256(error_output_path)
    run_log = {
        "status": "FAIL",
        "runner": "src/qira/run_active_core.py",
        "error_output": str(error_output_path),
        "run_id": error_output.get("run_id", "RUN_ID_UNAVAILABLE_WITH_LIMITS"),
        "trace_receipt": error_output.get("trace_receipt", {}),
        "error_payload_without_trace_hash_sha256": error_output.get(
            "error_payload_without_trace_hash_sha256",
            "UNAVAILABLE_WITH_LIMITS",
        ),
        "final_error_file_sha256": final_error_file_sha256,
        "c05_hash_lineage_contract_version": C05_HASH_LINEAGE_CONTRACT_VERSION,
        "c05_hash_lineage_contract_sha256": C05_HASH_LINEAGE_CONTRACT_SHA256,
        "proof_limits": _not_proven_limits(),
    }
    with (output_dir / "run.log").open("w", encoding="utf-8", newline="\n") as f:
        json.dump(run_log, f, indent=2, sort_keys=True)
        f.write("\n")


def _emit_failure(output_dir, error_type, error_message, error_stage, details=None, trace_context=None):
    payload = _failure_payload(
        error_type,
        error_message,
        error_stage,
        details=details,
        trace_context=trace_context,
    )
    _write_failure_outputs(output_dir, payload)
    return 2


def main() -> int:
    repo_root = _repo_root_from_script()
    src_root = repo_root / "src"
    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))
    from qira.decision_unit import build_decision
    from qira.schemas import validate_config

    parser = argparse.ArgumentParser(description="Run QIRA Wave 01 active core skeleton.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    config_path = Path(args.config)
    output_dir = Path(args.output_dir)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as exc:
        print(
            "QIRA runtime output write failure; status=FAIL; "
            "error_type=FILE_IO_ERROR; error_stage=output_write; "
            f"error_message={type(exc).__name__}; "
            "decision=ABSTAIN; gate_status=ABSTAIN; "
            "technical_readiness=NOT_PROVEN",
            file=sys.stderr,
        )
        return 2

    try:
        with input_path.open("r", encoding="utf-8") as f:
            input_payload = json.load(f)
    except json.JSONDecodeError as exc:
        return _emit_failure(
            output_dir,
            "JSON_PARSE_ERROR",
            str(exc),
            "input_json_load",
            trace_context={
                "input_hash_sha256": _safe_file_sha256(input_path),
                "config_hash_sha256": _safe_file_sha256(config_path),
            },
        )
    except FileNotFoundError as exc:
        return _emit_failure(
            output_dir,
            "FILE_NOT_FOUND",
            str(exc),
            "input_json_load",
            trace_context={"config_hash_sha256": _safe_file_sha256(config_path)},
        )
    except (PermissionError, OSError) as exc:
        return _emit_failure(
            output_dir,
            "FILE_IO_ERROR",
            str(exc),
            "input_json_load",
            trace_context={"config_hash_sha256": _safe_file_sha256(config_path)},
        )

    try:
        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
        config_errors = validate_config(config)
        if config_errors:
            return _emit_failure(
                output_dir,
                "VALIDATION_ERROR",
                "config_validation_failed",
                "Config validation failed",
                details={"errors": config_errors},
                trace_context={"input_payload": input_payload, "config": config},
            )

    except json.JSONDecodeError as exc:
        return _emit_failure(
            output_dir,
            "JSON_PARSE_ERROR",
            str(exc),
            "config_json_load",
            trace_context={
                "input_payload": input_payload,
                "config_hash_sha256": _safe_file_sha256(config_path),
            },
        )
    except FileNotFoundError as exc:
        return _emit_failure(
            output_dir,
            "FILE_NOT_FOUND",
            str(exc),
            "config_json_load",
            trace_context={"input_payload": input_payload},
        )
    except (PermissionError, OSError) as exc:
        return _emit_failure(
            output_dir,
            "FILE_IO_ERROR",
            str(exc),
            "config_json_load",
            trace_context={"input_payload": input_payload},
        )

    command = (
        "python src/qira/run_active_core.py "
        f"--input {_display_path(input_path, repo_root)} "
        f"--config {_display_path(config_path, repo_root)} "
        f"--output-dir {_display_path(output_dir, repo_root)}"
    )
    try:
        output = build_decision(input_payload, config, command)
    except ValueError as exc:
        message = str(exc)
        if not message.startswith(("input_validation_failed:", "output_validation_failed:")):
            raise
        return _emit_failure(
            output_dir,
            "VALIDATION_ERROR",
            message,
            "validation",
            trace_context={"input_payload": input_payload, "config": config},
        )

    decision_output_path = output_dir / "decision_output.json"
    run_log_path = output_dir / "run.log"
    execution_manifest_path = output_dir / "execution_manifest.json"
    try:
        with decision_output_path.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(output, f, indent=2, sort_keys=True)
            f.write("\n")
        decision_output_file_sha256 = _file_sha256(decision_output_path)
        trace = output["trace_receipt"]
        manifest = {
            "status": "PASS",
            "runner": "src/qira/run_active_core.py",
            "input_path": _display_path(input_path, repo_root),
            "config_path": _display_path(config_path, repo_root),
            "output_dir": _display_path(output_dir, repo_root),
            "decision_output": _display_path(decision_output_path, repo_root),
            "decision_output_file_sha256": decision_output_file_sha256,
            "final_output_file_sha256": decision_output_file_sha256,
            "c05_hash_lineage_contract_version": C05_HASH_LINEAGE_CONTRACT_VERSION,
            "c05_hash_lineage_contract_sha256": C05_HASH_LINEAGE_CONTRACT_SHA256,
            "decision_output_file_hash_semantics": {
                "scope": "final serialized decision_output.json artifact",
                "includes_run_variant_trace_metadata": True,
                "replay_stability_expectation": "may differ when command or output directory differs",
            },
            "run_log": _display_path(run_log_path, repo_root),
            "run_id": output["run_id"],
            "config_id": config.get("config_id", "CONFIG_ID_ABSENT"),
            "config_version": config.get("config_version", "CONFIG_VERSION_ABSENT"),
            "trace_hashes": {
                "input_hash_sha256": trace["input_hash_sha256"],
                "config_hash_sha256": trace["config_hash_sha256"],
                "output_hash_sha256": trace["output_hash_sha256"],
                "input_payload_sha256": trace.get("input_payload_sha256", "UNAVAILABLE_WITH_LIMITS"),
                "config_payload_sha256": trace.get("config_payload_sha256", "UNAVAILABLE_WITH_LIMITS"),
                "output_payload_pre_trace_sha256": trace.get(
                    "output_payload_pre_trace_sha256",
                    "UNAVAILABLE_WITH_LIMITS",
                ),
                "output_hash_semantics": trace.get("output_hash_semantics", {}),
            },
            "environment_dependency_lock_surface": _local_environment_snapshot(),
            "proof_limits": output["proof_limits"],
        }
        with execution_manifest_path.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(manifest, f, indent=2, sort_keys=True)
            f.write("\n")
        run_log = {
            "status": "PASS",
            "runner": "src/qira/run_active_core.py",
            "decision_output": _display_path(decision_output_path, repo_root),
            "decision_output_file_sha256": decision_output_file_sha256,
            "final_output_file_sha256": decision_output_file_sha256,
            "execution_manifest": _display_path(execution_manifest_path, repo_root),
            "config_id": config.get("config_id", "CONFIG_ID_ABSENT"),
            "config_version": config.get("config_version", "CONFIG_VERSION_ABSENT"),
            "c05_hash_lineage_contract_version": C05_HASH_LINEAGE_CONTRACT_VERSION,
            "c05_hash_lineage_contract_sha256": C05_HASH_LINEAGE_CONTRACT_SHA256,
            "proof_limits": output["proof_limits"],
        }
        with run_log_path.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(run_log, f, indent=2, sort_keys=True)
            f.write("\n")
    except (PermissionError, OSError) as exc:
        print(
            "QIRA runtime output write failure; status=FAIL; "
            "error_type=FILE_IO_ERROR; error_stage=output_write; "
            f"error_message={type(exc).__name__}; "
            "decision=ABSTAIN; gate_status=ABSTAIN; "
            "technical_readiness=NOT_PROVEN",
            file=sys.stderr,
        )
        return 2

    print(
        "QIRA Wave 01 active core skeleton run completed; "
        f"decision={output['decision']}; "
        f"gate_status={output['gate_status']}; "
        "technical_readiness=NOT_PROVEN; "
        "sale_value_defensibility=NOT_PROVEN"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
