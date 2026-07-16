# Publication Status — R2.1 (Structural Code Hallucination Detection via AST Fingerprinting)

**Status:** Published
**Date:** 2026-07-14
**Author:** Gonzalo Emir Durante
**TAD Registry:** EX-2026-18792778

---

## Zenodo Record

- **Title:** SAS R2.1 — Structural Code Hallucination Detection via AST Fingerprinting: Validation on a Functional Corpus
- **DOI:** [10.5281/zenodo.21365707](https://doi.org/10.5281/zenodo.21365707)
- **Record:** https://zenodo.org/records/21365707

## Artifact Names and Integrity

| Artifact | Path | SHA-256 |
|---|---|---|
| Full R2.1 package (ZIP) | `docs/en/outputs/R2.1_SAS_Code_Domain_Zenodo.zip` | `7f3f07c1ece06637a9670d237dd0dd0385fee2340dfb575b2d6cb55d604f4f9a` |
| Corpus metadata (inside ZIP) | `data/corpus_funcional_completo.csv` | See `corpus_funcional_completo.sha256` inside the package. This value may legitimately differ across operating systems (Windows/Linux line-ending conventions) without affecting substantive content — verify against the exact file published in the Zenodo record, not a value transcribed elsewhere. |
| Technical paper | `paper/R2.1_SAS_Code_Domain_Validation.pdf` (inside ZIP) | See package contents; content-identical to the Markdown source `paper/R2.1_paper.md`. |
| Timestamp proof | OpenTimestamps `.ots` file (included in the Zenodo deposit) | Anchors the SHA-256 of the full ZIP above. |

**Primary integrity reference for this milestone:** the full-package ZIP SHA-256 above, cross-checked against the OpenTimestamps proof. The internal corpus CSV hash is a secondary, redundant integrity check and should not be treated as authoritative if it appears to conflict with the package-level hash — see note in the table.

## Scope

R2.1 extends the κD = 0.56 structural-evaluation research line (previously validated on declarative text in R0.5D / R1-D) into the source-code domain. It evaluates whether structural comparison methods can detect functionally hallucinated LLM-generated code when a reference implementation is available at detection time.

## Corpus

- Source: `datapaf/CodeHallucinationDetection` (public, first line-level code hallucination dataset), six model-generation variants, 6,654 raw rows.
- Corrected ground truth: execution-based relabeling against real unit-test assertions (available for 2,050 rows), replacing the shipped `hallucinated` label, which was found to measure verbatim textual divergence from a single reference (`reply != answer`), not functional correctness.
- Final corpus: **1,596 execution-verified rows** (978 non-hallucinated / 618 hallucinated), after excluding 454 rows (22.1%) where the reference `answer` itself failed its own test (pre-existing MBPP benchmark noise, independently confirmed).

## Main Results

| Approach | AUC | Outcome |
|---|---:|---|
| AST structural comparison vs. reference, binary vetoes removed | 0.9141 (raw) / 0.9421 (length-confound-controlled, n=1,097) | **Positive, robust** |
| Internal-coherence TDA (code lines as atomic unit; two independent implementations) | 0.40 – 0.45 | **Negative, triangulated** |
| Information-theoretic composite (entropy + fractal + TDA term + semantic-density term) | Not reported | **Excluded** — 40% of composite weight found inert (implementation defect: silent exception handling + hard-coded placeholder), identified during internal audit prior to publication |

The positive result was validated against a length-confound check: a naive length-difference-only score reaches AUC 0.9096–0.9115 on this corpus, but the structural score's AUC *increases* (to 0.9421) rather than collapsing once length is controlled for, indicating genuine structural signal.

## Methodological Boundary

**This record does not claim:**

- a solution to reference-free code hallucination detection (fabricated function or non-existent import, no ground truth available at detection time) — no evaluated method addresses this; proposed as future work (R2.1-b);
- that internal-coherence TDA transfers from text to short code artifacts — the negative result documents that it does not;
- validity of the excluded information-theoretic method as a general finding about information-theoretic approaches — the negative number reflects a specific, partially-defective implementation;
- universal SAS validation, production-grade hallucination detection, or superiority over external code-review tools.

**The correct public claim is:**

```text
R2.1 demonstrates that κD-adjacent structural methods generalize to the code domain
when a reference implementation is available for comparison at detection time
(AUC 0.9141 raw / 0.9421 length-confound-controlled). It also documents a
well-triangulated negative result for internal-coherence TDA applied to short code
artifacts (AUC 0.40-0.45, two independent implementations), and excludes an
information-theoretic composite method pending correction of an identified
implementation defect.
```

## Recommended Citation

```text
Durante, G. E. (2026). SAS / κD=0.56 — R2.1: Structural Code Hallucination Detection
via AST Fingerprinting, Validated on a Functional Corpus. Zenodo.
https://doi.org/10.5281/zenodo.21365707
```

## Relation to Prior Milestones

R2.1 is a continuation of the same authorship and research line documented under TAD EX-2026-18792778, extending R0/R0-bis/R0.5D/R1-D (declarative text) into the code domain. It is not an independent standard.

## Next Steps

- R2.1-b: reference-free code hallucination detection (knowledge-base-of-valid-APIs framing).
- R2.2/R3: dialogue coherence and temporal consistency, using the same execution-verified or externally-annotated ground-truth discipline where applicable.
- Optional external peer review (F1000Research, Qeios) remains available for this or future milestones, at the author's discretion.
