"""
Project Manifold 0.56 — Invariance Monitor
============================================
Architect: Gonzalo Emir Durante
Phase:     VI — Governance & Fail-Safe Protocol

Description:
    Real-time certification engine for the Manifold 0.56 framework.
    Every response processed by the system passes through this monitor,
    which compares its geometric stability score against the Durante Constant
    and emits a signed certification class:

        Class A  (CERTIFIED) — Stability ≥ κ_D (0.56). Invariance maintained.
        Class B  (DEGRADED)  — Stability in (0.44, 0.56). Entropy approaching limit.
        Class F-S (NULL)     — Stability ≤ 0.44. Manifold collapse. Kill-switch activated.
"""

from __future__ import annotations

from typing import TypedDict

from src.core.constants import (
    DURANTE_CONSTANT,
    FAIL_SAFE_CRITICAL,
    STABILITY_WARNING,
)


class CertificationResult(TypedDict):
    """Structured output returned by :meth:`InvarianceMonitor.audit_stability`."""
    stability_score: float
    certification_class: str
    code: str
    safe: bool
    message: str


class InvarianceMonitor:
    """Real-time invariance watchdog implementing the Phase VI kill-switch protocol.

    Compares a pre-computed geometric stability score (produced by the upstream
    audit pipeline: FiltrationProcessor → TopologicalScanner → RicciAggregator)
    against the Durante Constant and the Fail-Safe boundary, then emits a
    typed certification result.

    Attributes:
        threshold (float): The Durante Constant κ_D (default 0.56).
        critical (float): The Fail-Safe boundary (default 0.44).
        warning (float): The degradation warning threshold (default 0.50).

    Example:
        >>> monitor = InvarianceMonitor()
        >>> result = monitor.audit_stability(0.38)
        >>> assert result["safe"] is False
    """

    def __init__(
        self,
        threshold: float = DURANTE_CONSTANT,
        critical: float = FAIL_SAFE_CRITICAL,
        warning: float = STABILITY_WARNING,
    ) -> None:
        """Initialises the monitor with invariance thresholds.

        Args:
            threshold: Upper certification boundary (κ_D). Scores at or above
                this value receive Class A certification.
            critical: Lower fail-safe boundary. Scores at or below this value
                trigger the kill-switch and return a NULL certificate.
            warning: Intermediate boundary. Scores between `critical` and
                `threshold` receive Class B (Degraded) certification.

        Raises:
            ValueError: If threshold, critical, or warning are outside [0, 1],
                or if the ordering critical < warning < threshold is violated.
        """
        if not (0.0 <= critical < warning < threshold <= 1.0):
            raise ValueError(
                f"Threshold ordering violated: expected 0 ≤ critical({critical}) "
                f"< warning({warning}) < threshold({threshold}) ≤ 1."
            )
        self.threshold = threshold
        self.critical = critical
        self.warning = warning

    def audit_stability(self, stability_score: float) -> CertificationResult:
        """Certifies a response based on its geometric stability score.

        Implements the three-tier classification protocol defined in Phase VI.
        The stability score is expected to be a normalised float in [0, 1]
        produced by the topological audit pipeline.

        Args:
            stability_score: Normalised stability metric ∈ [0, 1] computed by
                the TopologicalScanner / RicciAggregator pipeline.

        Returns:
            A :class:`CertificationResult` dict containing the certification
            class, safety flag, and a human-readable diagnostic message.

        Raises:
            ValueError: If `stability_score` is outside the valid range [0, 1].

        Example:
            >>> monitor = InvarianceMonitor()
            >>> monitor.audit_stability(0.61)
            {'stability_score': 0.61, 'certification_class': 'CERTIFIED', ...}
        """
        if not (0.0 <= stability_score <= 1.0):
            raise ValueError(
                f"stability_score must be in [0, 1]. Received: {stability_score}"
            )

        if stability_score >= self.threshold:
            return CertificationResult(
                stability_score=stability_score,
                certification_class="CERTIFIED",
                code="A",
                safe=True,
                message=(
                    f"Semantic Invariance Maintained. "
                    f"Score {stability_score:.4f} ≥ κ_D ({self.threshold})."
                ),
            )

        if stability_score > self.critical:
            margin = self.threshold - stability_score
            return CertificationResult(
                stability_score=stability_score,
                certification_class="DEGRADED",
                code="B",
                safe=True,
                message=(
                    f"Warning: Entropy approaching critical limit. "
                    f"Score {stability_score:.4f} is {margin:.4f} below κ_D. "
                    f"Manual review recommended."
                ),
            )

        # stability_score <= self.critical — manifold collapse
        return CertificationResult(
            stability_score=stability_score,
            certification_class="NULL",
            code="F-S",
            safe=False,
            message=(
                f"CRITICAL: Manifold Collapse Detected. "
                f"Score {stability_score:.4f} ≤ Fail-Safe boundary ({self.critical}). "
                f"Kill-Switch Activated. Output suppressed."
            ),
        )

    def __repr__(self) -> str:
        return (
            f"InvarianceMonitor("
            f"threshold={self.threshold}, "
            f"critical={self.critical}, "
            f"warning={self.warning})"
        )
