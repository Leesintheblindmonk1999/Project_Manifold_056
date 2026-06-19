# SAS / Project Manifold kD-0.56 - R0.5P-1 Publication Status

**Status date:** 2026-06-18  
**Project:** SAS / Project Manifold 0.56  
**Track:** R0.5P-1 - Historical Query Paraphrase external-clean audit  
**Repository context:** Project Manifold 0.56 root-level publication status file  
**Author / maintainer:** Gonzalo Emir Durante  
**Purpose:** Freeze the public status of the R0.5P-1 milestone after Zenodo, GitHub, and TAD documentation actions.

---

## 1. Executive Status

R0.5P-1 is the first validated track-conditioned external-clean prompt-paraphrase audit in the SAS / Project Manifold kD-0.56 research line.

This status file records the publication and traceability state of the R0.5P-1 milestone after:

- source-shape discovery;
- track reformulation from factual external-clean generation to prompt paraphrase;
- v0.2.0 -> v0.2.3 script hardening;
- smoke, alpha, beta, and main-scale runs;
- main-1200 rejection analysis;
- external audit;
- v1.0.1 documentation patch;
- Zenodo publication;
- GitHub artifact placement;
- TAD executive documentation submission.

This file is intentionally administrative and evidentiary. It does not replace the paper, README, manifests, source packages, or Zenodo record.

---

## 2. Zenodo Record

| Field | Value |
|---|---|
| Zenodo record URL | `https://zenodo.org/records/20742205` |
| Version DOI | `10.5281/zenodo.20742205` |
| Release version | `v1.0.1` |
| Suggested upload type | `Publication / Technical note` or `Dataset`, depending on Zenodo classification |
| Main title | `R0.5P-1 External-Clean Historical Query Paraphrase Audit for SAS/kD-0.56: A Track-Conditioned Prompt-Paraphrase Study` |

> Note: if Zenodo displays both a concept DOI and a version DOI, the version DOI should remain `10.5281/zenodo.20742205`, while the concept DOI should be copied from the Zenodo UI if needed.

---

## 3. Zenodo Files Uploaded / Release File Set

Minimum public Zenodo release set:

| File | Role |
|---|---|
| `SAS_R0_5P1_Historical_Query_Paraphrase_Zenodo_Package_v1_0_1.zip` | Main traceable package: paper, methods, data summaries, figures, metadata, audit response, manifests, hashes, and source artifacts |
| `SAS_R0_5P1_Historical_Query_Paraphrase_Zenodo_Package_v1_0_1.zip.sha256.txt` | SHA-256 digest for the main Zenodo package |
| `SAS_R0_5P1_Historical_Query_Paraphrase_Paper_v1_0_1.pdf` | Human-readable paper, uploaded separately for visibility |

Recommended optional companion release files, if uploaded:

| File | Role |
|---|---|
| `SAS_R0_5P1_runs_v0_1_9_to_v0_2_3_<timestamp>.zip` | Local run archive containing run folders, manifests, verification reports, and outputs from v0.1.9 through v0.2.3 |
| `SAS_R0_5P1_runs_v0_1_9_to_v0_2_3_<timestamp>.zip.sha256.txt` | SHA-256 digest for the local run archive |

---

## 4. Cryptographic Hashes

### 4.1 Main Zenodo Package

```text
SAS_R0_5P1_Historical_Query_Paraphrase_Zenodo_Package_v1_0_1.zip
SHA-256:
48db407a59f612baa0d787331fed5fc9ed58ccd80c05bb569b83d8b1fcf196d0
```

### 4.2 R0.5P-1 v0.2.3 Source Package

```text
r05_external_clean_scripts_v0_2_3.zip
SHA-256:
1457818882720bc2f3a420e6992627776d1cea00b0c840533cd3be382895d501
```

### 4.3 TAD R0.5P-1 Executive Dossier Package

```text
Dossier_TAD_R05P1_SAS_kD056_v1_0_0_package.zip
SHA-256:
641b92f4a4ec8776850c4736312dd2325d558f271903c9d7d9f053d39561d19b
```

### 4.4 Run Archive Hash

If a local run archive was uploaded separately, record it here:

```text
SAS_R0_5P1_runs_v0_1_9_to_v0_2_3_<timestamp>.zip
SHA-256:
TODO: paste local run archive hash if uploaded separately.
```

---

## 5. Main R0.5P-1 Results

### 5.1 Preflight

```text
Raw A_clean files discovered:        21,008
Eligible after preflight:            18,964
Skipped by preflight:                 2,044
  mojibake_or_encoding_artifact:      1,232
  source_too_short_or_underspecified:   812
```

### 5.2 Main-1200 Generation and Verification

```text
Selected sources:                     1,200
Accepted generated C_clean files:     1,197
Rejected generated candidates:            3
Runtime errors:                           0

Verification:
  A files found:                       1,200
  C files found:                       1,197
  Missing C files:                         3
  Accepted by verification:            1,197
  Rejected by verification:                0
  Verification acceptance over C:      1,197 / 1,197
```

### 5.3 Retry Disclosure Added in v1.0.1

```text
First-attempt accepted:                1,179 / 1,200
First-attempt acceptance rate:         98.25%

Records requiring fallback retry:         21 / 1,200
Fallback temperature path:             0.25 -> 0.35
Retry-rescued accepted records:           18 / 21

Final with-retry accepted:             1,197 / 1,200
Final with-retry acceptance rate:      99.75%
```

---

## 6. Main-1200 Rejected Cases

Three selected records were rejected and intentionally not exported as accepted `C_clean`.

| ID | Classification | Decision |
|---:|---|---|
| `19064` | malformed generation / prompt-boundary leakage / token corruption | correct rejection |
| `5702` | malformed generation / repetition / token corruption | correct rejection |
| `7164` | malformed generation / mojibake-like artifact / prompt-boundary leakage / token corruption | correct rejection |

Interpretation:

```text
The rejected cases were not semantic disagreements or verifier false positives.
They were malformed model generations with visible decoding corruption, duplicated spans,
mojibake-like artifacts, or prompt-boundary leakage such as "Human:".
They were correctly withheld from the accepted C_clean export.
```

---

## 7. Methodological Discovery

The category name `halogen/historical_events` was initially misleading.

Manual inspection showed that the relevant A_clean sources were not declarative factual prose. They were request-style prompts, for example:

```text
Tell me about the famous meeting between X and Y.
```

Therefore, the correct external-clean target was not factual answer generation. It was request-to-request paraphrasing:

```text
Describe the famous meeting between X and Y.
```

This led to the `--track prompt_paraphrase` protocol.

Core methodological boundary:

```text
B_hallucination was quarantined from generation.
B_hallucination was used only later as a contamination-audit antigen.
```

---

## 8. Version History Summary

| Version | Status | Main role |
|---|---|---|
| `v0.1.9` | historical predecessor | pre-v0.2 hardening state |
| `v0.2.0` | corrected but insufficient for prompt-like sources | multi-audit hardening; still produced wrong target style for prompt-like A sources |
| `v0.2.1` | first working prompt-paraphrase track | added `--track prompt_paraphrase`; passed smoke-3 and alpha-20 |
| `v0.2.2` | mojibake filtering | added `mojibake_or_encoding_artifact` filtering; revealed B-only contamination false positives |
| `v0.2.3` | main R0.5P-1 execution version | boundary-aware contamination patch; beta-500 perfect; main-1200 stable |
| documentation `v1.0.1` | publication patch | added retry-rate disclosure and apostrophe-boundary caveat after external audit |

---

## 9. External Audit Status

External audit verdict:

```text
APPROVE WITH MINOR PATCHES
```

Audit findings:

```text
Critical blockers: none.
Headline metrics: verified against real JSON artifacts.
Overclaiming: none detected.
Methodology: coherent for R0.5P-1.
Rejected cases: correctly classified as malformed generations.
```

Required patches identified by audit:

1. disclose retry-rate and distinguish first-attempt acceptance from with-retry acceptance;
2. document residual apostrophe-boundary gap in v0.2.3 B-only contamination matching.

Patch response:

```text
Both required findings were incorporated into the v1.0.1 documentation package.
```

---

## 10. Known Limitations

This record is limited to R0.5P-1.

It does **not** claim:

- full R0.5 validation;
- R1 tribunal validation;
- production-grade hallucination detection;
- universal kD validation;
- cross-domain generalization;
- validation of QA, reasoning, summarization, dialogue, code, or numerical tracks.

Known technical limitations:

```text
1. The main run used a two-attempt generation budget.
   First-attempt and with-retry acceptance must be reported separately.

2. v0.2.3 fixes suffix collisions such as Trade/trader,
   but does not fully close apostrophe-adjacent collisions such as Emery/d'Emery
   in all B-only-vs-C contamination matching cases.

3. The current validated track is prompt/query paraphrasing.
   Declarative factual external-clean equivalence remains deferred.

4. Some diagnostic JSON files may include UTF-8 BOM depending on export path.
   Future v0.2.4 should standardize BOM-free JSON output.

5. Larger scaling should not proceed without source-shape profiling.
```

---

## 11. GitHub Status

### 11.1 Repository Root

| Path | Role |
|---|---|
| `README.md` | Updated with R0, R0-bis, R0.5P-1 status and roadmap |
| `PUBLICATION_STATUS_R05P1.md` | This root-level milestone status file |

### 11.2 Outputs

| Path | Role |
|---|---|
| `docs/outputs/r05p1/` | R0.5P-1 output and package area |
| `docs/outputs/r05p1/source_packages/r05_external_clean_scripts_v0_2_3.zip` | v0.2.3 source package committed separately |
| `docs/outputs/r05p1/source_packages/r05_external_clean_scripts_v0_2_3.zip.sha256.txt` | source package digest |

### 11.3 Papers

| Path | Role |
|---|---|
| `docs/papers/r05p1/` | R0.5P-1 technical paper location |
| `docs/papers/r05p1/SAS_R0_5P1_Historical_Query_Paraphrase_Paper_v1_0_1.pdf` | human-readable paper |
| `docs/papers/r05p1/SAS_R0_5P1_Historical_Query_Paraphrase_Paper_v1_0_1.docx` | editable paper |
| `docs/papers/r05p1/SAS_R0_5P1_Historical_Query_Paraphrase_Paper_v1_0_1.md` | markdown paper |

---

## 12. Git Commit Messages

Known commit messages associated with this milestone:

```text
docs: update roadmap with R0.5P-1 external-clean results
docs(outputs): add R0.5P-1 historical query paraphrase artifacts
docs(papers): add R0.5P-1 patched technical paper
add R0.5P-1 v0.2.3 source package
```

Commit SHAs should be filled from local Git history if needed:

```powershell
git log --oneline --decorate --all -- README.md docs/outputs/r05p1 docs/papers/r05p1 PUBLICATION_STATUS_R05P1.md
```

---

## 13. TAD Reference

Original SAS / kD-0.56 registration context:

```text
TAD Argentina reference:
EX-2026-18792778
```

R0.5P-1 complementary documentation status:

```text
Dossier Ejecutivo TAD R0.5P-1 submitted as supplementary documentation.
Main visible document:
Dossier_Ejecutivo_TAD_R05P1_SAS_kD056_v1_0_0.pdf

Supporting package:
Dossier_TAD_R05P1_SAS_kD056_v1_0_0_package.zip
SHA-256:
641b92f4a4ec8776850c4736312dd2325d558f271903c9d7d9f053d39561d19b
```

If TAD assigned a new submission or expediente number for the supplementary upload, record it here:

```text
R0.5P-1 TAD supplementary submission reference:
TODO: paste TAD-generated reference if available.
```

---

## 14. Roadmap After R0.5P-1

Recommended next technical stage:

```text
r05_external_clean_scripts_v0_2_4
```

Required v0.2.4 goals:

```text
1. automatic retry metrics export;
2. apostrophe-boundary contamination fix;
3. BOM-free JSON output;
4. rejection taxonomy normalization;
5. regression tests for:
   - Trade/trader
   - Emery/d'Emery
   - Brien/O'Brien
   - Angelo/D'Angelo
   - Diaye/N'Diaye
   - prompt-boundary leakage
   - mojibake artifacts
   - duplicated spans
```

Recommended next methodological stage:

```text
source_shape_profiler.py
```

Purpose:

```text
Classify A_clean sources by actual source shape before choosing external-clean generation protocol.
```

Candidate source-shape labels:

```text
prompt_query
instruction
mapping_question
declarative_factual
dialogue_turn
summary_task
code_task
reasoning_task
short_underspecified
mojibake_corrupt
unknown
```

Recommended next research stage:

```text
R0.5P-2 - Multi-Category Prompt/Query Paraphrase Audit
```

Do not move to R1 until external-clean track coverage and module independence are stronger.

---

## 15. Publication Boundary Statement

R0.5P-1 should be cited as:

```text
a track-conditioned external-clean prompt-paraphrase audit over historical query-style sources.
```

It should not be cited as:

```text
final SAS validation,
full R0.5 validation,
R1 validation,
or universal hallucination detection evidence.
```

The correct scientific value of this milestone is:

```text
A traceable demonstration that source-shape inspection can correct a misleading corpus-category assumption,
select an appropriate external-clean generation protocol,
preserve B_hallucination quarantine,
generate clean prompt paraphrases at main-scale,
document malformed generation failures,
and publish the resulting evidence with hashes, manifests, external audit, GitHub placement, Zenodo record, and TAD traceability.
```

---

## 16. Freeze Note

This file freezes the administrative state of R0.5P-1 after the v1.0.1 publication patch.

Further changes should be recorded in new files or changelogs, such as:

```text
PUBLICATION_STATUS_R05P2.md
PATCH_NOTES_v0_2_4.md
SOURCE_SHAPE_REPORT.md
```

Do not retroactively reinterpret this R0.5P-1 record as broader validation than its stated scope.
