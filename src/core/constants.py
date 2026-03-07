"""
Project Manifold 0.56 — Core Constants
========================================
Architect: Gonzalo Emir Durante
Phase:     I — Semantic Thermodynamic Invariance

Description:
    Defines the thermodynamic and geometric invariants that govern semantic
    stability across the Manifold 0.56 framework. The Durante Constant (κ_D)
    represents the universal phase-transition threshold below which semantic
    coherence degrades and entropic collapse begins.

    These values are IMMUTABLE. Modifying DURANTE_CONSTANT or FAIL_SAFE_CRITICAL
    constitutes a violation of the Invariance Law and invalidates any
    downstream certification produced by this engine.
"""

# ---------------------------------------------------------------------------
# Phase I — The Durante Constant (κ_D)
# The universal phase-transition threshold for semantic stability.
# Outputs scoring >= 0.56 are certified as invariant.
# ---------------------------------------------------------------------------
DURANTE_CONSTANT: float = 0.56

# ---------------------------------------------------------------------------
# Phase VI — Fail-Safe Boundaries
# Operational thresholds for the Governance & Certification protocol.
# ---------------------------------------------------------------------------
FAIL_SAFE_CRITICAL: float = 0.44   # Below this value, the manifold is considered collapsed.
STABILITY_WARNING: float  = 0.50   # Threshold for "Degraded" (Class B) certification.

# ---------------------------------------------------------------------------
# Phase I — Thermodynamic Variables
# Derived from the Durante Constant; govern entropy budget in semantic space.
# ---------------------------------------------------------------------------
ENTROPY_LIMIT: float = 1.0 - DURANTE_CONSTANT  # Max allowable semantic entropy (0.44)
BOLTZMANN_SEMANTIC_K: float = 1.38e-23          # Boltzmann analogue, normalized for semantic space.
                                                 # (Note: corrected spelling from BULTZMANN)

# ---------------------------------------------------------------------------
# Phase II — Geometric Scaling (Crystal Network)
# Parameters for Non-Euclidean lattice construction.
# ---------------------------------------------------------------------------
CRYSTAL_LATTICE_DENSITY: float = 0.56   # Node density per unit of non-Euclidean volume.

# ---------------------------------------------------------------------------
# Phase IV — Ricci Flow Parameters
# Controls the smoothing step for truth-density homogenisation.
# ---------------------------------------------------------------------------
RICCI_FLOW_STEP: float  = 0.01   # Metric tensor evolution step size (ε).
RICCI_FLOW_EPSILON: float = 0.01  # Alias retained for backward compatibility.
