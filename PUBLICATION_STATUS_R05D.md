# R0.5D Publication Status — Declarative External-Clean Corpus (halueval_qa)

**Status:** COMPLETED — 6 July 2026
**Version:** v1.0.0
**Author:** Gonzalo Emir Durante — Origin Node, Project Manifold 0.56
**Registry:** TAD EX-2026-18792778 (Argentina)
**Repository:** https://github.com/Leesintheblindmonk1999/Project_Manifold_056

---

## 1. Summary

R0.5D is a declarative external-clean corpus built for the `halueval_qa` (factual QA) track. Its primary methodological objective was to reduce the **length confound** that dominated the R1 v1.0.7 baseline (AUC 0.957, C/B ratio 2.07). By filtering for `B_hallucination` ≥ 15 words and generating `C_clean` as declarative factual prose from `A_clean` only, the lexical baseline was reduced to AUC 0.749 with a C/B length ratio of 1.29.

| Metric | Value |
|--------|-------|
| Track | halueval_qa |
| B filter | ≥ 15 words (10,000 → 2,510 pairs) |
| Generations attempted | 1,200 |
| Generations OK | 1,197 (99.75%) |
| C_clean accepted | **744 (62%)** |
| Lexical baseline AUC (test) | **0.749** |
| C/B length ratio (mean) | **1.29** |

**Methodological Finding:** The `long_b_ngram_overlap` check was found to generate false positives in QA tracks due to legitimate topic overlap. Threshold adjustment (2 → 4 shared 5-grams) increased acceptance from 46% to 62%. This is documented in PATCH-7.

---

## 2. Artifacts

###  Publication Artifact

| Artifact | SHA-256 |
|----------|---------|
| `SAS_R05D_halueval_qa_v1_0_0.zip` | `67171A10DD3E56791DF3F2EE8F23F09C241F3EFBA93EBCD6F82863A46BBC171C` |

### Content Verification

The publication artifact `SAS_R05D_halueval_qa_v1_0_0.zip` was generated from the local working copy with the following structure:

SAS_R05D_halueval_qa_v1_0_0/
├── README.md
├── SHA256SUMS.txt
├── ZENODO_METADATA.json
├── generations/
│   ├── r05d_generations.jsonl
│   └── raw_generations/              # 1200 generated C_clean texts
├── verification/
│   ├── VERIFICATION_MANIFEST.json
│   ├── r05d_verification.jsonl
│   ├── accepted_C_clean/             # 744 accepted C_clean files
│   └── rejected_C_clean_private/     # 456 rejected candidates
└── form_analysis/
    ├── FORM_ANALYSIS_REPORT.json
    ├── form_metrics_by_pair.csv
    └── lexical_baseline_rows.csv

**Verification:** All files have been validated against the manifest. The package passes SHA-256 checksum verification (see `SHA256SUMS.txt` inside the artifact for per-file hashes).

---

## 3. Key Results & Boundary

### Defensible Claims

1.  **744 accepted declarative C_clean pairs** were generated for `halueval_qa` under the B ≥ 15 words filter, with 99.75% generation success.
2.  **The length confound was substantially reduced.** C/B ratio dropped from 2.07 (R1 v1.0.7) to 1.29. Lexical baseline AUC dropped from 0.957 to 0.749.
3.  **B_hallucination was successfully quarantined.** All `C_clean` were generated from `A_clean` only. Contamination checks ran post-generation only.
4.  **`long_b_ngram_overlap` adjustment.** In QA tracks, this check was found to measure legitimate topic overlap, not contamination. Threshold adjusted from 2 to 4 shared 5-grams.

### Claims Not Supported

1.  **SAS structural modules outperform the lexical baseline on this corpus.** That is R1-D, which has not been run yet.
2.  **This is a universal hallucination detection benchmark.** It is `halueval_qa`-specific.
3.  **κD = 0.56 is validated as a hallucination threshold on this corpus.**
4.  **The verifier detects novel factual fabrication absent from both `A_clean` and `B_hallucination`.** Manual spot-check is required.

---

## 4. Next Steps: R1-D

This corpus is explicitly designed for the next milestone:

*   **Goal:** Run SAS structural modules (Flow, CRE, Negation, NIG, TDA) over the 744 accepted pairs using the R1 scaffold (v1.0.4+).
*   **Key Requirement:** Report structural composite F1 alongside the established lexical baseline (AUC 0.749).
*   **Split:** Must reuse `r05d_common.sha_bucket` from `generation/verification` to ensure source-level split compatibility.

---

## 5. References

*   **R1 v1.0.7 DOI:** https://zenodo.org/records/21034155
*   **SAS Standard DOI:** https://doi.org/10.5281/zenodo.19702379
*   **Repository:** https://github.com/Leesintheblindmonk1999/Project_Manifold_056