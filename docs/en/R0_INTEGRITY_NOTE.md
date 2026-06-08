# R0 Integrity Note

## Purpose

This document explains how to preserve the original Project Manifold 0.56 integrity record while adding updated documentation.

## R0 manifest

The original repository includes:

```text
INTEGRITY_MANIFEST.json
```

This file is the historical R0 integrity manifest.

It records the SHA-256 state of the original registered snapshot and should not be overwritten.

Known R0 summary retained from the historical README:

```text
Generated: 2026-03-07T12:02:30.161343+00:00
Algorithm: SHA-256
Files hashed: 31
Master Digest: b8fbe7c0e334fd483634c16c87a8b2cff77debc118b35b115d89d25e04f45e1b
Registration: EX-2026-18792778- -APN-DGDYD#JGM
```

## R1 manifest

The updated documentation state may include:

```text
INTEGRITY_MANIFEST_R1.json
```

R1 should hash the contextualized documentation files, for example:

- `README.md`
- `docs/HISTORICAL_CONTEXT.md`
- `docs/TERMINOLOGY_ALIGNMENT.md`
- `docs/KAPPA_EQUIVALENCE_SEMANTIC_SHIELD.md`
- `docs/ROADMAP_EXTENSIONS.md`
- `docs/R0_INTEGRITY_NOTE.md`
- `UPLOAD_INSTRUCTIONS.md` if archived externally
- any future documentation-only files

## Preservation rule

Do not edit or replace `INTEGRITY_MANIFEST.json`.

Place `INTEGRITY_MANIFEST_R1.json` in the repository root, beside the original.

Recommended root layout:

```text
INTEGRITY_MANIFEST.json       # historical R0 manifest
INTEGRITY_MANIFEST_R1.json    # contextualized documentation update
README.md
docs/
```

## Tagging before update

Before replacing README or adding R1 files, create an annotated tag pointing to the current R0 commit:

```bash
git checkout main
git pull origin main
git tag -a r0-manifold-056-2026-03-07 -m "R0 historical Project Manifold 0.56 snapshot"
git push origin r0-manifold-056-2026-03-07
```

If the repository uses `master` instead of `main`, replace `main` with `master`.

## Verification after update

After adding R1 files:

```bash
git status
git diff --stat
sha256sum README.md docs/*.md INTEGRITY_MANIFEST_R1.json
```

On PowerShell:

```powershell
Get-FileHash README.md -Algorithm SHA256
Get-FileHash docs\*.md -Algorithm SHA256
Get-FileHash INTEGRITY_MANIFEST_R1.json -Algorithm SHA256
```

## Commit recommendation

```bash
git add README.md docs/HISTORICAL_CONTEXT.md docs/TERMINOLOGY_ALIGNMENT.md docs/KAPPA_EQUIVALENCE_SEMANTIC_SHIELD.md docs/ROADMAP_EXTENSIONS.md docs/R0_INTEGRITY_NOTE.md INTEGRITY_MANIFEST_R1.json
git commit -m "docs: contextualize Project Manifold 0.56 as historical κD prior-art snapshot"
git push origin main
```
