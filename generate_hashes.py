"""
Project Manifold 0.56 — Cryptographic Integrity Hasher
========================================================
Architect: Gonzalo Emir Durante
Script:    generate_hashes.py

Description:
    Automatically discovers and SHA-256 hashes EVERY file in the
    project directory (recursively), regardless of name or extension.
    No hardcoded file list — if it exists in the repo, it gets hashed.

    Produces:
        - INTEGRITY_MANIFEST.json   machine-readable, embeds into OSS seals
        - INTEGRITY_REPORT.md       human-readable table, paste into README

Usage:
    python generate_hashes.py
    python generate_hashes.py --root /path/to/Project_Manifold_056
    python generate_hashes.py --root . --output my_manifest.json

    # Exclude extra folders if needed (default excludes: .git, __pycache__, .venv)
    python generate_hashes.py --exclude .git __pycache__ .venv node_modules
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_EXCLUDES: list[str] = [
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    "*.pyc",
    "INTEGRITY_MANIFEST.json",   # don't hash the manifest itself
    "INTEGRITY_REPORT.md",       # don't hash the report itself
]


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    """Returns the SHA-256 hex digest of a file's binary content."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def should_exclude(path: Path, root: Path, excludes: list[str]) -> bool:
    """Returns True if any part of the path matches an exclusion pattern."""
    rel = path.relative_to(root)
    parts = rel.parts
    for excl in excludes:
        # Match against any directory component or the filename
        if excl.startswith("*"):
            if path.name.endswith(excl[1:]):
                return True
        else:
            if excl in parts or path.name == excl:
                return True
    return False


def discover_files(root: Path, excludes: list[str]) -> list[Path]:
    """Recursively discovers all files in root, applying exclusions."""
    all_files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and not should_exclude(p, root, excludes)
    )
    return all_files


def phase_label(rel_path: str) -> str:
    """Infers a phase/category label from the file path."""
    p = rel_path.lower()
    if "constants"       in p: return "Phase I   — Constants & κ_D"
    if "crystal_engine"  in p: return "Phase II  — Crystal Network"
    if "filtration"      in p: return "Phase III — Vietoris-Rips Filtration"
    if "persistence"     in p: return "Phase III — Persistent Homology"
    if "ricci"           in p: return "Phase IV  — Ricci Flow"
    if "simplex"         in p: return "Phase V   — Simplex Engine"
    if "monitor"         in p: return "Phase VI  — Invariance Monitor"
    if "certification"   in p: return "Phase VI  — Certification (OSS)"
    if "helpers"         in p: return "Utils     — Helpers"
    if "plotting"        in p: return "Utils     — Visualisation"
    if "main.py"         in p: return "Orchestrator — main.py"
    if "license"         in p: return "Legal     — License"
    if "prior_art"       in p: return "Legal     — Prior Art Declaration"
    if "tad_argentina"   in p: return "Legal     — TAD Notice"
    if "readme"          in p: return "README"
    if "requirements"    in p: return "Config    — requirements.txt"
    if "gitignore"       in p: return "Config    — .gitignore"
    if "docs/"           in p or "docs\\" in p: return "Docs      — Manual / PDF"
    if "data/"           in p or "data\\" in p: return "Data      — Dataset"
    if "output/"         in p or "output\\" in p: return "Output    — Result"
    if "legal/"          in p or "legal\\" in p: return "Legal     — Document"
    if "tests/"          in p or "tests\\" in p: return "Tests     — Test file"
    return "Other"


# ---------------------------------------------------------------------------
# Build manifest
# ---------------------------------------------------------------------------

def build_manifest(root: Path, excludes: list[str]) -> dict:
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    files     = discover_files(root, excludes)
    entries   = []

    print(f"\n{'═' * 68}")
    print("  PROJECT MANIFOLD 0.56 — Cryptographic Integrity Hasher")
    print(f"  Root      : {root.resolve()}")
    print(f"  Timestamp : {timestamp}")
    print(f"  Files found: {len(files)}")
    print(f"{'═' * 68}\n")

    for full_path in files:
        rel     = full_path.relative_to(root).as_posix()
        digest  = sha256_file(full_path)
        size    = full_path.stat().st_size
        label   = phase_label(rel)

        print(f"  ✓  {rel}")
        print(f"     SHA-256 : {digest}")
        print(f"     Size    : {size:,} bytes  |  {label}\n")

        entries.append({
            "file":        rel,
            "description": label,
            "sha256":      digest,
            "size_bytes":  size,
        })

    # Master digest — SHA-256 of all individual digests concatenated in order
    combined      = "".join(e["sha256"] for e in entries)
    master_digest = hashlib.sha256(combined.encode()).hexdigest()

    print(f"{'─' * 68}")
    print(f"  Total files hashed : {len(entries)}")
    print(f"\n  ╔══════════════════════════════════════════════════════════════╗")
    print(f"  ║  MASTER DIGEST (SHA-256)                                     ║")
    print(f"  ║  {master_digest}  ║")
    print(f"  ╚══════════════════════════════════════════════════════════════╝\n")

    return {
        "project":       "Project Manifold 0.56 — The Invariance Engine",
        "author":        "Gonzalo Emir Durante",
        "license":       "Durante Invariance License v1.0",
        "registration":  "EX-2026-18792778- -APN-DGDYD#JGM",
        "zenodo":        "https://zenodo.org/records/18664548",
        "generated_at":  timestamp,
        "algorithm":     "SHA-256",
        "total_files":   len(entries),
        "master_digest": master_digest,
        "files":         entries,
    }


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def write_json(manifest: dict, path: Path) -> None:
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  ✓ JSON manifest saved : {path}")


def write_markdown(manifest: dict, path: Path) -> None:
    ts     = manifest["generated_at"]
    master = manifest["master_digest"]
    reg    = manifest["registration"]
    zenodo = manifest["zenodo"]
    total  = manifest["total_files"]

    lines = [
        "## Cryptographic Integrity Manifest\n",
        f"> **Generated:** `{ts}`",
        f"> **Algorithm:** `SHA-256`",
        f"> **Files hashed:** `{total}`",
        f"> **Master Digest:** `{master}`",
        f"> **Registration:** `{reg}` — [Zenodo]({zenodo})\n",
        "---\n",
    ]

    # Group entries by category
    groups: dict[str, list[dict]] = {}
    for e in manifest["files"]:
        cat = e["description"].split("—")[0].strip()
        groups.setdefault(cat, []).append(e)

    for cat, entries in groups.items():
        lines.append(f"### {cat}\n")
        lines.append("| File | SHA-256 | Size |")
        lines.append("|------|---------|------|")
        for e in entries:
            short = e["sha256"][:20] + "..."
            size  = f"{e['size_bytes']:,} B"
            lines.append(f"| `{e['file']}` | `{short}` | {size} |")
        lines.append("")

    lines += [
        "---\n",
        f"*© 2026 Gonzalo Emir Durante · Durante Invariance License v1.0*  ",
        f"*Registration: `{reg}` · [Zenodo]({zenodo})*\n",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✓ Markdown report saved : {path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Project Manifold 0.56 — Auto-discovery Cryptographic Hasher"
    )
    p.add_argument(
        "--root", type=Path, default=Path("."),
        help="Project root directory (default: current directory)."
    )
    p.add_argument(
        "--output", type=Path, default=None,
        help="Output path for INTEGRITY_MANIFEST.json (default: <root>/INTEGRITY_MANIFEST.json)."
    )
    p.add_argument(
        "--exclude", nargs="*", default=[],
        help="Additional folder/file names to exclude (added to defaults)."
    )
    return p.parse_args()


if __name__ == "__main__":
    args     = parse_args()
    root     = args.root.resolve()
    excludes = DEFAULT_EXCLUDES + (args.exclude or [])

    if not root.exists():
        print(f"ERROR: Root not found: {root}")
        sys.exit(1)

    manifest = build_manifest(root, excludes)
    json_out = args.output or root / "INTEGRITY_MANIFEST.json"
    md_out   = json_out.parent / "INTEGRITY_REPORT.md"

    write_json(manifest, json_out)
    write_markdown(manifest, md_out)

    print(f"\n{'═' * 68}")
    print("  DONE")
    print(f"  JSON   : {json_out}")
    print(f"  REPORT : {md_out}")
    print(f"\n  → Add INTEGRITY_MANIFEST.json and INTEGRITY_REPORT.md to git.")
    print(f"  → Paste the MASTER DIGEST into your README as tamper-proof seal.")
    print(f"{'═' * 68}\n")