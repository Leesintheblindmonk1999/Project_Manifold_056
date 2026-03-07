"""
Project Manifold 0.56 — Simplex Engine
========================================
Architect: Gonzalo Emir Durante
Phase:     V — High-Dimensional Simplices (Superior Intelligence)

Description:
    Models semantic truth as indivisible n-dimensional simplicial structures
    rather than linear reasoning chains. A k-simplex formed by k+1 information
    nodes encodes the total mutual interconnection of those concepts — if any
    node drifts, the entire simplicial structure degrades.

    This is the geometric heart of Phase V: truth is not a link between two
    ideas, but a solid, high-dimensional polytope that either holds its shape
    or collapses. The Structural Integrity score produced here feeds into the
    final composite score used by the Phase VI certification pipeline.

    Mathematical foundation:
        - Barycenter: centroid of all node vectors → equilibrium point of
          semantic truth.
        - Structural Integrity: 1 / (1 + σ²) where σ² is the mean intra-simplex
          variance. Dispersion = instability.
        - Simplicial volume: approximated via the Cayley-Menger-inspired
          mean pairwise distance between nodes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from src.core.constants import DURANTE_CONSTANT


@dataclass
class SimplexResult:
    """Structured result produced by :meth:`SimplexEngine.build_high_dim_simplex`.

    Attributes:
        dimension: Topological dimension of the simplex (= num_nodes − 1).
        num_nodes: Number of information nodes forming the simplex.
        barycenter: NDArray of shape (D,) — the semantic equilibrium point.
        structural_integrity: Float ∈ (0, 1]. Measures cohesion of the simplex.
            Values ≥ κ_D (0.56) indicate a stable truth structure.
        mean_edge_length: Mean pairwise distance between nodes (simplicial volume proxy).
        certified: True if structural_integrity ≥ κ_D.
    """
    dimension: int
    num_nodes: int
    barycenter: NDArray[np.float64]
    structural_integrity: float
    mean_edge_length: float
    certified: bool = field(init=False)

    def __post_init__(self) -> None:
        self.certified = self.structural_integrity >= DURANTE_CONSTANT

    def summary(self) -> str:
        """Returns a compact diagnostic string for console output."""
        status = "✓ CERTIFIED" if self.certified else "✗ UNSTABLE"
        return (
            f"Simplex [{status}] | "
            f"dim={self.dimension} | "
            f"nodes={self.num_nodes} | "
            f"integrity={self.structural_integrity:.4f} | "
            f"mean_edge={self.mean_edge_length:.4f}"
        )


class SimplexEngine:
    """Constructs and evaluates high-dimensional simplicial truth structures.

    A simplex formed from k+1 nodes is the tightest possible encoding of
    mutual coherence between k+1 concepts. Unlike a graph (pairwise links),
    a simplex demands *total* interconnection — one incoherent node destabilises
    the entire structure, mirroring how a single false premise can corrupt a
    chain of reasoning.

    Attributes:
        dim (int): Expected embedding dimensionality of input nodes.
        k_d (float): The Durante Constant used as the certification threshold.

    Example:
        >>> engine = SimplexEngine(dimension=128)
        >>> nodes = np.random.randn(5, 128)
        >>> result = engine.build_high_dim_simplex(nodes)
        >>> print(result.summary())
    """

    def __init__(
        self,
        dimension: int = 128,
        k_d: float = DURANTE_CONSTANT,
    ) -> None:
        """Initialises the Simplex Engine.

        Args:
            dimension: Expected embedding dimensionality of input node vectors.
                Used for validation; does not constrain the simplex dimension.
            k_d: The Durante Constant κ_D used as the certification threshold
                for structural integrity. Must be in (0, 1].

        Raises:
            ValueError: If `dimension` < 2 or `k_d` is outside (0, 1].
        """
        if dimension < 2:
            raise ValueError(f"`dimension` must be ≥ 2. Received: {dimension}")
        if not (0.0 < k_d <= 1.0):
            raise ValueError(f"`k_d` must be in (0, 1]. Received: {k_d}")

        self.dim = dimension
        self.k_d = k_d

    def build_high_dim_simplex(
        self,
        nodes: NDArray[np.float64],
    ) -> Optional[SimplexResult]:
        """Constructs a high-dimensional simplex from a set of information nodes.

        Models semantic truth as a (k)-simplex formed by k+1 nodes, computing:
            - The barycenter: mean position = semantic equilibrium point.
            - Structural integrity: cohesion score derived from intra-simplex
              variance. High dispersion → low integrity → unstable reasoning.
            - Mean edge length: proxy for simplicial volume (spread of truth).

        A simplex with integrity ≥ κ_D (0.56) is certified as a stable truth
        structure. Below that threshold, the reasoning is considered fragile and
        susceptible to semantic collapse.

        Args:
            nodes: NDArray of shape (N, D) where N ≥ 2 is the number of
                information nodes and D is the embedding dimension. Each row
                is a concept vector on the semantic manifold.

        Returns:
            A :class:`SimplexResult` containing the geometric properties of the
            simplex, or None if `nodes` has fewer than 2 rows.

        Raises:
            ValueError: If `nodes` is not a 2D array or contains non-finite values.

        Example:
            >>> nodes = np.random.randn(6, 128)
            >>> result = engine.build_high_dim_simplex(nodes)
            >>> assert result.dimension == 5  # 6 nodes → 5-simplex
        """
        if nodes.ndim != 2:
            raise ValueError(
                f"`nodes` must be a 2D array of shape (N, D). "
                f"Received shape: {nodes.shape}"
            )
        if not np.all(np.isfinite(nodes)):
            raise ValueError("`nodes` contains NaN or Inf values.")

        num_nodes = nodes.shape[0]
        if num_nodes < 2:
            return None  # Cannot form a simplex from a single node

        # --- Barycenter: semantic equilibrium point of the simplex ---
        barycenter: NDArray[np.float64] = np.mean(nodes, axis=0)

        # --- Structural Integrity via intra-simplex variance ---
        # Variance across all nodes and all dimensions → scalar dispersion proxy
        mean_variance: float = float(np.mean(np.var(nodes, axis=0)))
        structural_integrity: float = 1.0 / (1.0 + mean_variance)

        # --- Mean edge length: pairwise L2 distances (simplicial volume proxy) ---
        mean_edge_length = self._compute_mean_edge_length(nodes)

        return SimplexResult(
            dimension=num_nodes - 1,
            num_nodes=num_nodes,
            barycenter=barycenter,
            structural_integrity=structural_integrity,
            mean_edge_length=mean_edge_length,
        )

    def compute_barycentric_coordinates(
        self,
        point: NDArray[np.float64],
        nodes: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Computes barycentric coordinates of a point relative to a simplex.

        Barycentric coordinates express how a point decomposes as a weighted
        sum of the simplex vertices. A point inside the simplex has all
        non-negative weights summing to 1 — it is "contained" within the
        truth structure.

        Args:
            point: NDArray of shape (D,) — the query concept vector.
            nodes: NDArray of shape (N, D) — the simplex vertices (N ≥ 2).

        Returns:
            NDArray of shape (N,) containing the barycentric weights.
            Negative weights indicate the point lies outside the simplex.

        Raises:
            ValueError: If shapes are incompatible or inputs are invalid.
        """
        if point.ndim != 1 or nodes.ndim != 2:
            raise ValueError(
                "Expected `point` of shape (D,) and `nodes` of shape (N, D)."
            )
        if point.shape[0] != nodes.shape[1]:
            raise ValueError(
                f"Dimension mismatch: point has D={point.shape[0]}, "
                f"nodes have D={nodes.shape[1]}."
            )

        # Use least-squares projection for over-determined high-dim systems
        # Solve: nodes.T @ w = point, subject to sum(w) = 1
        n = nodes.shape[0]
        # Augmented system for affine constraint
        A = np.vstack([nodes.T, np.ones((1, n))])        # (D+1, N)
        b = np.append(point, 1.0)                         # (D+1,)
        weights, *_ = np.linalg.lstsq(A, b, rcond=None)
        return weights

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_mean_edge_length(nodes: NDArray[np.float64]) -> float:
        """Computes mean pairwise L2 distance between simplex nodes.

        Args:
            nodes: NDArray of shape (N, D).

        Returns:
            Mean pairwise distance as a float. Returns 0.0 for N < 2.
        """
        diff = nodes[:, np.newaxis, :] - nodes[np.newaxis, :, :]
        dist_matrix = np.sqrt(np.einsum("ijk,ijk->ij", diff, diff))
        # Upper triangle only (exclude diagonal = 0)
        upper = dist_matrix[np.triu_indices(nodes.shape[0], k=1)]
        return float(np.mean(upper)) if upper.size > 0 else 0.0

    def __repr__(self) -> str:
        return f"SimplexEngine(dim={self.dim}, k_d={self.k_d})"