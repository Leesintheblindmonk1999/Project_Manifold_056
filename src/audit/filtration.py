"""
Project Manifold 0.56 — Filtration Processor
==============================================
Architect: Gonzalo Emir Durante
Phase:     III — Persistent Homology (Part 1: Complex Construction)

Description:
    Constructs the Vietoris-Rips distance matrix from a point cloud of semantic
    embeddings. This is the first stage of the Phase III topological audit:
    the distance matrix produced here is consumed by the TopologicalScanner
    (persistence.py) to compute persistence diagrams and Betti numbers.

    A Vietoris-Rips complex captures the "shape" of the data at every scale
    simultaneously. Logical holes in the manifold (potential hallucinations)
    manifest as persistent H1 cycles in the resulting persistence diagram.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


class FiltrationProcessor:
    """Prepares semantic point clouds for topological filtration.

    Converts a matrix of high-dimensional embedding vectors into a pairwise
    Euclidean distance matrix suitable for Vietoris-Rips complex construction.
    Optionally clips distances at `max_radius` to focus the analysis on local
    topological structure within the invariance neighbourhood.

    Attributes:
        max_radius (float): Maximum filtration radius. Distances beyond this
            threshold are clamped, restricting the complex to the local manifold.

    Example:
        >>> processor = FiltrationProcessor(max_radius=1.0)
        >>> dist_matrix = processor.build_vietoris_rips(embeddings)
        >>> dist_matrix.shape
        (N, N)
    """

    def __init__(self, max_radius: float = 1.0) -> None:
        """Initialises the filtration processor.

        Args:
            max_radius: Maximum filtration radius for the Vietoris-Rips complex.
                Pairwise distances exceeding this value are clamped, preventing
                the formation of spurious long-range topological features.

        Raises:
            ValueError: If `max_radius` is not strictly positive.
        """
        if max_radius <= 0.0:
            raise ValueError(
                f"`max_radius` must be strictly positive. Received: {max_radius}"
            )
        self.max_radius = max_radius

    def build_vietoris_rips(
        self,
        data_points: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Computes the pairwise Euclidean distance matrix for a point cloud.

        Constructs the symmetric distance matrix required to build a
        Vietoris-Rips filtration. Uses a fully vectorised NumPy implementation
        (O(N² · D) time, O(N²) space) — significantly faster than the nested
        loop approach for large point clouds.

        Distances beyond `self.max_radius` are clamped to `max_radius` to
        confine the topological analysis to the invariance neighbourhood defined
        by the Durante Constant.

        Args:
            data_points: NDArray of shape (N, D) where N is the number of
                semantic concept embeddings and D is the embedding dimension.
                Requires N ≥ 2 to form at least one non-trivial simplex.

        Returns:
            Symmetric NDArray of shape (N, N) containing pairwise Euclidean
            distances, clamped at `max_radius`. Diagonal entries are 0.

        Raises:
            ValueError: If `data_points` is not a 2D array or contains fewer
                than 2 points.

        Example:
            >>> import numpy as np
            >>> pts = np.random.randn(50, 64)
            >>> processor = FiltrationProcessor(max_radius=2.0)
            >>> D = processor.build_vietoris_rips(pts)
            >>> assert D.shape == (50, 50)
            >>> assert np.allclose(D, D.T)  # symmetric
        """
        if data_points.ndim != 2:
            raise ValueError(
                f"`data_points` must be a 2D array of shape (N, D). "
                f"Received shape: {data_points.shape}"
            )
        n_points = data_points.shape[0]
        if n_points < 2:
            raise ValueError(
                f"At least 2 points are required to build a Vietoris-Rips complex. "
                f"Received: {n_points}"
            )

        # Vectorised pairwise L2 distance via broadcasting: O(N² · D)
        # diff[i, j] = data_points[i] - data_points[j]
        diff: NDArray[np.float64] = (
            data_points[:, np.newaxis, :] - data_points[np.newaxis, :, :]
        )
        dist_matrix: NDArray[np.float64] = np.sqrt(
            np.einsum("ijk,ijk->ij", diff, diff)
        )

        # Clamp distances to the filtration radius (local manifold constraint)
        np.clip(dist_matrix, a_min=0.0, a_max=self.max_radius, out=dist_matrix)

        # Enforce exact symmetry and zero diagonal (guards against float drift)
        dist_matrix = (dist_matrix + dist_matrix.T) / 2.0
        np.fill_diagonal(dist_matrix, 0.0)

        return dist_matrix

    def __repr__(self) -> str:
        return f"FiltrationProcessor(max_radius={self.max_radius})"
