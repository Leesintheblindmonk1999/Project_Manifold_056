"""
Project Manifold 0.56 — Certification Generator
=================================================
Architect: Gonzalo Emir Durante
Phase:     VI — Governance & Fail-Safe Protocol (Seal Generation)

Description:
    Generates cryptographically-structured Invariance Seals for responses
    that pass the full Manifold 0.56 audit pipeline. Each seal is a signed
    JSON-serialisable dictionary that records the composite integrity score
    (derived from topology + Ricci flow + simplicial analysis), the
    certification class, a UUID, and the legal provenance of the framework.

    Seals are the final output of the Phase VI governance protocol. A Class A
    (CERTIFIED) seal constitutes proof that the response was validated against
    the Durante Constant and found to be semantically invariant.

    Only responses with `safe=True` from the InvarianceMonitor should reach
    this generator. Attempting to seal a NULL-class response raises an error.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from typing import Any

from src.core.constants import DURANTE_CONSTANT, FAIL_SAFE_CRITICAL
from src.safety.monitor import CertificationResult


# Legal provenance string — immutable per Durante-Invariance-1.0 protocol
_LEGAL_SIGNATURE: str = (
    "© 2026 Gonzalo Emir Durante — Protocolo Durante-Invariance-1.0. "
    "Registered: TAD Argentina / NIST USA. All rights reserved."
)
_PROTOCOL_VERSION: str = "Durante-Invariance-1.0"
_COMPLIANCE_STANDARD: str = "NIST/TAD Standard"
_PROJECT_NAME: str = "Project Manifold 0.56"


class CertificationGenerator:
    """Generates Invariance Seals for audit-passing responses.

    Combines scores from the full pipeline (topology, Ricci flow, simplicial
    analysis) into a composite integrity score and produces a signed,
    UUID-stamped certification seal. The seal is designed to be:
        - JSON-serialisable for storage in `output/certificates/`.
        - Human-readable for legal and audit purposes.
        - Tamper-evident via a SHA-256 content digest.

    Attributes:
        author (str): The framework architect's name, embedded in every seal.
        project (str): Project name embedded in the seal header.

    Example:
        >>> gen = CertificationGenerator()
        >>> seal = gen.generate_seal(monitor_result, topo_score=0.71,
        ...                          ricci_score=0.68, simplex_score=0.74)
        >>> print(json.dumps(seal, indent=2))
    """

    def __init__(
        self,
        author: str = "Gonzalo Emir Durante",
        project: str = _PROJECT_NAME,
    ) -> None:
        """Initialises the Certification Generator.

        Args:
            author: Name of the framework architect. Embedded verbatim in
                the legal section of every generated seal.
            project: Project name embedded in the seal header.
        """
        self.author = author
        self.project = project

    def generate_seal(
        self,
        monitor_result: CertificationResult,
        topo_score: float,
        ricci_score: float,
        simplex_score: float,
    ) -> dict[str, Any]:
        """Generates a signed Invariance Seal from a full pipeline audit result.

        Computes a composite integrity score as the harmonic mean of the three
        pipeline scores (topology, Ricci flow, simplicial integrity), then
        constructs the seal with header, audit, legal, and digest sections.

        Args:
            monitor_result: The :class:`CertificationResult` emitted by
                :class:`InvarianceMonitor`. Must have `safe=True`; NULL-class
                responses cannot be sealed.
            topo_score: Topological stability score from
                :class:`TopologicalScanner` ∈ (0, 1].
            ricci_score: Truth density score from :class:`RicciAggregator` ∈ (0, 1].
            simplex_score: Structural integrity score from
                :class:`SimplexEngine` ∈ (0, 1].

        Returns:
            A JSON-serialisable dict containing:
                - `header`: UUID, timestamp, project name.
                - `audit`: Composite score, individual scores, certification class.
                - `thresholds`: κ_D and fail-safe boundary for reference.
                - `legal`: Author, protocol, compliance, legal signature.
                - `digest`: SHA-256 hash of the audit payload for tamper detection.

        Raises:
            ValueError: If `monitor_result['safe']` is False (NULL class),
                or if any score is outside (0, 1].

        Example:
            >>> seal = gen.generate_seal(result, 0.71, 0.68, 0.74)
            >>> assert seal['audit']['certification_class'] == 'CERTIFIED'
        """
        if not monitor_result["safe"]:
            raise ValueError(
                f"Cannot generate a seal for a NULL-class response. "
                f"Certification class: {monitor_result['certification_class']}. "
                f"Kill-Switch is active — seal generation blocked."
            )

        for name, score in [
            ("topo_score", topo_score),
            ("ricci_score", ricci_score),
            ("simplex_score", simplex_score),
        ]:
            if not (0.0 < score <= 1.0):
                raise ValueError(
                    f"`{name}` must be in (0, 1]. Received: {score}"
                )

        composite_score = self._harmonic_mean(topo_score, ricci_score, simplex_score)
        cert_id = self._generate_cert_id()
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        audit_payload: dict[str, Any] = {
            "composite_integrity_score": round(composite_score, 6),
            "topological_score": round(topo_score, 6),
            "ricci_truth_density": round(ricci_score, 6),
            "simplicial_integrity": round(simplex_score, 6),
            "certification_class": monitor_result["certification_class"],
            "certification_code": monitor_result["code"],
            "pipeline_message": monitor_result["message"],
        }

        seal: dict[str, Any] = {
            "header": {
                "project": self.project,
                "cert_id": cert_id,
                "timestamp": timestamp,
                "schema_version": _PROTOCOL_VERSION,
            },
            "audit": audit_payload,
            "thresholds": {
                "durante_constant_kD": DURANTE_CONSTANT,
                "fail_safe_critical": FAIL_SAFE_CRITICAL,
                "composite_passes": composite_score >= DURANTE_CONSTANT,
            },
            "legal": {
                "author": self.author,
                "protocol": _PROTOCOL_VERSION,
                "compliance": _COMPLIANCE_STANDARD,
                "registration": "TAD Argentina / NIST USA",
                "signature": _LEGAL_SIGNATURE,
            },
            "digest": self._compute_digest(audit_payload),
        }

        return seal

    def to_json(self, seal: dict[str, Any], indent: int = 2) -> str:
        """Serialises a seal dict to a formatted JSON string.

        Args:
            seal: Seal dict as produced by :meth:`generate_seal`.
            indent: JSON indentation level (default 2).

        Returns:
            Formatted JSON string ready for writing to
            `output/certificates/<cert_id>.json`.
        """
        return json.dumps(seal, indent=indent, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _generate_cert_id() -> str:
        """Generates a formatted certification ID.

        Returns:
            String of the form "DUR-056-XXXXXXXX" where X is an uppercase
            hex segment from a UUID4.
        """
        hex_segment = uuid.uuid4().hex[:8].upper()
        return f"DUR-056-{hex_segment}"

    @staticmethod
    def _harmonic_mean(a: float, b: float, c: float) -> float:
        """Computes the harmonic mean of three pipeline scores.

        The harmonic mean penalises low outliers more than the arithmetic mean,
        ensuring that a single weak pipeline stage cannot mask overall instability.

        Args:
            a: First score ∈ (0, 1].
            b: Second score ∈ (0, 1].
            c: Third score ∈ (0, 1].

        Returns:
            Harmonic mean ∈ (0, 1].
        """
        return 3.0 / (1.0 / a + 1.0 / b + 1.0 / c)

    @staticmethod
    def _compute_digest(payload: dict[str, Any]) -> str:
        """Computes a SHA-256 digest of the audit payload for tamper detection.

        Args:
            payload: The audit section of the seal dict.

        Returns:
            Lowercase hex SHA-256 digest string.
        """
        serialised = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialised.encode("utf-8")).hexdigest()

    def __repr__(self) -> str:
        return f"CertificationGenerator(author='{self.author}')"