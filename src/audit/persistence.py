"""
Project Manifold 0.56 — Topological Scanner
=============================================
Architect: Gonzalo Emir Durante
Phase:     III — Persistent Homology (Part 2: Hole Detection)

Description:
    Computes persistence diagrams and Betti numbers from the distance matrix
    produced by FiltrationProcessor (filtration.py). This is the core
    hallucination-detection mechanism of Phase III.

    A persistent H1 cycle represents a "logical loop with no basis" — a closed
    chain of reasoning that never resolves to a grounded fact. The longer the
    lifetime of such a cycle, the more severe the semantic gap. The stability
    score returned by this scanner is the primary input to the Phase VI
    InvarianceMonitor.

    Dependency: ripser, persim
        pip install ripser persim
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Optional dependency guard — graceful degradation if ripser is unavailable
# ---------------------------------------------------------------------------
try:
    from ripser import ripser
    from persim import plot_diagrams as _plot_diagrams
    _RIPSER_AVAILABLE = True
except ImportError:
    _RIPSER_AVAILABLE = False
    logger.warning(
        "Optional dependencies 'ripser' and/or 'persim' are not installed. "
        "TopologicalScanner will operate in degraded mode. "
        "Install with: pip install ripser persim"
    )


class TopologicalScanner:
    """Detects logical holes (hallucinations) via Persistent Homology.

    Wraps the Ripser persistent homology library to compute H0 and H1
    persistence diagrams from a pairwise distance matrix. The H1 diagram
    exposes cyclic reasoning patterns that lack a grounded base — the
    topological signature of hallucination in the Manifold 0.56 model.

    The normalised stability score ∈ [0, 1] is derived from the maximum
    H1 cycle lifetime: longer-lived holes correspond to lower scores, which
    may trigger Class B or NULL certification in the Phase VI monitor.

    Attributes:
        max_dim (int): Maximum homology dimension to compute (default 1).
            Dimension 1 captures loops (potential hallucinations).
        min_persistence (float): Minimum lifetime threshold below which
            H1 features are treated as topological noise and ignored.

    Example:
        >>> scanner = TopologicalScanner()
        >>> score = scanner.compute_stability_score(dist_matrix)
        >>> print(f"Stability: {score:.4f}")
    """

    def __init__(
        self,
        max_dim: int = 1,
        min_persistence: float = 1e-6,
    ) -> None:
        """Initialises the TopologicalScanner.

        Args:
            max_dim: Maximum homology dimension. Dimension 1 captures H1 cycles
                (loops). Increasing this is computationally expensive.
            min_persistence: Minimum H1 feature lifetime to be considered
                significant. Features with lifetime < this value are treated as
                numerical noise and discarded.

        Raises:
            RuntimeError: If ripser is not installed and strict mode is required.
            ValueError: If `max_dim` < 1 or `min_persistence` < 0.
        """
        if max_dim < 1:
            raise ValueError(f"`max_dim` must be ≥ 1. Received: {max_dim}")
        if min_persistence < 0.0:
            raise ValueError(
                f"`min_persistence` must be ≥ 0. Received: {min_persistence}"
            )
        self.max_dim = max_dim
        self.min_persistence = min_persistence

    def compute_persistence(
        self,
        dist_matrix: NDArray[np.float64],
    ) -> list[NDArray[np.float64]]:
        """Computes full persistence diagrams for all homology dimensions.

        Args:
            dist_matrix: Symmetric pairwise distance matrix of shape (N, N),
                as produced by :class:`FiltrationProcessor`.

        Returns:
            List of persistence diagrams, one per homology dimension.
            Each diagram is an NDArray of shape (K, 2) with columns
            [birth, death] for each topological feature.

        Raises:
            RuntimeError: If ripser is not available.
            ValueError: If `dist_matrix` is not a valid symmetric 2D array
                or has fewer than 2 points.
        """
        self._validate_distance_matrix(dist_matrix)
        if not _RIPSER_AVAILABLE:
            raise RuntimeError(
                "ripser is required for persistence computation. "
                "Install with: pip install ripser persim"
            )
        result = ripser(dist_matrix, maxdim=self.max_dim, distance_matrix=True)
        return result["dgms"]

    def compute_stability_score(
        self,
        dist_matrix: NDArray[np.float64],
    ) -> float:
        """Computes a normalised stability score from H1 persistence.

        Derives the stability score from the maximum H1 cycle lifetime.
        A score of 1.0 indicates no persistent logical holes (full coherence).
        Scores decrease as the longest-lived H1 cycle grows, reflecting
        increasingly severe semantic gaps.

        Formula:
            score = 1 / (1 + max_lifetime)

        where `max_lifetime` is the maximum finite H1 feature lifetime after
        filtering noise below `min_persistence`.

        Args:
            dist_matrix: Symmetric pairwise distance matrix of shape (N, N).

        Returns:
            Stability score ∈ (0, 1]. Returns 1.0 if no significant H1
            features are found (perfectly coherent manifold).

        Raises:
            ValueError: If `dist_matrix` is malformed.

        Example:
            >>> score = scanner.compute_stability_score(dist_matrix)
            >>> assert 0.0 < score <= 1.0
        """
        self._validate_distance_matrix(dist_matrix)

        if not _RIPSER_AVAILABLE:
            logger.warning(
                "ripser is unavailable. Returning degraded stability score 0.0."
            )
            return 0.0

        diagrams = self.compute_persistence(dist_matrix)

        # H1 diagram: cycles representing potential logical holes
        h1: NDArray[np.float64] = diagrams[1] if len(diagrams) > 1 else np.empty((0, 2))

        # Filter out infinite-death features and noise below min_persistence
        finite_mask = np.isfinite(h1[:, 1])
        h1_finite = h1[finite_mask]

        if h1_finite.shape[0] == 0:
            return 1.0  # No persistent cycles — manifold is fully coherent

        lifetimes: NDArray[np.float64] = h1_finite[:, 1] - h1_finite[:, 0]

        # Discard sub-threshold noise features
        significant = lifetimes[lifetimes >= self.min_persistence]
        if significant.shape[0] == 0:
            return 1.0

        max_lifetime: float = float(np.max(significant))
        return 1.0 / (1.0 + max_lifetime)

    def betti_numbers(
        self,
        dist_matrix: NDArray[np.float64],
        threshold: Optional[float] = None,
    ) -> dict[int, int]:
        """Computes Betti numbers at a given filtration threshold.

        Betti numbers count the number of topological features (connected
        components, loops, voids) that are alive at a given radius.

        Args:
            dist_matrix: Symmetric pairwise distance matrix of shape (N, N).
            threshold: Filtration radius at which to count living features.
                Defaults to the median of all pairwise distances.

        Returns:
            Dict mapping homology dimension → Betti number.
            e.g. {0: 3, 1: 1} means 3 connected components and 1 loop.

        Raises:
            ValueError: If `dist_matrix` is malformed.
        """
        self._validate_distance_matrix(dist_matrix)
        diagrams = self.compute_persistence(dist_matrix)

        if threshold is None:
            threshold = float(np.median(dist_matrix[dist_matrix > 0]))

        betti: dict[int, int] = {}
        for dim, dgm in enumerate(diagrams):
            if dgm.shape[0] == 0:
                betti[dim] = 0
                continue
            # Count features alive at the given threshold (born ≤ t < death)
            alive = np.sum(
                (dgm[:, 0] <= threshold)
                & (
                    np.where(np.isfinite(dgm[:, 1]), dgm[:, 1], np.inf)
                    > threshold
                )
            )
            betti[dim] = int(alive)

        return betti

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_distance_matrix(dist_matrix: NDArray[np.float64]) -> None:
        """Validates that `dist_matrix` is a proper symmetric square matrix.

        Args:
            dist_matrix: Matrix to validate.

        Raises:
            ValueError: If the matrix is not 2D, not square, or has fewer
                than 2 points.
        """
        if dist_matrix.ndim != 2:
            raise ValueError(
                f"Distance matrix must be 2D. Received shape: {dist_matrix.shape}"
            )
        n, m = dist_matrix.shape
        if n != m:
            raise ValueError(
                f"Distance matrix must be square (N×N). Received: {n}×{m}"
            )
        if n < 2:
            raise ValueError(
                f"Distance matrix must have at least 2 points. Received: {n}"
            )

    def __repr__(self) -> str:
        return (
            f"TopologicalScanner("
            f"max_dim={self.max_dim}, "
            f"min_persistence={self.min_persistence})"
        )
