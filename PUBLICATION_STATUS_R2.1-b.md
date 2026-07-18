# Publication Status — R2.1-b (Toward Reference-Free Code Hallucination Detection)

**Status:** Published
**Date:** 2026-07-18
**Author:** Gonzalo Emir Durante
**TAD Registry:** EX-2026-18792778
**Extends:** R2.1 (DOI 10.5281/zenodo.21365707)

---

## Zenodo Record

- **Title:** SAS R2.1-b — Toward Reference-Free Code Hallucination Detection: Live PyPI Verification and Evidence of Defensive Package Squatting
- **DOI:** [10.5281/zenodo.21420392](https://doi.org/10.5281/zenodo.21420392)
- **Record:** https://zenodo.org/records/21420392

## Artifact Names and Integrity

| Artifact | Path | SHA-256 |
|---|---|---|
| Full R2.1-b package (ZIP) | `docs/en/outputs/R2.1b_Reference_Free_Detection_Zenodo.zip` | `caa4362c74540aac640ecb9ac1765c7399720565d52a70aa2a25dfdfb8c3696c` |
| Technical paper | `paper/R2.1b_Reference_Free_Detection.pdf` (inside ZIP) | See package contents; content-identical to the Markdown source `paper/R2.1b_paper.md`. |
| Timestamp proof | RFC 3161 token (TSA: FreeTSA), `.tsr` file, included in the Zenodo deposit | Anchors the SHA-256 of the full ZIP above. Alternative to OpenTimestamps, used because `opentimestamps-client` had an unresolved Windows/Python 3.13 dependency conflict (`python-bitcoinlib` ctypes/OpenSSL DLL loading failure) at the time of publication. |

**Primary integrity reference for this milestone:** the full-package ZIP SHA-256 above, cross-checked against the RFC 3161 timestamp token.

## Scope

R2.1-b addresses the problem R2.1 explicitly left open: detecting a fabricated import, function, or module in freshly generated code with **no reference implementation available at detection time**. This milestone is restricted to the narrowest tractable sub-case: verifying whether an **imported Python module name** corresponds to a real package, using the module name alone, with no execution and no reference required.

## Methodology, in Three Phases

- **Phase 1:** minimal knowledge base combining `sys.stdlib_module_names` and the top-200 PyPI packages by download volume (source: `hugovk/top-pypi-packages`, snapshot included for reproducibility). Documented that package name and import name frequently disagree.
- **Phase 2:** validated against Trend Micro's public "Slopsquatting" dataset (MIT license): 7,956 real coding-agent module references, 302 ground-truth fabricated packages.
- **Phase 3:** replaced the static whitelist with a live query against the real PyPI JSON API, with multi-candidate name resolution.

## Main Results

| Phase | Result | Outcome |
|---|---:|---|
| Phase 2 (raw) | Precision 5.25% / Recall 90.73% | **Negative** — static whitelist not usable in production |
| Phase 2 (ground-truth corrected) | Recall 100% (274/274) after excluding 28 noise entries (9.3% of the labeled positive class) | Data-quality finding on the *external* dataset's own verification method |
| Phase 3 (live PyPI check) | Precision 100.00% (0 false positives) / Recall 61.68% | **Mixed** — precision solved via live registry verification |
| Phase 3 (recall investigation) | 21 of 24 remaining unresolved names are real PyPI packages first published 2026-02-19 to 2026-02-21, described as "Benign slopsquatting research package" | **Unplanned finding** — evidence of active, deliberate defensive registration of exactly the names known to be hallucinated by LLM coding agents |

## Methodological Boundary

**This record does not claim:**

- a solution to reference-free hallucination detection at the function or method level — only import-name existence is validated;
- applicability to any language other than Python;
- that the 61.68% raw recall figure is a stable estimate of the live-check method's real-time performance. It is a lower bound produced by comparing a live system against a benchmark ground truth frozen at an earlier point in time, in a domain now shown to be under active, adversarially-reactive modification (see paper Section 4.4);
- attribution of the "benign slopsquatting research package" registrations to any specific individual or organization — reported as an independently verifiable observation against the public PyPI registry.

**The correct public claim is:**

```text
R2.1-b validates import-name existence checking for Python, achieving 100.00%
precision via live PyPI registry verification (0 false positives against a
7,956-reference real-world corpus). Its raw recall figure of 61.68% is shown,
through direct investigation of the underlying package registration dates, to
be substantially explained by registry drift rather than by a detection
failure.
```

## Recommended Citation

```text
Durante, G. E. (2026). SAS / κD=0.56 — R2.1-b: Toward Reference-Free Code
Hallucination Detection. Zenodo. https://doi.org/10.5281/zenodo.21420392
```

## Relation to Prior Milestones

R2.1-b is a direct continuation of R2.1 (DOI 10.5281/zenodo.21365707), within the same authorship and TAD registry (EX-2026-18792778). It is not an independent standard.

## Next Steps

- Function- and method-level reference-free validation (open work; no dedicated milestone number assigned yet).
- Production-scale considerations for the live PyPI check (rate limits, local mirror/index for high-volume use — see paper Section 6).
- R2.2/R3: dialogue coherence and temporal consistency.
