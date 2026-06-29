# SAS / kD=0.56 - R1 Real Local Structural Evaluation v1.0.7

**Author:** Gonzalo Emir Durante  
**Project:** Symbiotic Autoprotection System (SAS) / kD=0.56  
**Release type:** Technical report and reproducibility snapshot  
**Freeze ID:** `R1_REAL_LOCAL_V107_STRUCTURAL_EVAL_PASS`  
**Runner:** `r1_module_runner_v1.0.7`

## Abstract

This report documents the R1 real local structural evaluation of SAS / kD=0.56. The snapshot validates an end-to-end real-data pipeline with paired CLEAN and HALLUCINATION candidates, full light-runner execution, corrected `pair_id`/`source_id` joins, NIG JSON serialization in v1.0.7, and validation-calibrated non-runtime structural evaluation on a held-out test split.

The best non-runtime structural composite, using Flow coherence, CRE rupture, and Negation inversion with score >= 1, achieved test F1=0.8717, precision=0.9952, recall=0.7755, and accuracy=0.8859. These results demonstrate reproducible and interpretable structural signal in SAS-light modules. They do not outperform the lexical baseline, which achieved test AUC=0.9963 and test F1=0.9968. The correct interpretation is therefore structural signal confirmation, not final detector superiority.

## 1. Scope

This release is a local reproducibility snapshot for R1 real structural evaluation. It preserves outputs, scripts, logs, and methodological boundaries of the v1.0.7 pass.

Supported claim:

> SAS-light structural modules produce a reproducible, non-runtime, interpretable signal on the R1 real split, with the best Flow + CRE + Negation composite achieving test F1=0.8717, precision=0.9952, recall=0.7755, and accuracy=0.8859.

Not supported: final validation, general deployment readiness, or superiority over lexical baselines.

## 2. Dataset

| Split | Rows |
|---|---:|
| Validation | 938 |
| Test | 3760 |
| Total | 4698 |

The dataset contains 2349 paired source groups, each represented by one CLEAN and one HALLUCINATION candidate.

## 3. Runner execution

| Item | Result |
|---|---:|
| Rows processed | 4698 / 4698 |
| Runtime | approximately 26.05 seconds |
| Aborted due runtime limit | No |
| Runner schema | `r1_module_runner_v1.0.7` |
| Output manifest | `outputs/r1_results_light_full_real_v107/run_manifest.json` |

## 4. NIG serialization patch

v1.0.7 introduced `ensure_jsonable()` and corrected the NIG conversion path.

| Field | Result |
|---|---:|
| NIG status OK | 4698 |
| `conversion_error` present | 0 |
| Import path | `core.nig_engine_v1.run_nig` |
| Source-aware | False |
| Role | Diagnostic-only / standalone |

NIG is technically serialized correctly. Because it remains source-unaware in this local configuration, it should be treated as diagnostic-only for source-candidate divergence.

## 5. Lexical baseline

| Split | AUC | F1 |
|---|---:|---:|
| Validation | 0.9880 | 0.9936 |
| Test | 0.9963 | 0.9968 |

The lexical baseline remains stronger than the structural composite.

## 6. Non-runtime structural evaluation

Runtime-derived features were excluded from the main structural claim. Thresholds were calibrated on validation and evaluated on held-out test.

### Best single structural signals

| Signal | Direction / Threshold | Test F1 | Precision | Recall | Accuracy |
|---|---|---:|---:|---:|---:|
| Flow combined penalty | low-is-hall, threshold 0.85 | 0.8176 | 1.0000 | 0.6915 | 0.8457 |
| Flow layer4 fired | high-is-hall, threshold 1.0 | 0.8176 | 1.0000 | 0.6915 | 0.8457 |
| CRE Ricci scalar max | high-is-hall, threshold 0.006275 | 0.7344 | 0.9936 | 0.5824 | 0.7894 |
| CRE rupture | high-is-hall, threshold 1.0 | 0.6707 | 0.9927 | 0.5064 | 0.7513 |

### Composite ablation

| Rule | Test F1 | Precision | Recall | Accuracy |
|---|---:|---:|---:|---:|
| Flow only | 0.8176 | 1.0000 | 0.6915 | 0.8457 |
| CRE only | 0.6707 | 0.9927 | 0.5064 | 0.7513 |
| Negation only | 0.4777 | 1.0000 | 0.3138 | 0.6569 |
| NIG only | 0.1430 | 0.6881 | 0.0798 | 0.5218 |
| Flow + CRE | 0.8416 | 0.9949 | 0.7293 | 0.8628 |
| Flow + Negation | 0.8610 | 1.0000 | 0.7559 | 0.8779 |
| Flow + CRE + Negation | **0.8717** | **0.9952** | **0.7755** | **0.8859** |
| Flow + CRE + Negation + NIG | 0.8571 | 0.9513 | 0.7798 | 0.8699 |

## 7. Interpretation

Flow is the dominant structural signal. CRE and Negation add recall without substantially degrading precision. NIG was fixed at the serialization level, but does not provide strong discriminative value in the current source-unaware configuration.

## 8. Claim boundary

Supported:

- R1 real local v1.0.7 pipeline pass.
- NIG JSON serialization pass.
- Flow/CRE/Negation composite produces non-trivial structural signal.
- Held-out test evaluation reports F1=0.8717, precision=0.9952, recall=0.7755, accuracy=0.8859.

Not supported:

- Superiority over lexical baselines.
- Final hallucination detector status.
- Generalization beyond this R1 split.
- Scientific use of runtime-derived features as structural evidence.
- NIG as a source-aware divergence vote in this configuration.

## 9. Reproducibility package

Primary freeze directory expected in the local repository:

`outputs/r1_freeze_real_v107/`

Integrity manifest:

`outputs/r1_freeze_real_v107/INTEGRITY_MANIFEST_R1_REAL_LOCAL_v107.json`

Integrity manifest SHA-256:

`eb2899292ae72384f9eff8e8fab8e57f09b00ea0962ee822a40fbcdac2574b4c`

## 10. Recommended citation label

Durante, G. E. (2026). *SAS / kD=0.56 - R1 Real Local Structural Evaluation v1.0.7*. Technical report and reproducibility snapshot.
