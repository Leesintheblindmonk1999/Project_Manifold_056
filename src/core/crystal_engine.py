"""
Project Manifold 0.56 — Crystal Engine
========================================
Architect: Gonzalo Emir Durante
Phase:     II — Crystal Network (Non-Euclidean Topology)

Description:
    Constructs the rigid non-Euclidean lattice that forms the geometric backbone
    of the Manifold 0.56 framework. Information nodes are projected onto a
    hypersphere of radius κ_D, ensuring that no two concepts drift beyond the
    invariance boundary or collapse into a degenerate singularity.

    The cohesion score produced by :meth:`CrystalEngine.calculate_cohesion`
    feeds directly into the Phase III audit pipeline (FiltrationProcessor).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from src.core.constants import CRYSTAL_LATTICE_DENSITY, DURANTE_CONSTANT


class CrystalEngine:
    """Generates and evaluates Non-Euclidean Crystal Network lattices.

    Each node in the lattice is a high-dimensional unit vector scaled by the
    Durante Constant (κ_D), so that inter-node distances are bounded by the
    invariance manifold. This prevents semantic drift and concept collision as
    defined in Phase II of the Manifold 0.56 doctrine.

    Attributes:
        dim (int): Embedding dimensionality of each lattice node.
        k_d (float): The Durante Constant used as the hypersphere radius.
        lattice_density (float): Node density per unit non-Euclidean volume.

    Example:
        >>> engine = CrystalEngine(dimension=128)
        >>> lattice = engine.generate_lattice(num_nodes=500)
        >>> cohesion = engine.calculate_cohesion(lattice)
        >>> assert 0.0 < cohesion <= 1.0
    """

    def __init__(
        self,
        dimension: int = 128,
        k_d: float = DURANTE_CONSTANT,
        lattice_density: float = CRYSTAL_LATTICE_DENSITY,
    ) -> None:
        """Initialises the Crystal Engine with geometric parameters.

        Args:
            dimension: Embedding dimensionality for lattice nodes. Higher
                values increase the non-Euclidean resolution of the manifold.
            k_d: The Durante Constant (κ_D). Acts as the hypersphere radius
                onto which all nodes are projected. Must be in (0, 1].
            lattice_density: Target node density per unit non-Euclidean volume.

        Raises:
            ValueError: If `dimension` < 2, or if `k_d` is outside (0, 1].
        """
        if dimension < 2:
            raise ValueError(f"`dimension` must be ≥ 2. Received: {dimension}")
        if not (0.0 < k_d <= 1.0):
            raise ValueError(f"`k_d` must be in (0, 1]. Received: {k_d}")

        self.dim = dimension
        self.k_d = k_d
        self.lattice_density = lattice_density

    def generate_lattice(
        self,
        num_nodes: int = 1000,
        seed: int | None = None,
    ) -> NDArray[np.float64]:
        """Generates a Crystal Network lattice projected onto the κ_D hypersphere.

        Samples random vectors from a standard normal distribution and projects
        each onto a hypersphere of radius κ_D. This ensures all nodes lie on the
        invariance manifold and that the lattice is free of degenerate zero vectors.

        Args:
            num_nodes: Number of nodes to generate. Must be ≥ 1.
            seed: Optional random seed for reproducibility.

        Returns:
            NDArray of shape (num_nodes, dim) where every row is a unit vector
            scaled by κ_D, representing a node on the invariance hypersphere.

        Raises:
            ValueError: If `num_nodes` < 1.

        Example:
            >>> lattice = engine.generate_lattice(num_nodes=256, seed=42)
            >>> lattice.shape
            (256, 128)
        """
        if num_nodes < 1:
            raise ValueError(f"`num_nodes` must be ≥ 1. Received: {num_nodes}")

        rng = np.random.default_rng(seed)
        raw: NDArray[np.float64] = rng.standard_normal((num_nodes, self.dim))

        # Compute L2 norms; add small epsilon to guard against zero-norm vectors
        norms: NDArray[np.float64] = np.linalg.norm(raw, axis=1, keepdims=True)
        norms = np.where(norms == 0.0, np.finfo(float).eps, norms)

        # Project onto the κ_D hypersphere (Phase II invariance constraint)
        return (raw / norms) * self.k_d

    def calculate_cohesion(self, points: NDArray[np.float64]) -> float:
        """Measures the structural cohesion of a Crystal Network lattice.

        Cohesion is defined as the harmonic inverse of the mean L2 norm across
        all nodes. When nodes are tightly clustered around the κ_D radius, the
        cohesion score approaches 1/(1 + κ_D), indicating a stable, well-formed
        manifold. Low cohesion signals geometric dispersion and potential
        semantic drift.

        Args:
            points: NDArray of shape (N, dim) representing lattice node positions.
                Each row should be a vector in the embedding space.

        Returns:
            Cohesion score ∈ (0, 1]. Higher is more stable.

        Raises:
            ValueError: If `points` is empty or not 2-dimensional.

        Example:
            >>> cohesion = engine.calculate_cohesion(lattice)
            >>> print(f"Lattice cohesion: {cohesion:.4f}")
        """
        if points.ndim != 2 or points.shape[0] == 0:
            raise ValueError(
                "`points` must be a non-empty 2D array of shape (N, dim)."
            )

        mean_norm: float = float(np.mean(np.linalg.norm(points, axis=1)))
        return 1.0 / (1.0 + mean_norm)

    def __repr__(self) -> str:
        return (
            f"CrystalEngine(dim={self.dim}, k_d={self.k_d}, "
            f"lattice_density={self.lattice_density})"
        )
