"""
Project Manifold 0.56 — Utility Helpers
=========================================
Architect: Gonzalo Emir Durante
Phase:     Cross-cutting (Phases I–VI support)

Description:
    Data preparation and diagnostic utilities used across the Manifold 0.56
    pipeline. These functions handle the normalisation, standardisation, and
    entropy analysis of semantic point clouds before and after they pass
    through the core audit stages (Filtration → Topology → Ricci → Simplex).

    All functions are stateless and operate on NumPy arrays for maximum
    composability with the rest of the engine.
"""

from __future__ import annotations

import logging
from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from src.core.constants import DURANTE_CONSTANT, ENTROPY_LIMIT

logger = logging.getLogger(__name__)


def normalize_manifold(
    points: NDArray[np.float64],
    center: bool = True,
    scale: bool = True,
) -> NDArray[np.float64]:
    """Centers and optionally scales a semantic point cloud for pipeline ingestion.

    Translates the point cloud so its centroid lies at the origin (zero-mean),
    and optionally scales it so that the maximum L2 norm of any point equals 1.
    This ensures the manifold fits within the invariance hypersphere of radius κ_D
    and prevents numerical overflow in downstream geometric operations.

    Args:
        points: NDArray of shape (N, D) representing N semantic embeddings in
            D-dimensional space. Must be a non-empty 2D array.
        center: If True (default), subtract the column-wise mean so that the
            centroid of the point cloud lies at the origin.
        scale: If True (default), divide by the maximum L2 norm across all
            points so that the furthest point lies on the unit hypersphere.
            If the maximum norm is zero (degenerate cloud), scaling is skipped.

    Returns:
        NDArray of shape (N, D) — the normalised point cloud.

    Raises:
        ValueError: If `points` is not a non-empty 2D array.

    Example:
        >>> import numpy as np
        >>> pts = np.random.randn(100, 64) * 5 + 3  # off-centre, large scale
        >>> normed = normalize_manifold(pts)
        >>> np.testing.assert_allclose(normed.mean(axis=0), 0, atol=1e-10)
    """
    _validate_points(points)
    result = points.astype(np.float64, copy=True)

    if center:
        result -= result.mean(axis=0)

    if scale:
        max_norm = float(np.max(np.linalg.norm(result, axis=1)))
        if max_norm > 0.0:
            result /= max_norm
        else:
            logger.warning(
                "normalize_manifold: all points have zero norm after centering. "
                "Scaling step skipped."
            )

    return result


def calculate_entropy(stability_score: float) -> float:
    """Computes the Semantic Entropy from a stability score.

    Semantic Entropy is defined as the complement of the stability score:
        H_semantic = 1.0 − stability_score

    This maps directly to the thermodynamic intuition in Phase I: as stability
    approaches κ_D (0.56), entropy approaches the ENTROPY_LIMIT (0.44).
    When entropy exceeds 0.56, the system is in a super-critical state and
    the manifold is considered collapsed.

    Args:
        stability_score: Normalised stability score ∈ [0, 1] from the
            audit pipeline.

    Returns:
        Semantic entropy ∈ [0, 1]. Values above ENTROPY_LIMIT (0.44) indicate
        a manifold at risk of collapse.

    Raises:
        ValueError: If `stability_score` is outside [0, 1].

    Example:
        >>> calculate_entropy(0.56)
        0.44
        >>> calculate_entropy(0.38)
        0.62
    """
    if not (0.0 <= stability_score <= 1.0):
        raise ValueError(
            f"`stability_score` must be in [0, 1]. Received: {stability_score}"
        )
    return round(1.0 - stability_score, 10)


def compute_pipeline_scores_summary(
    topo_score: float,
    ricci_score: float,
    simplex_score: float,
) -> dict[str, float]:
    """Computes a summary of all pipeline scores with derived diagnostics.

    Aggregates the three main pipeline scores and derives additional metrics:
    arithmetic mean, harmonic mean (composite), and the semantic entropy of
    the composite score.

    Args:
        topo_score: Topological stability score ∈ (0, 1].
        ricci_score: Ricci truth density score ∈ (0, 1].
        simplex_score: Simplicial structural integrity ∈ (0, 1].

    Returns:
        Dict with keys: topo, ricci, simplex, arithmetic_mean,
        harmonic_mean (composite), entropy, passes_kD.

    Raises:
        ValueError: If any score is outside (0, 1].

    Example:
        >>> summary = compute_pipeline_scores_summary(0.71, 0.68, 0.74)
        >>> summary['passes_kD']
        True
    """
    for name, score in [
        ("topo_score", topo_score),
        ("ricci_score", ricci_score),
        ("simplex_score", simplex_score),
    ]:
        if not (0.0 < score <= 1.0):
            raise ValueError(f"`{name}` must be in (0, 1]. Received: {score}")

    arithmetic_mean = (topo_score + ricci_score + simplex_score) / 3.0
    harmonic_mean = 3.0 / (1.0 / topo_score + 1.0 / ricci_score + 1.0 / simplex_score)
    entropy = calculate_entropy(min(harmonic_mean, 1.0))

    return {
        "topo": round(topo_score, 6),
        "ricci": round(ricci_score, 6),
        "simplex": round(simplex_score, 6),
        "arithmetic_mean": round(arithmetic_mean, 6),
        "harmonic_mean": round(harmonic_mean, 6),
        "entropy": round(entropy, 6),
        "passes_kD": harmonic_mean >= DURANTE_CONSTANT,
        "entropy_within_limit": entropy <= ENTROPY_LIMIT,
    }


def clip_to_invariance_sphere(
    points: NDArray[np.float64],
    radius: float = DURANTE_CONSTANT,
) -> Tuple[NDArray[np.float64], int]:
    """Clips point cloud vectors to lie within the κ_D invariance hypersphere.

    Any node whose L2 norm exceeds `radius` is projected back onto the surface
    of the sphere. This enforces the hard geometric boundary imposed by the
    Durante Constant in Phase II.

    Args:
        points: NDArray of shape (N, D).
        radius: Hypersphere radius (default κ_D = 0.56).

    Returns:
        Tuple of:
            - Clipped NDArray of shape (N, D).
            - Number of points that were projected (clipped).

    Raises:
        ValueError: If `points` is not a valid 2D array.
    """
    _validate_points(points)
    norms: NDArray[np.float64] = np.linalg.norm(points, axis=1, keepdims=True)
    scale = np.where(norms > radius, radius / np.maximum(norms, np.finfo(float).eps), 1.0)
    clipped = points * scale
    num_clipped = int(np.sum(norms.squeeze() > radius))
    return clipped, num_clipped


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------

def _validate_points(points: NDArray[np.float64]) -> None:
    """Validates that `points` is a non-empty 2D array.

    Args:
        points: Array to validate.

    Raises:
        ValueError: If array is not 2D or has zero rows.
    """
    if points.ndim != 2 or points.shape[0] == 0:
        raise ValueError(
            f"Expected a non-empty 2D array of shape (N, D). "
            f"Received shape: {points.shape}"
        )