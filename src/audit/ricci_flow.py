"""
Project Manifold 0.56 — Ricci Flow Aggregator
===============================================
Architect: Gonzalo Emir Durante
Phase:     IV — Ricci Flow Aggregation (Truth Density & Bias Removal)

Description:
    Applies a discrete, iterative approximation of the Ricci Flow equation to
    homogenise truth density across the semantic manifold. Regions of high
    curvature correspond to induced biases or semantic irregularities;
    iterating the flow smooths these out toward a uniform density state.

    The governing equation (Hamilton, 1982) is:
        ∂g_ij / ∂t = −2 R_ij

    In this discrete implementation, point-wise variance serves as a proxy for
    Ricci curvature: high variance in a neighbourhood signals a "bumpy" region
    of the manifold that requires smoothing.

    The truth density score emitted by this aggregator is passed downstream to
    the Phase VI InvarianceMonitor for final certification.
"""

from __future__ import annotations

import logging
from typing import Optional, Tuple

import numpy as np
from numpy.typing import NDArray

from src.core.constants import RICCI_FLOW_STEP

logger = logging.getLogger(__name__)


class RicciAggregator:
    """Discrete Ricci Flow engine for semantic bias removal.

    Iteratively smooths a point cloud representing the semantic manifold by
    applying gradient-descent updates proportional to the local curvature
    (approximated by per-feature variance). Converges toward a state of
    uniform truth density, as required by Phase IV of the Manifold 0.56 doctrine.

    Attributes:
        step (float): Flow step size ε controlling the rate of smoothing.
        max_iterations (int): Maximum number of flow iterations.
        convergence_tol (float): Early-stop tolerance on the Frobenius norm
            of successive manifold updates.

    Example:
        >>> aggregator = RicciAggregator(step=0.01, max_iterations=50)
        >>> smoothed, score = aggregator.smooth_manifold(manifold_points)
        >>> print(f"Truth density score: {score:.4f}")
    """

    def __init__(
        self,
        step: float = RICCI_FLOW_STEP,
        max_iterations: int = 100,
        convergence_tol: float = 1e-6,
    ) -> None:
        """Initialises the Ricci Flow aggregator.

        Args:
            step: Flow step size ε for the discrete metric evolution.
                Small values (e.g. 0.01) yield stable, gradual smoothing.
                Values > 0.1 risk overshooting and manifold inversion.
            max_iterations: Maximum number of smoothing iterations before
                forced termination.
            convergence_tol: Frobenius norm threshold for early stopping.
                The flow halts when ‖Δmanifold‖_F < convergence_tol.

        Raises:
            ValueError: If `step` ≤ 0, `max_iterations` < 1, or
                `convergence_tol` < 0.
        """
        if step <= 0.0:
            raise ValueError(f"`step` must be > 0. Received: {step}")
        if max_iterations < 1:
            raise ValueError(
                f"`max_iterations` must be ≥ 1. Received: {max_iterations}"
            )
        if convergence_tol < 0.0:
            raise ValueError(
                f"`convergence_tol` must be ≥ 0. Received: {convergence_tol}"
            )

        self.step = step
        self.max_iterations = max_iterations
        self.convergence_tol = convergence_tol

    def smooth_manifold(
        self,
        manifold_points: NDArray[np.float64],
        return_history: bool = False,
    ) -> Tuple[NDArray[np.float64], float]:
        """Applies discrete Ricci Flow to homogenise semantic truth density.

        Iterates the update rule:
            manifold ← manifold − 2 · Var(manifold, axis=0) · ε

        where Var(·, axis=0) is the per-feature variance across all points,
        acting as a proxy for Ricci curvature in the neighbourhood.

        The process terminates early if the Frobenius norm of the update
        falls below `convergence_tol`, signalling that the manifold has
        reached a sufficiently uniform density state.

        Args:
            manifold_points: NDArray of shape (N, D) representing N semantic
                concept embeddings in D-dimensional space. Must contain at
                least 2 points to compute meaningful curvature.
            return_history: If True, convergence norms are logged at DEBUG
                level for diagnostic purposes.

        Returns:
            Tuple of:
                - smoothed_manifold: NDArray of shape (N, D) after flow.
                - truth_density_score: Float ∈ (0, 1]. Measures residual
                  curvature after smoothing; higher values indicate a more
                  uniform, less biased manifold. Computed as
                  1 / (1 + mean_residual_variance).

        Raises:
            ValueError: If `manifold_points` is not a 2D array with ≥ 2 rows,
                or if it contains NaN or Inf values.

        Example:
            >>> pts = np.random.randn(200, 64)
            >>> agg = RicciAggregator(step=0.01, max_iterations=50)
            >>> smoothed, score = agg.smooth_manifold(pts)
            >>> assert score > 0.0
        """
        self._validate_points(manifold_points)

        current: NDArray[np.float64] = manifold_points.copy()
        iterations_run = 0

        for i in range(self.max_iterations):
            curvature: NDArray[np.float64] = np.var(current, axis=0)  # shape: (D,)
            adjustment: NDArray[np.float64] = -2.0 * curvature * self.step

            # Broadcast adjustment across all N points
            updated = current + adjustment[np.newaxis, :]

            delta_norm = float(np.linalg.norm(updated - current, ord="fro"))
            current = updated
            iterations_run = i + 1

            if return_history:
                logger.debug(
                    "Ricci Flow iteration %d — Δ‖manifold‖_F = %.8f",
                    i + 1,
                    delta_norm,
                )

            if delta_norm < self.convergence_tol:
                logger.info(
                    "Ricci Flow converged at iteration %d (Δ = %.2e < tol %.2e).",
                    iterations_run,
                    delta_norm,
                    self.convergence_tol,
                )
                break
        else:
            logger.warning(
                "Ricci Flow reached max_iterations=%d without converging. "
                "Consider increasing max_iterations or adjusting step size.",
                self.max_iterations,
            )

        truth_density_score = self._compute_truth_density(current)
        return current, truth_density_score

    def compute_curvature_map(
        self,
        manifold_points: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Returns the per-feature curvature proxy (variance) of the manifold.

        Useful for diagnostic visualisation (e.g. via utils/plotting.py) to
        identify which semantic dimensions carry the highest bias load before
        and after smoothing.

        Args:
            manifold_points: NDArray of shape (N, D).

        Returns:
            NDArray of shape (D,) containing per-feature variance values.
            High values indicate biased or irregular semantic dimensions.

        Raises:
            ValueError: If `manifold_points` is invalid.
        """
        self._validate_points(manifold_points)
        return np.var(manifold_points, axis=0)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_truth_density(points: NDArray[np.float64]) -> float:
        """Computes a normalised truth density score from residual curvature.

        Args:
            points: Smoothed manifold NDArray of shape (N, D).

        Returns:
            Score ∈ (0, 1]. Approaches 1.0 as variance → 0.
        """
        mean_variance: float = float(np.mean(np.var(points, axis=0)))
        return 1.0 / (1.0 + mean_variance)

    @staticmethod
    def _validate_points(points: NDArray[np.float64]) -> None:
        """Validates manifold point array.

        Args:
            points: Array to validate.

        Raises:
            ValueError: If array is not 2D, has fewer than 2 rows,
                or contains non-finite values.
        """
        if points.ndim != 2:
            raise ValueError(
                f"`manifold_points` must be 2D (N, D). Received shape: {points.shape}"
            )
        if points.shape[0] < 2:
            raise ValueError(
                f"At least 2 points are required for curvature estimation. "
                f"Received: {points.shape[0]}"
            )
        if not np.all(np.isfinite(points)):
            raise ValueError(
                "`manifold_points` contains NaN or Inf values. "
                "Clean your data before applying Ricci Flow."
            )

    def __repr__(self) -> str:
        return (
            f"RicciAggregator("
            f"step={self.step}, "
            f"max_iterations={self.max_iterations}, "
            f"convergence_tol={self.convergence_tol})"
        )
