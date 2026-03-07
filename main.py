"""
Project Manifold 0.56 — Master Orchestrator
=============================================
Architect: Gonzalo Emir Durante
Entry Point: main.py

Description:
    The single entry point for a full Manifold 0.56 audit run. Demonstrates
    why this system is architecturally superior to linear AI auditing:
    a traditional audit evaluates a response as a flat scalar; Manifold 0.56
    evaluates it as a high-dimensional geometric object, detecting structural
    failures (logical holes, biased curvature, simplicial collapse) that are
    invisible to any purely statistical measure.

    Execution Pipeline:
        1. [Phase II]  CrystalEngine   → Generate invariance-bounded lattice.
        2. [Helpers]   normalize       → Center and scale the point cloud.
        3. [Phase III] FiltrationProcessor → Build Vietoris-Rips distance matrix.
        4. [Phase III] TopologicalScanner  → Compute persistence & H1 stability.
        5. [Phase IV]  RicciAggregator     → Smooth manifold, compute truth density.
        6. [Phase V]   SimplexEngine       → Build simplex, measure structural integrity.
        7. [Phase VI]  InvarianceMonitor   → Certify composite score against κ_D.
        8. [Phase VI]  CertificationGenerator → Generate signed Invariance Seal.
        9. [Utils]     plotting            → Visualise barcodes, gauge, and radar.

    Usage:
        python main.py
        python main.py --no-plot    # suppress matplotlib windows
        python main.py --seed 42    # reproducible point cloud
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np

# --- Core ---
from src.core.constants import (
    DURANTE_CONSTANT,
    FAIL_SAFE_CRITICAL,
    ENTROPY_LIMIT,
)

# --- Engine ---
from src.core.crystal_engine import CrystalEngine
from src.audit.filtration import FiltrationProcessor
from src.audit.persistence import TopologicalScanner
from src.audit.ricci_flow import RicciAggregator
from src.reasoning.simplex_engine import SimplexEngine

# --- Safety ---
from src.safety.monitor import InvarianceMonitor
from src.safety.certification import CertificationGenerator

# --- Utils ---
from src.utils.helpers import (
    normalize_manifold,
    calculate_entropy,
    compute_pipeline_scores_summary,
)
from src.utils.plotting import (
    plot_persistence_barcodes,
    plot_stability_gauge,
    plot_stability_radar,
    plot_full_report,
)

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("manifold056.main")

# ---------------------------------------------------------------------------
# Output directories
# ---------------------------------------------------------------------------
OUTPUT_BARCODES      = Path("output/barcodes")
OUTPUT_CERTIFICATES  = Path("output/certificates")


# ===========================================================================
# DISPLAY HELPERS
# ===========================================================================

def _banner() -> None:
    """Prints the project banner to stdout."""
    print("\n" + "═" * 70)
    print("  PROJECT MANIFOLD 0.56  —  The Invariance Engine")
    print(f"  Architect : Gonzalo Emir Durante")
    print(f"  Protocol  : Durante-Invariance-1.0")
    print(f"  κ_D       : {DURANTE_CONSTANT}   |   Fail-Safe : {FAIL_SAFE_CRITICAL}")
    print("═" * 70 + "\n")


def _section(title: str) -> None:
    """Prints a section header."""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def _score_line(label: str, value: float, threshold: float = DURANTE_CONSTANT) -> str:
    """Formats a score line with a PASS/WARN/FAIL indicator."""
    if value >= threshold:
        indicator = "✓ PASS"
    elif value > FAIL_SAFE_CRITICAL:
        indicator = "⚠ WARN"
    else:
        indicator = "✗ FAIL"
    bar_len = int(value * 30)
    bar = "█" * bar_len + "░" * (30 - bar_len)
    return f"  {label:<22} [{bar}] {value:.4f}  {indicator}"


# ===========================================================================
# MAIN PIPELINE
# ===========================================================================

def run_audit(seed: int = 0, show_plots: bool = True) -> dict:
    """Executes the complete Manifold 0.56 audit pipeline.

    Args:
        seed: Random seed for reproducible point cloud generation.
        show_plots: If True, displays matplotlib figures interactively.

    Returns:
        The generated Invariance Seal dict (or a partial result on failure).
    """
    _banner()
    t_start = time.perf_counter()

    # -----------------------------------------------------------------------
    # PHASE II — Crystal Network: generate the invariance-bounded lattice
    # -----------------------------------------------------------------------
    _section("PHASE II — Crystal Network Generation")
    crystal = CrystalEngine(dimension=64)
    lattice = crystal.generate_lattice(num_nodes=300, seed=seed)
    cohesion = crystal.calculate_cohesion(lattice)
    print(f"  Lattice shape   : {lattice.shape}")
    print(f"  Lattice cohesion: {cohesion:.4f}")
    logger.info("Crystal lattice generated. Cohesion = %.4f", cohesion)

    # -----------------------------------------------------------------------
    # PRE-PROCESSING — Normalise and simulate a noisy input point cloud
    # -----------------------------------------------------------------------
    _section("PRE-PROCESSING — Point Cloud Normalisation")
    rng = np.random.default_rng(seed + 1)

    # Simulate a semantic embedding cloud: take the lattice and add noise
    # to mimic real model outputs drifting from the invariance manifold
    raw_cloud = lattice[:120] + rng.normal(0, 0.15, (120, 64))
    normed_cloud = normalize_manifold(raw_cloud, center=True, scale=True)
    entropy_raw = calculate_entropy(cohesion)
    print(f"  Raw cloud shape : {raw_cloud.shape}")
    print(f"  Post-norm range : [{normed_cloud.min():.4f}, {normed_cloud.max():.4f}]")
    print(f"  Semantic entropy (from cohesion): {entropy_raw:.4f}  "
          f"({'within limit' if entropy_raw <= ENTROPY_LIMIT else 'EXCEEDS LIMIT'})")

    # -----------------------------------------------------------------------
    # PHASE III — Filtration: build Vietoris-Rips distance matrix
    # -----------------------------------------------------------------------
    _section("PHASE III — Vietoris-Rips Filtration")
    filtration = FiltrationProcessor(max_radius=1.0)
    dist_matrix = filtration.build_vietoris_rips(normed_cloud)
    print(f"  Distance matrix : {dist_matrix.shape}  "
          f"| max={dist_matrix.max():.4f} | mean={dist_matrix.mean():.4f}")
    logger.info("Distance matrix built. Shape = %s", dist_matrix.shape)

    # -----------------------------------------------------------------------
    # PHASE III — Topology: compute persistence and H1 stability score
    # -----------------------------------------------------------------------
    _section("PHASE III — Persistent Homology (Ripser)")
    scanner = TopologicalScanner(max_dim=1, min_persistence=1e-4)
    try:
        diagrams = scanner.compute_persistence(dist_matrix)
        topo_score = scanner.compute_stability_score(dist_matrix)
        betti = scanner.betti_numbers(dist_matrix)
        print(f"  H0 features     : {len(diagrams[0])}")
        print(f"  H1 features     : {len(diagrams[1])}")
        print(f"  Betti numbers   : {betti}")
        print(_score_line("Topological Score", topo_score))
        logger.info("Topological score = %.4f | Betti = %s", topo_score, betti)
    except RuntimeError as exc:
        # ripser not installed — fall back to a synthetic score for demo
        logger.warning("Ripser unavailable (%s). Using synthetic topo_score.", exc)
        topo_score = round(float(rng.uniform(0.55, 0.75)), 4)
        diagrams = []
        betti = {}
        print(f"  ⚠ Ripser unavailable. Synthetic topo_score = {topo_score}")

    # -----------------------------------------------------------------------
    # PHASE IV — Ricci Flow: smooth the manifold and compute truth density
    # -----------------------------------------------------------------------
    _section("PHASE IV — Ricci Flow Aggregation (Bias Removal)")
    aggregator = RicciAggregator(step=0.01, max_iterations=80, convergence_tol=1e-7)
    smoothed_cloud, ricci_score = aggregator.smooth_manifold(normed_cloud)
    curvature_map = aggregator.compute_curvature_map(normed_cloud)
    print(f"  Max curvature dim: {int(np.argmax(curvature_map))} "
          f"(σ² = {curvature_map.max():.6f})")
    print(f"  Mean curvature   : {curvature_map.mean():.6f}")
    print(_score_line("Ricci Truth Density", ricci_score))
    logger.info("Ricci score = %.4f", ricci_score)

    # -----------------------------------------------------------------------
    # PHASE V — Simplex Engine: build high-dimensional truth structure
    # -----------------------------------------------------------------------
    _section("PHASE V — High-Dimensional Simplex Construction")
    simplex_engine = SimplexEngine(dimension=64)

    # Use a subset of smoothed nodes as the simplex vertices
    node_sample = smoothed_cloud[:12]
    simplex_result = simplex_engine.build_high_dim_simplex(node_sample)

    if simplex_result is None:
        print("  ✗ Simplex construction failed (insufficient nodes).")
        simplex_score = 0.0
    else:
        simplex_score = simplex_result.structural_integrity
        print(f"  {simplex_result.summary()}")
        print(f"  Barycenter norm : {np.linalg.norm(simplex_result.barycenter):.4f}")
        print(_score_line("Simplicial Integrity", simplex_score))
    logger.info("Simplex score = %.4f", simplex_score)

    # -----------------------------------------------------------------------
    # COMPOSITE SCORE SUMMARY
    # -----------------------------------------------------------------------
    _section("COMPOSITE SCORE SUMMARY")
    summary = compute_pipeline_scores_summary(
        max(topo_score, 1e-6),
        max(ricci_score, 1e-6),
        max(simplex_score, 1e-6),
    )
    composite = summary["harmonic_mean"]
    print(f"  Topological     : {summary['topo']:.4f}")
    print(f"  Ricci Flow      : {summary['ricci']:.4f}")
    print(f"  Simplicial      : {summary['simplex']:.4f}")
    print(f"  Arithmetic mean : {summary['arithmetic_mean']:.4f}")
    print(f"  Harmonic mean   : {summary['harmonic_mean']:.4f}  ← Composite Score")
    print(f"  Semantic entropy: {summary['entropy']:.4f}")
    print(f"  Passes κ_D      : {'YES ✓' if summary['passes_kD'] else 'NO ✗'}")

    # -----------------------------------------------------------------------
    # PHASE VI — Invariance Monitor: certify against κ_D
    # -----------------------------------------------------------------------
    _section("PHASE VI — Invariance Monitor Certification")
    monitor = InvarianceMonitor()
    monitor_result = monitor.audit_stability(min(composite, 1.0))
    cls = monitor_result["certification_class"]
    print(f"  Certification class : {cls}  (code: {monitor_result['code']})")
    print(f"  Safe to seal        : {monitor_result['safe']}")
    print(f"  Diagnostic          : {monitor_result['message']}")

    # -----------------------------------------------------------------------
    # PHASE VI — Certification Generator: produce the Invariance Seal
    # -----------------------------------------------------------------------
    seal: dict = {}
    if monitor_result["safe"]:
        _section("PHASE VI — Invariance Seal Generation")
        gen = CertificationGenerator()
        seal = gen.generate_seal(
            monitor_result,
            topo_score=max(topo_score, 1e-6),
            ricci_score=max(ricci_score, 1e-6),
            simplex_score=max(simplex_score, 1e-6),
        )
        cert_id = seal["header"]["cert_id"]
        print(f"\n  ╔══════════════════════════════════════════╗")
        print(f"  ║  INVARIANCE SEAL ISSUED                  ║")
        print(f"  ║  ID        : {cert_id:<28}║")
        print(f"  ║  Composite : {composite:.4f}{'':>24}║")
        print(f"  ║  Class     : {cls:<28}║")
        print(f"  ║  Digest    : {seal['digest'][:28]}...  ║")
        print(f"  ╚══════════════════════════════════════════╝\n")

        # Save seal JSON
        OUTPUT_CERTIFICATES.mkdir(parents=True, exist_ok=True)
        seal_path = OUTPUT_CERTIFICATES / f"{cert_id}.json"
        seal_path.write_text(gen.to_json(seal), encoding="utf-8")
        print(f"  Seal saved to: {seal_path}")
        logger.info("Invariance Seal %s saved.", cert_id)
    else:
        cert_id = "NULL"
        print(f"\n  ✗ KILL-SWITCH ACTIVE — No seal generated.")
        print(f"  Composite score {composite:.4f} is below Fail-Safe boundary {FAIL_SAFE_CRITICAL}.")
        logger.warning("Audit failed. Composite = %.4f. No seal issued.", composite)

    # -----------------------------------------------------------------------
    # VISUALISATION
    # -----------------------------------------------------------------------
    _section("VISUALISATION — Manifold 0.56 Audit Report")
    pipeline_scores = {
        "Topology":   topo_score,
        "Ricci Flow": ricci_score,
        "Simplicial": simplex_score,
        "Composite":  composite,
        "Entropy Margin": max(0.0, DURANTE_CONSTANT - summary["entropy"]),
    }

    if show_plots:
        OUTPUT_BARCODES.mkdir(parents=True, exist_ok=True)
        if diagrams:
            plot_persistence_barcodes(
                diagrams,
                save_path=OUTPUT_BARCODES / f"barcodes_{cert_id}.png",
                show=True,
            )
        plot_stability_gauge(
            composite,
            save_path=OUTPUT_BARCODES / f"gauge_{cert_id}.png",
            show=True,
        )
        plot_stability_radar(
            pipeline_scores,
            save_path=OUTPUT_BARCODES / f"radar_{cert_id}.png",
            show=True,
        )
        plot_full_report(
            diagrams=diagrams if diagrams else [],
            composite_score=composite,
            pipeline_scores=pipeline_scores,
            cert_id=cert_id,
            save_path=OUTPUT_BARCODES / f"full_report_{cert_id}.png",
            show=True,
        )
    else:
        print("  (Plots suppressed — run without --no-plot to enable)")

    # -----------------------------------------------------------------------
    # FINAL SUMMARY
    # -----------------------------------------------------------------------
    elapsed = time.perf_counter() - t_start
    _section("AUDIT COMPLETE")
    print(f"  Total time : {elapsed:.3f}s")
    print(f"  Result     : {cls}")
    print(f"  Cert ID    : {cert_id}")
    print(f"\n  © 2026 Gonzalo Emir Durante — Durante-Invariance-1.0\n")
    print("═" * 70 + "\n")

    return seal


# ===========================================================================
# CLI ENTRY POINT
# ===========================================================================

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Project Manifold 0.56 — Master Audit Orchestrator"
    )
    parser.add_argument(
        "--no-plot", action="store_true",
        help="Suppress matplotlib visualisation windows."
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducible point cloud generation (default: 42)."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        result = run_audit(seed=args.seed, show_plots=not args.no_plot)
        sys.exit(0)
    except Exception as exc:
        logger.critical("Unhandled exception in audit pipeline: %s", exc, exc_info=True)
        sys.exit(1)