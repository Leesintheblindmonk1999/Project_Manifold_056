# Errata Register — Project Manifold 0.56

## R1-D (2026-07-09 → corrected 2026-07-29)

**What was published:** F1 = 0.8571 / 0.8717 for the Flow + CRE + Negation composite on R0.5D.

**What was wrong:** These figures were accidentally copied from R1 v1.0.7's own ablation table (Zenodo 21034155), not computed on the R0.5D corpus. They matched to four decimal places across all metrics — impossible by chance.

**How it was detected:** Independent re-verification during cross-correlation of production modules against R0-bis baseline modules on real data.

**Corrected figures (computed from original unmodified per-pair outputs):**
- Flow + CRE + Negation, score ≥ 1: F1 = 0.5230, Precision = 0.5617, Recall = 0.4892

**Impact:** The structural composite performs above chance but below the lexical baseline (AUC 0.749) on this corpus. No artifact hashes were affected; only interpretive claims.

**Verification:** Original data preserved in `r1d_results_archive.zip` (SHA-256: `37F2B540...`). Corrected values computed directly from stored per-pair module outputs without re-running modules.