# QIRA Phase 3 Local Static Check Receipt

```json
{
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
    "TARGET_TRANSACTION_OBJECTIVE_15M_SUPPORT_CLAIM = NOT_PROVEN"
  ],
  "files": [
    {
      "path": ".github/workflows/qira-governance-static.yml",
      "sha256": "087c5e66c468b1c024abcb3dc67ff4c2da33e2056f83e59d37d0e69f0021b0cb",
      "size_bytes": 441
    },
    {
      "path": ".github/workflows/qira-python-quality-candidate.yml",
      "sha256": "f0397aead18919826307509040ed9e2b6a29b0332a2c259745506261e8f1b3b9",
      "size_bytes": 598
    },
    {
      "path": "tools/ci/README.md",
      "sha256": "f80411450de03e2e99f888ae2b7a4bd17c8b0cb6ec7dbbfdf2be3f3bdb6a0cd8",
      "size_bytes": 1315
    },
    {
      "path": "tools/ci/qira_ci_local_static_runner.py",
      "sha256": "f015d2286f6285c979fd00592dab3b1f5e1bdf69209ef9dd11e076168756f97f",
      "size_bytes": 5164
    },
    {
      "path": "tools/ci/qira_claim_boundary_scan.py",
      "sha256": "218f07b59c54a46c579a9184eb826fc95d171642e7c5048bf9ef9092a92ab33e",
      "size_bytes": 3202
    },
    {
      "path": "tools/ci/qira_secret_surface_scan.py",
      "sha256": "433dce51b2197667b3b0f50834273ef3c03efc69b137fa52d84c4f77f3185363",
      "size_bytes": 2320
    },
    {
      "path": "tools/ci/qira_json_semantic_check.py",
      "sha256": "75fb44f25ff0593c144408f4888217533f199efc9156f1c0aa582b349c048aa9",
      "size_bytes": 2350
    },
    {
      "path": "tools/ci/qira_artifact_integrity_check.py",
      "sha256": "5df0d12bfdec4c19cd0066be1f68a47d28feaa3e3beadd87d06d48bdc82a5526",
      "size_bytes": 2977
    },
    {
      "path": "factory_acceleration/phase_3_ci/README.md",
      "sha256": "b279556527acd05bf17aaaa89c08b52c06f50f3f6a21847e96bdc7163bf7a199",
      "size_bytes": 989
    },
    {
      "path": "factory_acceleration/phase_3_ci/PHASE_3_CI_QUALITY_LOOP_REGISTER_v1.json",
      "sha256": "86a117b01ff024d4de6e31c1eaa56aa5497d51cb97923fe58ab11256964e1f7c",
      "size_bytes": 1933
    },
    {
      "path": "factory_acceleration/phase_3_ci/CI_TOOL_ADOPTION_BOUNDARY_v1.md",
      "sha256": "827344d4bd093b726e304161051918cbbe5adb8262d37cd512c912ff447c0c69",
      "size_bytes": 909
    },
    {
      "path": "factory_acceleration/phase_3_ci/NEXT_ROUTE_AFTER_PHASE_3_CI_v1.md",
      "sha256": "0c5c11e2dbccff64cf6442a629ef782edbf880987b6536970a5aa14d5e2dfc2b",
      "size_bytes": 1153
    },
    {
      "path": "factory_acceleration/phase_3_ci/PHASE_3_LOCAL_STATIC_CHECK_RECEIPT_v1.md",
      "sha256": "5508366ff563a08de54071bda55439ef70f0eebd64a00edde23d2c104e7d871c",
      "size_bytes": 13739
    }
  ],
  "generated_utc": "2026-05-08T21:04:03.853603+00:00",
  "github_parser_acceptance": "NOT_PROVEN",
  "proof_ceiling": "PHASE_3_CI_QUALITY_LOOP_CANDIDATE_CREATED_AND_LOCAL_STATIC_SELF_VERIFIED_WITH_LIMITS_NO_REMOTE_CI_RUN_NO_INSTALL_NO_TESTS_NO_VALIDATION_NO_READINESS_PROOF",
  "remote_ci_execution": "NOT_PROVEN",
  "scripts": [
    {
      "exit_code": 0,
      "script": "tools/ci/qira_artifact_integrity_check.py",
      "stderr_size": 0,
      "stdout_json": {
        "check": "artifact_integrity_check",
        "checks": {
          "missing": [],
          "phase_3_exact": true,
          "target_workflows_present": true,
          "tools_ci_exact": true
        },
        "files": [
          {
            "path": ".github/workflows/qira-governance-static.yml",
            "sha256": "087c5e66c468b1c024abcb3dc67ff4c2da33e2056f83e59d37d0e69f0021b0cb",
            "size_bytes": 441
          },
          {
            "path": ".github/workflows/qira-python-quality-candidate.yml",
            "sha256": "f0397aead18919826307509040ed9e2b6a29b0332a2c259745506261e8f1b3b9",
            "size_bytes": 598
          },
          {
            "path": "tools/ci/README.md",
            "sha256": "f80411450de03e2e99f888ae2b7a4bd17c8b0cb6ec7dbbfdf2be3f3bdb6a0cd8",
            "size_bytes": 1315
          },
          {
            "path": "tools/ci/qira_ci_local_static_runner.py",
            "sha256": "f015d2286f6285c979fd00592dab3b1f5e1bdf69209ef9dd11e076168756f97f",
            "size_bytes": 5164
          },
          {
            "path": "tools/ci/qira_claim_boundary_scan.py",
            "sha256": "218f07b59c54a46c579a9184eb826fc95d171642e7c5048bf9ef9092a92ab33e",
            "size_bytes": 3202
          },
          {
            "path": "tools/ci/qira_secret_surface_scan.py",
            "sha256": "433dce51b2197667b3b0f50834273ef3c03efc69b137fa52d84c4f77f3185363",
            "size_bytes": 2320
          },
          {
            "path": "tools/ci/qira_json_semantic_check.py",
            "sha256": "75fb44f25ff0593c144408f4888217533f199efc9156f1c0aa582b349c048aa9",
            "size_bytes": 2350
          },
          {
            "path": "tools/ci/qira_artifact_integrity_check.py",
            "sha256": "5df0d12bfdec4c19cd0066be1f68a47d28feaa3e3beadd87d06d48bdc82a5526",
            "size_bytes": 2977
          },
          {
            "path": "factory_acceleration/phase_3_ci/README.md",
            "sha256": "b279556527acd05bf17aaaa89c08b52c06f50f3f6a21847e96bdc7163bf7a199",
            "size_bytes": 989
          },
          {
            "path": "factory_acceleration/phase_3_ci/PHASE_3_CI_QUALITY_LOOP_REGISTER_v1.json",
            "sha256": "86a117b01ff024d4de6e31c1eaa56aa5497d51cb97923fe58ab11256964e1f7c",
            "size_bytes": 1933
          },
          {
            "path": "factory_acceleration/phase_3_ci/CI_TOOL_ADOPTION_BOUNDARY_v1.md",
            "sha256": "827344d4bd093b726e304161051918cbbe5adb8262d37cd512c912ff447c0c69",
            "size_bytes": 909
          },
          {
            "path": "factory_acceleration/phase_3_ci/NEXT_ROUTE_AFTER_PHASE_3_CI_v1.md",
            "sha256": "0c5c11e2dbccff64cf6442a629ef782edbf880987b6536970a5aa14d5e2dfc2b",
            "size_bytes": 1153
          },
          {
            "path": "factory_acceleration/phase_3_ci/PHASE_3_LOCAL_STATIC_CHECK_RECEIPT_v1.md",
            "sha256": "5508366ff563a08de54071bda55439ef70f0eebd64a00edde23d2c104e7d871c",
            "size_bytes": 13739
          }
        ],
        "status": "PASS"
      }
    },
    {
      "exit_code": 0,
      "script": "tools/ci/qira_json_semantic_check.py",
      "stderr_size": 0,
      "stdout_json": {
        "check": "json_semantic_check",
        "results": [
          {
            "canonical_json_semantic_sha256": "01c31f43ecc9f4b7eec91c8f320da6c5321741201106fc79ce5dac538174682d",
            "duplicate_keys_detected": "NO",
            "parse_status": "PASS",
            "path": "factory_acceleration/phase_3_ci/PHASE_3_CI_QUALITY_LOOP_REGISTER_v1.json",
            "status": "PASS"
          }
        ],
        "status": "PASS"
      }
    },
    {
      "exit_code": 0,
      "script": "tools/ci/qira_claim_boundary_scan.py",
      "stderr_size": 0,
      "stdout_json": {
        "check": "claim_boundary_scan",
        "results": [
          {
            "forbidden_positive_patterns": [],
            "path": ".github/workflows/qira-governance-static.yml",
            "safe_token_count": 1,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": ".github/workflows/qira-python-quality-candidate.yml",
            "safe_token_count": 3,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "tools/ci/README.md",
            "safe_token_count": 11,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "tools/ci/qira_ci_local_static_runner.py",
            "safe_token_count": 11,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "tools/ci/qira_claim_boundary_scan.py",
            "safe_token_count": 11,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "tools/ci/qira_secret_surface_scan.py",
            "safe_token_count": 0,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "tools/ci/qira_json_semantic_check.py",
            "safe_token_count": 0,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "tools/ci/qira_artifact_integrity_check.py",
            "safe_token_count": 0,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "factory_acceleration/phase_3_ci/README.md",
            "safe_token_count": 9,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "factory_acceleration/phase_3_ci/PHASE_3_CI_QUALITY_LOOP_REGISTER_v1.json",
            "safe_token_count": 0,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "factory_acceleration/phase_3_ci/CI_TOOL_ADOPTION_BOUNDARY_v1.md",
            "safe_token_count": 5,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "factory_acceleration/phase_3_ci/NEXT_ROUTE_AFTER_PHASE_3_CI_v1.md",
            "safe_token_count": 9,
            "status": "PASS"
          },
          {
            "forbidden_positive_patterns": [],
            "path": "factory_acceleration/phase_3_ci/PHASE_3_LOCAL_STATIC_CHECK_RECEIPT_v1.md",
            "safe_token_count": 11,
            "status": "PASS"
          }
        ],
        "status": "PASS"
      }
    },
    {
      "exit_code": 0,
      "script": "tools/ci/qira_secret_surface_scan.py",
      "stderr_size": 0,
      "stdout_json": {
        "check": "secret_surface_scan",
        "results": [
          {
            "hit_classes": {},
            "path": ".github/workflows/qira-governance-static.yml",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": ".github/workflows/qira-python-quality-candidate.yml",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "tools/ci/README.md",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "tools/ci/qira_ci_local_static_runner.py",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "tools/ci/qira_claim_boundary_scan.py",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "tools/ci/qira_secret_surface_scan.py",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "tools/ci/qira_json_semantic_check.py",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "tools/ci/qira_artifact_integrity_check.py",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "factory_acceleration/phase_3_ci/README.md",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "factory_acceleration/phase_3_ci/PHASE_3_CI_QUALITY_LOOP_REGISTER_v1.json",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "factory_acceleration/phase_3_ci/CI_TOOL_ADOPTION_BOUNDARY_v1.md",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "factory_acceleration/phase_3_ci/NEXT_ROUTE_AFTER_PHASE_3_CI_v1.md",
            "status": "PASS"
          },
          {
            "hit_classes": {},
            "path": "factory_acceleration/phase_3_ci/PHASE_3_LOCAL_STATIC_CHECK_RECEIPT_v1.md",
            "status": "PASS"
          }
        ],
        "status": "PASS"
      }
    }
  ],
  "self_verifier_proof_limit": "LOCAL_STATIC_SELF_VERIFIER_NOT_INDEPENDENT_PROOF",
  "status": "PASS_WITH_LIMITS",
  "untracked_safe_preflight": "NO_UNRELATED_UNTRACKED_PATH_NAMES_EMITTED_BY_RUNNER",
  "workflows": [
    {
      "disabled_gate_present": true,
      "manual_dispatch_present": true,
      "path": ".github/workflows/qira-governance-static.yml",
      "pull_request_trigger_present": false,
      "push_trigger_present": false,
      "schedule_trigger_present": false,
      "workflow_run_trigger_present": false
    },
    {
      "disabled_gate_present": true,
      "manual_dispatch_present": true,
      "path": ".github/workflows/qira-python-quality-candidate.yml",
      "pull_request_trigger_present": false,
      "push_trigger_present": false,
      "schedule_trigger_present": false,
      "workflow_run_trigger_present": false
    }
  ],
  "yaml_syntax_validity": "NOT_PROVEN"
}
```
