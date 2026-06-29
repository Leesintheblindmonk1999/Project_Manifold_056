# R1 Real Results v1.0.7

## Technical closure

**Freeze ID:** `R1_REAL_LOCAL_V107_STRUCTURAL_EVAL_PASS`  
**Runner:** `r1_module_runner_v1.0.7`  
**Integrity manifest SHA-256:** `eb2899292ae72384f9eff8e8fab8e57f09b00ea0962ee822a40fbcdac2574b4c`

## Dataset and execution

| Item | Value |
|---|---:|
| Source groups | 2349 |
| Total rows | 4698 |
| Validation rows | 938 |
| Test rows | 3760 |
| Full runner v1.0.7 rows | 4698 / 4698 |
| Full runner runtime | ~26.05s |
| NIG conversion errors | 0 / 4698 |

## Baseline boundary

| Baseline | Validation AUC | Validation F1 | Test AUC | Test F1 |
|---|---:|---:|---:|---:|
| Lexical baseline | 0.9880 | 0.9936 | 0.9963 | 0.9968 |

## Main structural result

| Composite | Test F1 | Precision | Recall | Accuracy |
|---|---:|---:|---:|---:|
| Flow + CRE + Negation, score >= 1 | 0.8717 | 0.9952 | 0.7755 | 0.8859 |

## Correct claim

SAS-light structural modules produce a reproducible, non-runtime, interpretable signal on the R1 real split.

## Incorrect claim

SAS-light does not outperform the lexical baseline in this release.
