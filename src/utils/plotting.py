"""
Project Manifold 0.56 — Visualisation Suite
=============================================
Architect: Gonzalo Emir Durante
Phase:     Cross-cutting (Phases III, IV, VI visual output)

Description:
    Provides publication-quality visualisation functions for the Manifold 0.56
    audit pipeline. All plots are themed consistently with the project's dark
    colour palette and annotated with the Durante Constant reference line.

    Functions:
        - plot_persistence_barcodes : H0/H1 barcode diagram (Phase III output).
        - plot_stability_gauge       : Horizontal stability bar with κ_D marker.
        - plot_stability_radar       : Multi-dimensional radar chart of pipeline scores.
        - plot_full_report           : Composite 2×2 figure combining all views.

    Output files are saved as PNGs to `output/barcodes/` or `output/certificates/`
    by default, and optionally displayed interactively.

    Dependencies:
        matplotlib >= 3.5
        persim >= 0.3   (for plot_persistence_barcodes)
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Theme constants
# ---------------------------------------------------------------------------
_DARK_BG     = "#0d0d0d"
_PANEL_BG    = "#1a1a2e"
_ACCENT_GOLD = "#f0c040"
_GREEN       = "#00e676"
_ORANGE      = "#ff9800"
_RED         = "#f44336"
_TEXT        = "#e0e0e0"
_KD_COLOR    = "#f0c040"  # κ_D reference line
_DPI         = 150

try:
    from persim import plot_diagrams as _persim_plot_diagrams
    _PERSIM_AVAILABLE = True
except ImportError:
    _PERSIM_AVAILABLE = False
    logger.warning(
        "persim is not installed. plot_persistence_barcodes will use a "
        "fallback renderer. Install with: pip install persim"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def plot_persistence_barcodes(
    diagrams: list[NDArray[np.float64]],
    title: str = "Persistence Barcodes — Phase III Topological Scan",
    save_path: Optional[Path] = None,
    show: bool = True,
) -> plt.Figure:
    """Plots H0 and H1 persistence barcodes from Ripser diagram output.

    Each bar represents the lifetime of a topological feature: H0 bars are
    connected components (semantic clusters), H1 bars are cycles (potential
    logical holes / hallucinations). Long-lived H1 bars indicate severe
    semantic gaps that will lower the stability score.

    Args:
        diagrams: List of persistence diagrams as returned by Ripser, where
            diagrams[0] is H0 and diagrams[1] is H1. Each entry is an NDArray
            of shape (K, 2) with columns [birth, death].
        title: Figure title.
        save_path: If provided, saves the figure to this path as a PNG.
        show: If True, calls plt.show() after rendering.

    Returns:
        The matplotlib :class:`Figure` object.

    Raises:
        ValueError: If `diagrams` is empty or does not contain H1 data.
    """
    if not diagrams:
        raise ValueError("`diagrams` must be a non-empty list of persistence diagrams.")

    if _PERSIM_AVAILABLE:
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=_DARK_BG)
        ax.set_facecolor(_PANEL_BG)
        _persim_plot_diagrams(diagrams, ax=ax, show=False)
        ax.set_title(title, color=_TEXT, fontsize=13, pad=12)
        _apply_dark_axes(ax)
    else:
        fig, axes = plt.subplots(
            1, min(len(diagrams), 2), figsize=(12, 5), facecolor=_DARK_BG
        )
        if len(diagrams) == 1:
            axes = [axes]
        for dim_idx, (ax, dgm) in enumerate(zip(axes, diagrams[:2])):
            ax.set_facecolor(_PANEL_BG)
            finite_mask = np.isfinite(dgm[:, 1])
            dgm_finite = dgm[finite_mask]
            colors = [_GREEN if dim_idx == 0 else _RED] * len(dgm_finite)
            for k, (birth, death) in enumerate(dgm_finite):
                ax.barh(k, death - birth, left=birth, height=0.7, color=colors[k], alpha=0.8)
            ax.set_xlabel("Filtration radius", color=_TEXT, fontsize=9)
            ax.set_title(f"H{dim_idx} — {'Components' if dim_idx == 0 else 'Cycles (Holes)'}", color=_TEXT)
            _apply_dark_axes(ax)
        fig.suptitle(title, color=_TEXT, fontsize=13)

    _add_kd_annotation(fig)
    plt.tight_layout()
    _save_and_show(fig, save_path, show)
    return fig


def plot_stability_gauge(
    score: float,
    threshold: float = 0.56,
    fail_safe: float = 0.44,
    title: str = "Manifold Stability Gauge",
    save_path: Optional[Path] = None,
    show: bool = True,
) -> plt.Figure:
    """Renders a horizontal stability gauge annotated with the κ_D threshold.

    The bar colour encodes the certification class:
        Green  → CERTIFIED  (score ≥ 0.56)
        Orange → DEGRADED   (0.44 < score < 0.56)
        Red    → NULL       (score ≤ 0.44)

    Args:
        score: Stability score ∈ [0, 1].
        threshold: κ_D reference line position (default 0.56).
        fail_safe: Fail-safe boundary reference line (default 0.44).
        title: Figure title.
        save_path: Optional output path for PNG export.
        show: If True, calls plt.show().

    Returns:
        The matplotlib :class:`Figure` object.

    Raises:
        ValueError: If `score` is outside [0, 1].
    """
    if not (0.0 <= score <= 1.0):
        raise ValueError(f"`score` must be in [0, 1]. Received: {score}")

    color = _GREEN if score >= threshold else (_ORANGE if score > fail_safe else _RED)
    label = "CERTIFIED" if score >= threshold else ("DEGRADED" if score > fail_safe else "NULL")

    fig, ax = plt.subplots(figsize=(8, 2.5), facecolor=_DARK_BG)
    ax.set_facecolor(_PANEL_BG)

    ax.barh(["Stability Score"], [score], color=color, height=0.5, alpha=0.9)

    # Background track
    ax.barh(["Stability Score"], [1.0], color="#2a2a3e", height=0.5, alpha=0.4)

    # Reference lines
    ax.axvline(threshold, color=_KD_COLOR, linestyle="--", linewidth=1.8,
               label=f"κ_D = {threshold}")
    ax.axvline(fail_safe, color=_RED, linestyle=":", linewidth=1.4,
               label=f"Fail-Safe = {fail_safe}")

    ax.set_xlim(0, 1)
    ax.set_title(
        f"{title}  |  Score: {score:.4f}  |  Class: {label}",
        color=_TEXT, fontsize=12, pad=10
    )
    ax.legend(loc="lower right", facecolor=_PANEL_BG, labelcolor=_TEXT, fontsize=9)
    _apply_dark_axes(ax)

    plt.tight_layout()
    _save_and_show(fig, save_path, show)
    return fig


def plot_stability_radar(
    scores: dict[str, float],
    threshold: float = 0.56,
    title: str = "Pipeline Stability Radar — Manifold 0.56",
    save_path: Optional[Path] = None,
    show: bool = True,
) -> plt.Figure:
    """Renders a radar (spider) chart of multi-dimensional pipeline scores.

    Each axis represents one pipeline dimension. The κ_D threshold is drawn
    as a reference polygon. Scores above the threshold polygon are in the
    invariance zone; scores below indicate instability in that dimension.

    Args:
        scores: Dict mapping dimension labels to score values ∈ (0, 1].
            Recommended keys: "Topology", "Ricci Flow", "Simplicial",
            "Composite", "Entropy Margin".
        threshold: κ_D reference polygon value (default 0.56).
        title: Figure title.
        save_path: Optional output path for PNG export.
        show: If True, calls plt.show().

    Returns:
        The matplotlib :class:`Figure` object.

    Raises:
        ValueError: If `scores` has fewer than 3 entries.

    Example:
        >>> plot_stability_radar({
        ...     "Topology": 0.72, "Ricci Flow": 0.68,
        ...     "Simplicial": 0.74, "Composite": 0.71,
        ... })
    """
    if len(scores) < 3:
        raise ValueError("Radar chart requires at least 3 dimensions.")

    labels = list(scores.keys())
    values = [max(0.0, min(1.0, v)) for v in scores.values()]
    N = len(labels)

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # close the polygon
    values_plot = values + values[:1]
    threshold_plot = [threshold] * (N + 1)

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True}, facecolor=_DARK_BG)
    ax.set_facecolor(_PANEL_BG)

    # κ_D reference polygon
    ax.plot(angles, threshold_plot, color=_KD_COLOR, linestyle="--",
            linewidth=1.5, label=f"κ_D = {threshold}", alpha=0.8)
    ax.fill(angles, threshold_plot, color=_KD_COLOR, alpha=0.06)

    # Score polygon
    composite = np.mean(values)
    fill_color = _GREEN if composite >= threshold else (_ORANGE if composite > 0.44 else _RED)
    ax.plot(angles, values_plot, color=fill_color, linewidth=2.2, label="Pipeline Scores")
    ax.fill(angles, values_plot, color=fill_color, alpha=0.25)

    # Score dots
    for angle, val in zip(angles[:-1], values):
        dot_color = _GREEN if val >= threshold else (_ORANGE if val > 0.44 else _RED)
        ax.scatter(angle, val, s=60, color=dot_color, zorder=5)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color=_TEXT, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.44, 0.56, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.44", "κ_D=0.56", "0.8", "1.0"],
                        color=_ACCENT_GOLD, fontsize=7)
    ax.tick_params(colors=_TEXT)
    ax.spines["polar"].set_color("#3a3a5e")
    ax.grid(color="#3a3a5e", linewidth=0.6)

    ax.set_title(title, color=_TEXT, fontsize=13, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1),
               facecolor=_PANEL_BG, labelcolor=_TEXT, fontsize=9)

    plt.tight_layout()
    _save_and_show(fig, save_path, show)
    return fig


def plot_full_report(
    diagrams: list[NDArray[np.float64]],
    composite_score: float,
    pipeline_scores: dict[str, float],
    cert_id: str = "PENDING",
    save_path: Optional[Path] = None,
    show: bool = True,
) -> plt.Figure:
    """Renders a composite 2×2 audit report figure.

    Combines:
        - Top-left:  H1 persistence barcode (Phase III).
        - Top-right: Stability gauge (Phase VI).
        - Bottom:    Full-width stability radar (Phases III–VI).

    Args:
        diagrams: Ripser persistence diagrams list.
        composite_score: Harmonic mean composite score ∈ (0, 1].
        pipeline_scores: Dict of labelled scores for the radar chart.
        cert_id: Certification ID string to embed in the figure title.
        save_path: Optional output path for PNG export.
        show: If True, calls plt.show().

    Returns:
        The matplotlib :class:`Figure` object.
    """
    fig = plt.figure(figsize=(16, 12), facecolor=_DARK_BG)
    fig.suptitle(
        f"Manifold 0.56 — Full Audit Report  |  Cert: {cert_id}",
        color=_ACCENT_GOLD, fontsize=15, fontweight="bold", y=0.98
    )

    # --- Top-left: Barcodes ---
    ax_bc = fig.add_subplot(2, 2, 1)
    ax_bc.set_facecolor(_PANEL_BG)
    if _PERSIM_AVAILABLE and diagrams:
        _persim_plot_diagrams(diagrams, ax=ax_bc, show=False)
    else:
        ax_bc.text(0.5, 0.5, "persim not available\n(install: pip install persim)",
                   ha="center", va="center", color=_ORANGE, fontsize=10,
                   transform=ax_bc.transAxes)
    ax_bc.set_title("H0/H1 Persistence Barcodes", color=_TEXT, fontsize=11)
    _apply_dark_axes(ax_bc)

    # --- Top-right: Stability gauge ---
    ax_gauge = fig.add_subplot(2, 2, 2)
    ax_gauge.set_facecolor(_PANEL_BG)
    threshold, fail_safe = 0.56, 0.44
    color = _GREEN if composite_score >= threshold else (_ORANGE if composite_score > fail_safe else _RED)
    label = "CERTIFIED" if composite_score >= threshold else ("DEGRADED" if composite_score > fail_safe else "NULL")
    ax_gauge.barh(["Score"], [composite_score], color=color, height=0.5)
    ax_gauge.barh(["Score"], [1.0], color="#2a2a3e", height=0.5, alpha=0.4)
    ax_gauge.axvline(threshold, color=_KD_COLOR, linestyle="--", linewidth=1.8, label=f"κ_D={threshold}")
    ax_gauge.axvline(fail_safe, color=_RED,   linestyle=":",  linewidth=1.4, label=f"FS={fail_safe}")
    ax_gauge.set_xlim(0, 1)
    ax_gauge.set_title(f"Composite Score: {composite_score:.4f}  [{label}]", color=_TEXT, fontsize=11)
    ax_gauge.legend(facecolor=_PANEL_BG, labelcolor=_TEXT, fontsize=8)
    _apply_dark_axes(ax_gauge)

    # --- Bottom: Radar (spans both columns) ---
    ax_radar = fig.add_subplot(2, 1, 2, polar=True)
    ax_radar.set_facecolor(_PANEL_BG)
    labels = list(pipeline_scores.keys())
    values = [max(0.0, min(1.0, v)) for v in pipeline_scores.values()]
    N = len(labels)
    if N >= 3:
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        values_plot = values + values[:1]
        kd_poly = [threshold] * (N + 1)
        ax_radar.plot(angles, kd_poly, color=_KD_COLOR, linestyle="--", linewidth=1.5, label=f"κ_D={threshold}")
        ax_radar.fill(angles, kd_poly, color=_KD_COLOR, alpha=0.06)
        fill_color = _GREEN if composite_score >= threshold else (_ORANGE if composite_score > fail_safe else _RED)
        ax_radar.plot(angles, values_plot, color=fill_color, linewidth=2.2, label="Scores")
        ax_radar.fill(angles, values_plot, color=fill_color, alpha=0.25)
        ax_radar.set_xticks(angles[:-1])
        ax_radar.set_xticklabels(labels, color=_TEXT, fontsize=9)
        ax_radar.set_ylim(0, 1)
        ax_radar.set_yticks([0.44, 0.56, 1.0])
        ax_radar.set_yticklabels(["0.44", "κ_D=0.56", "1.0"], color=_ACCENT_GOLD, fontsize=7)
        ax_radar.grid(color="#3a3a5e", linewidth=0.6)
        ax_radar.spines["polar"].set_color("#3a3a5e")
        ax_radar.set_title("Pipeline Stability Radar", color=_TEXT, fontsize=11, pad=20)
        ax_radar.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1),
                        facecolor=_PANEL_BG, labelcolor=_TEXT, fontsize=8)

    _add_kd_annotation(fig)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    _save_and_show(fig, save_path, show)
    return fig


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _apply_dark_axes(ax: plt.Axes) -> None:
    """Applies the dark theme to a standard (non-polar) Axes object."""
    ax.tick_params(colors=_TEXT, labelsize=8)
    ax.xaxis.label.set_color(_TEXT)
    ax.yaxis.label.set_color(_TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor("#3a3a5e")
    ax.grid(color="#2a2a3e", linewidth=0.5, alpha=0.6)


def _add_kd_annotation(fig: plt.Figure) -> None:
    """Adds a subtle κ_D watermark annotation to the figure."""
    fig.text(
        0.99, 0.01,
        f"κ_D = 0.56  |  © 2026 Gonzalo Emir Durante",
        ha="right", va="bottom", fontsize=7,
        color="#555577", style="italic"
    )


def _save_and_show(
    fig: plt.Figure,
    save_path: Optional[Path],
    show: bool,
) -> None:
    """Saves and/or displays the figure.

    Args:
        fig: The figure to save/show.
        save_path: If provided, saves as a PNG at this path.
        show: If True, calls plt.show().
    """
    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=_DPI, bbox_inches="tight", facecolor=fig.get_facecolor())
        logger.info("Figure saved to: %s", save_path)
    if show:
        plt.show()
    else:
        plt.close(fig)