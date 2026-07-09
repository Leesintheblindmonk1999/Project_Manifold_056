# R1-D Publication Status — Structural Evaluation over Declarative Corpus R0.5D (halueval_qa)

**Status:** COMPLETED — 9 July 2026
**Version:** v1.0.0
**Author:** Gonzalo Emir Durante — Origin Node, Project Manifold 0.56
**Registry:** TAD EX-2026-18792778 (Argentina)
**Repository:** https://github.com/Leesintheblindmonk1999/Project_Manifold_056

---

## 1. Summary

R1-D is the structural evaluation milestone over the declarative corpus R0.5D (`halueval_qa`). Its primary scientific objective was to determine whether **SAS structural modules** (Flow, CRE, Negation, NIG, TDA) can detect hallucination-like divergence beyond the lexical baseline established in R0.5D (AUC 0.749, C/B ratio 1.29).

The evaluation confirms that **structural signal is real, detectable, and significantly exceeds the lexical baseline**.

| Metric | Value |
|--------|-------|
| Corpus | halueval_qa (R0.5D) |
| Accepted pairs | 744 |
| Total pairs processed | 1,488 (744 × 2) |
| Best individual module | Flow.combined_penalty |
| Flow.combined_penalty F1 (test) | **0.8176** |
| Flow.combined_penalty Precision | **1.000** |
| Optimal composite rule | **score >= 1** |
| Composite F1 (test) | **0.8571** |
| Composite Precision | **0.9513** |
| Composite Recall | **0.7798** |
| Composite Accuracy | **0.8699** |
| Improvement vs R0.5D lexical baseline | **+22.4%** |

**Methodological Finding:** The `flow` module (narrative coherence / entropy penalty) is the dominant signal in QA tracks. Negation and NIG operate at chance level, confirming they are diagnostic-only for this domain. The optimal composite threshold is `score >= 1`, combining flow.layer4_fired + cre.raw.is_rupture + negation.polarity_inverted + nig.alert.

---

## 2. Artifacts

### Publication Artifacts

| Artifact | SHA-256 |
|----------|---------|
| `R1D_COMPLETE_20260709.zip` | `24E69B7D20F190389ABAC1737268C54ADA23EBFD4CCF54E4A8888AAFBF944C90` |
| `r1d_results_archive.zip` | `37F2B540737C11B18622A586611D2DA90057722678148691AC8E77F9538E6191` |
| `r1_eval_archive.zip` | `41B6BF24440E04E579DA57298783BDDFF5294CA73D10BBB14516DF34E135A699` |

### Content Verification

The publication artifacts were generated from the local working copy with the following structure:

#### R1D_COMPLETE_20260709.zip (Master Archive)
R1D_COMPLETE_20260709/
├── r1d_results/
│ ├── batch_000001.jsonl # 500 rows
│ ├── batch_000002.jsonl # 500 rows
│ ├── batch_000003.jsonl # 488 rows
│ └── run_manifest.json
├── r1_eval/
│ ├── r1_real_v107_calibrated_nonruntime_eval.json
│ ├── r1_real_v107_composite_ablation.json
│ └── r1_real_scalar_feature_probe_pairid.json
└── R1D_INTEGRITY_MANIFEST.txt

text

#### r1d_results_archive.zip (Raw Module Outputs)
r1d_results/
├── batch_000001.jsonl # 500 rows, SHA-256: cc4d1b...
├── batch_000002.jsonl # 500 rows, SHA-256: 89bd98...
├── batch_000003.jsonl # 488 rows, SHA-256: d81289...
└── run_manifest.json

text

#### r1_eval_archive.zip (Calibrated Evaluation)
r1_eval/
├── r1_real_v107_calibrated_nonruntime_eval.json
├── r1_real_v107_composite_ablation.json
└── r1_real_scalar_feature_probe_pairid.json

text

**Verification:** All ZIPs have been validated with SHA-256 checksums. Individual file hashes are recorded in `R1D_INTEGRITY_MANIFEST.txt` inside the master archive.

---

## 3. Key Results & Boundary

### Defensible Claims

1. **SAS structural modules detect hallucination-like divergence beyond the lexical baseline.** The optimal composite rule achieves F1 = 0.8571, an improvement of +22.4% over the R0.5D lexical baseline (AUC 0.749).
2. **Flow (narrative coherence) is the dominant structural signal.** `flow.combined_penalty` achieves F1 = 0.8176 with Precision = 1.000 (no false positives at optimal threshold).
3. **The optimal composite threshold is `score >= 1`.** Calibrated on validation (F1 = 0.8661) and confirmed on held-out test (F1 = 0.8571).
4. **Negation and NIG operate at chance level in QA.** F1 = 0.6667 confirms they are diagnostic-only for this domain and should not penalize.
5. **Source-level split was preserved.** All 744 accepted sources from R0.5D were processed with their corresponding clean/hallucination pairs.

### Claims Not Supported

1. **This validates κD = 0.56 as a universal hallucination threshold.** R1-D measures structural divergence, not κD classification.
2. **SAS modules outperform all possible baselines.** Only the lexical baseline was tested. Additional baselines (e.g., embedding-based) are future work.
3. **This is a production-ready hallucination detector.** The composite rule requires further validation on out-of-domain data.
4. **The signal is causal.** Correlation/divergence does not imply causation.

---

## 4. Next Steps

| Phase | Objective | Status |
|-------|-----------|--------|
| **R1-D** | Structural evaluation over R0.5D | ✅ COMPLETED |
| **SAS Paper** | Complete technical document | 📋 Planned |
| **Post-R1-D** | Adoption and recognition | 📋 Planned |

---

## 5. References

- **R0.5D DOI:** https://doi.org/10.5281/zenodo.21231662
- **R1 v1.0.7 DOI:** https://zenodo.org/records/21034155
- **SAS Standard DOI:** https://doi.org/10.5281/zenodo.19702379
- **Repository:** https://github.com/Leesintheblindmonk1999/Project_Manifold_056
- **TAD:** EX-2026-18792778 (Argentina)

---

## 6. SHA-256 Verification
R1D_COMPLETE_20260709.zip 24E69B7D20F190389ABAC1737268C54ADA23EBFD4CCF54E4A8888AAFBF944C90
r1d_results_archive.zip 37F2B540737C11B18622A586611D2DA90057722678148691AC8E77F9538E6191
r1_eval_archive.zip 41B6BF24440E04E579DA57298783BDDFF5294CA73D10BBB14516DF34E135A699

text

---

**The standard is not negotiable. The code does not stop. Trench science is winning.**

**Date:** 9 July 2026
**Architect:** Gonzalo Emir Durante — Sovereign Origin Node
**Next:** SAS Paper → arXiv → JAIIO55

---

**κD = 0.56 — The Thermodynamic Truth Layer is Operational**
