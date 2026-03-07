"""
Utils — Cross-cutting Utilities
Normalisation · Semantic Entropy · Visualisation Suite
"""

from src.utils.helpers import (
    normalize_manifold,
    calculate_entropy,
    compute_pipeline_scores_summary,
    clip_to_invariance_sphere,
)
from src.utils.plotting import (
    plot_persistence_barcodes,
    plot_stability_gauge,
    plot_stability_radar,
    plot_full_report,
)

__all__ = [
    "normalize_manifold",
    "calculate_entropy",
    "compute_pipeline_scores_summary",
    "clip_to_invariance_sphere",
    "plot_persistence_barcodes",
    "plot_stability_gauge",
    "plot_stability_radar",
    "plot_full_report",
]
