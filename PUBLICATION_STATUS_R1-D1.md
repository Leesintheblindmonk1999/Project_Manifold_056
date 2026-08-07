# R1-D Publication Status — Structural Evaluation over Declarative Corpus R0.5D (halueval_qa)

**Status:** CORRECTED — 29 July 2026 (original publication: 9 July 2026)
**Version:** v1.1.0 — ERRATUM to v1.0.0
**Author:** Gonzalo Emir Durante — Origin Node, Project Manifold 0.56
**Registry:** TAD EX-2026-18792778 (Argentina)
**Repository:** https://github.com/Leesintheblindmonk1999/Project_Manifold_056
**Zenodo Record:** https://zenodo.org/records/21282332

---

## ERRATUM (read before anything else in this document)

The performance table in v1.0.0 of this document (published 9 July 2026) reported results that were **copied from the R1 v1.0.7 ablation table** (Zenodo DOI 10.5281/zenodo.21034155, corpus of 4,698 rows) rather than computed on the R1-D / R0.5D corpus (1,488 rows) that this milestone is actually about. All three headline figures — Flow-only, the "Composite" row, and the "Simple composite" row — match R1's corresponding rows to four decimal places across every metric, which is not possible by coincidence.

This was found during an independent re-verification effort in July 2026, using the actual per-pair module outputs stored in the original `r1d_results_archive.zip` (`batch_000001.jsonl` through `batch_000003.jsonl`) from the 9 July 2026 run — not a re-run of the modules, the original stored data itself. **Section 1 below has been corrected. No other section of this document, and no artifact hash, is affected** — the underlying data and code artifacts were always correct; only the interpretive performance claims built on top of them were wrong.

This correction is published following the same standard of documentary rigor already applied to ground-truth defects found in external benchmarks in R2.1 and R2.1-b: documented plainly, with the verification method disclosed, rather than silently amended.

---

## 1. Summary (Corrected)

R1-D is the structural evaluation milestone over the declarative corpus R0.5D (`halueval_qa`). Its primary scientific objective was to determine whether SAS structural modules (Flow, CRE, Negation, NIG) can detect hallucination-like divergence beyond the lexical baseline established in R0.5D (AUC 0.749, C/B ratio 1.29).

The corrected evaluation shows that the binary-voting composite rule (`score >= 1` over `flow.layer4_fired`, `cre.raw.is_rupture`, `negation.polarity_inverted`, and optionally `nig.alert`) performs **well above chance but well below the lexical baseline** on this corpus, and well below what was originally reported.

| Metric | Value |
|--------|-------|
| Corpus | halueval_qa (R0.5D) |
| Accepted source pairs | 744 |
| Paired examples (rows evaluated) | 1,488 (744 × 2) |
| **Flow only (`layer4_fired`), F1** | **0.3485** |
| Flow only, Precision | 0.7478 |
| Flow only, Recall | 0.2272 |
| Flow only, Accuracy | 0.5753 |
| **Composite: Flow+CRE+Negation (`score>=1`), F1** | **0.5230** |
| Composite, Precision | 0.5617 |
| Composite, Recall | 0.4892 |
| Composite, Accuracy | 0.5538 |
| **Composite: Flow+CRE+Negation+NIG (`score>=1`), F1** | **0.5267** |
| Composite+NIG, Precision | 0.5436 |
| Composite+NIG, Recall | 0.5108 |
| Composite+NIG, Accuracy | 0.5410 |
| Lexical baseline (R0.5D, for comparison) | AUC 0.749 |

**Corrected Methodological Finding:** Neither individual modules nor the binary-voting composite outperform the R0.5D lexical baseline on this corpus. `flow.layer4_fired` alone reaches high precision (0.7478) but low recall (0.2272) — it fires rarely, but is usually right when it does. Adding CRE, Negation, and NIG to the vote increases recall at a steeper cost to precision, netting a modest F1 improvement over Flow alone but not approaching the lexical baseline. This is a materially different, and more modest, conclusion than the one originally published.

---

## 2. Artifacts (Unaffected by This Correction)

### Publication Artifacts

| Artifact | SHA-256 |
|----------|---------|
| R1D_Paper_v1.0.0.pdf | C7F5C6AAF96AB1EB299D28D50B483A3C9C5220666DA16B487D609CCF2341491D |
| R1D_COMPLETE_20260709.zip | 24E69B7D20F190389ABAC1737268C54ADA23EBFD4CCF54E4A8888AAFBF944C90 |
| r1d_results_archive.zip | 37F2B540737C11B18622A586611D2DA90057722678148691AC8E77F9538E6191 |
| r1_eval_archive.zip | 41B6BF24440E04E579DA57298783BDDFF5294CA73D10BBB14516DF34E135A699 |

**Note:** the artifacts themselves — the corpus, the per-pair module outputs in `r1d_results_archive.zip` — are correct and are, in fact, the source used to compute the correction above. Only the summary table and narrative claims in the original v1.0.0 publication status were wrong. If citing this milestone's data directly (not the original summary claims), no re-download or re-verification of the ZIPs is required.

### Content Verification

```
R1D_COMPLETE_20260709/
├── r1d_results/
│   ├── batch_000001.jsonl          # 500 rows
│   ├── batch_000002.jsonl          # 500 rows
│   ├── batch_000003.jsonl          # 488 rows
│   └── run_manifest.json
├── r1_eval/
│   ├── r1_real_v107_calibrated_nonruntime_eval.json
│   ├── r1_real_v107_composite_ablation.json   # NOTE: this file's numbers are R1's, see erratum
│   └── r1_real_scalar_feature_probe_pairid.json
└── R1D_INTEGRITY_MANIFEST.txt
```

**Important:** `r1_real_v107_composite_ablation.json`, despite living inside the R1-D archive, contains R1's own ablation results (4,698-row corpus), not a fresh computation over R0.5D. This filename/content mismatch is the direct, traceable source of the error corrected in this document.

---

## 3. Key Results & Boundary (Corrected)

### Defensible Claims

1. The binary-voting composite (`score >= 1`) over Flow, CRE, and Negation detects hallucination-like divergence on R0.5D at F1 = 0.5230 — well above a random classifier (F1 ≈ 0.5 at this class balance), but **below the lexical baseline (AUC 0.749) established for this same corpus**.
2. `flow.layer4_fired` alone is a high-precision, low-recall signal (Precision 0.7478, Recall 0.2272) — when it fires, it is usually right, but it fires infrequently on this corpus.
3. Adding NIG to the vote (`Flow+CRE+Negation+NIG`) trades precision for recall (F1 0.5267 vs. 0.5230) — a small, not clearly significant, difference.
4. Source-level split was preserved; all 744 accepted sources from R0.5D were processed with their corresponding clean/hallucination pairs.

### Claims Not Supported (Expanded)

1. ~~The optimal composite rule achieves test F1 = 0.8717, an improvement of +22.4% over the lexical baseline.~~ **Retracted.** The real composite F1 on R0.5D is 0.5230–0.5267, below the lexical baseline.
2. This validates κD = 0.56 as a universal hallucination threshold. R1-D measures structural divergence, not κD classification.
3. SAS modules outperform all possible baselines. On this corpus, they do not outperform the tested lexical baseline.
4. This is a production-ready hallucination detector. The composite rule underperforms a simple lexical baseline on this corpus and requires further work before any production claim.
5. The signal is causal. Correlation/divergence does not imply causation.

---

## 4. Next Steps

| Phase | Objective | Status |
|-------|-----------|--------|
| R1-D | Structural evaluation over R0.5D | COMPLETED (corrected 29 July 2026) |
| R1-D Erratum | Correct copy-paste error in headline metrics | COMPLETED — this document |
| Tribunal correlation study | Cross-correlate production + R0-bis baseline modules on R0.5D | In progress |
| Module improvement pass | Revisit Flow/CRE/Negation/NIG individually against real R0.5D performance | Planned |
| SAS Paper | Complete technical document, with corrected figures | Planned |

---

## 5. References

- R1-D Zenodo Record: https://zenodo.org/records/21282332
- R0.5D DOI: https://doi.org/10.5281/zenodo.21231662
- R1 v1.0.7 DOI: https://zenodo.org/records/21034155 (source of the originally miscopied figures)
- SAS Standard DOI: https://doi.org/10.5281/zenodo.19702379
- Repository: https://github.com/Leesintheblindmonk1999/Project_Manifold_056
- TAD: EX-2026-18792778 (Argentina)

---

## 6. SHA-256 Verification

```
R1D_Paper_v1.0.0.pdf           C7F5C6AAF96AB1EB299D28D50B483A3C9C5220666DA16B487D609CCF2341491D
R1D_COMPLETE_20260709.zip      24E69B7D20F190389ABAC1737268C54ADA23EBFD4CCF54E4A8888AAFBF944C90
r1d_results_archive.zip        37F2B540737C11B18622A586611D2DA90057722678148691AC8E77F9538E6191
r1_eval_archive.zip            41B6BF24440E04E579DA57298783BDDFF5294CA73D10BBB14516DF34E135A699
```

---

*This erratum does not change any artifact hash. It corrects the interpretive summary published alongside those artifacts. Verification method: direct extraction of `flow.layer4_fired`, `cre.raw.is_rupture`, `negation.polarity_inverted`, and `nig.alert` from all 1,488 rows across the three original `batch_*.jsonl` files, re-scored against the real corpus labels.*

Date of correction: 29 July 2026
Architect: Gonzalo Emir Durante
