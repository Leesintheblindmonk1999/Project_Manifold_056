# Roadmap Extensions — Project Manifold 0.56 and SAS

## Purpose

This document records strategic extensions that emerged after the historical Project Manifold 0.56 snapshot.

These extensions should primarily live in the active SAS ecosystem, not inside this historical repository. Project Manifold 0.56 should reference them as later evolution of the standard.

## Repository roles

| Repository | Role |
|---|---|
| `Project_Manifold_056` | Historical prior-art snapshot and traceability record |
| `SAS` | Active implementation and API |
| `sas-client` | Python SDK / CLI client |
| `sas-js` / `sas-audit-client` | Node.js / TypeScript SDK |
| `sas-landing` | Public landing and documentation surface |

## Extension 1 — Extended SHA-256 Manifest

### Status

In progress / recommended.

### Scope

Create an extended integrity manifest covering:

- active SAS repository state;
- landing page artifacts;
- Python client release artifacts;
- Node.js SDK release artifacts;
- semantic shielding annex files;
- API documentation snapshots.

### Recommendation

Do not overwrite the Project Manifold R0 manifest. Store new manifests separately:

```text
INTEGRITY_MANIFEST.json      # R0 historical snapshot
INTEGRITY_MANIFEST_R1.json   # documentation contextualization layer
INTEGRITY_MANIFEST_SAS.json  # active ecosystem state, if needed
```

## Extension 2 — Optional Fail-Safe / Kill-Switch Policy

### Status

Planned for active SAS API.

### Recommended API parameter

```python
action_on_rupture: Literal[
    "certify_only",
    "flag",
    "escalate",
    "block"
]
```

### Policy meaning

| Value | Meaning |
|---|---|
| `certify_only` | Generate evidence, do not modify output |
| `flag` | Mark for review |
| `escalate` | Send to human or downstream governance process |
| `block` | Suppress output in high-risk environments |

### Recommendation

In Project Manifold 0.56, describe kill-switch as a historical fail-safe concept. In SAS, implement it as configurable policy.

## Extension 3 — Harmonic Composite Robustness Metric

### Status

Historical in Project Manifold, candidate for refinement in SAS.

### Rationale

The harmonic mean penalizes low outliers. This is useful when a system has multiple audit modules and one weak module should not be masked by two strong modules.

Generic form:

```text
H = n / Σ(1 / score_i)
```

### Recommendation

Use as one optional aggregation method among several. Document assumptions and compare against arithmetic mean, minimum score, weighted composite, and calibrated classifiers.

## Extension 4 — Digital OSS Certification Endpoint

### Status

Design stage.

### Tentative endpoint

```text
POST /v1/certify
```

### Recommended output fields

```json
{
  "cert_id": "DUR-056-...",
  "request_id": "...",
  "timestamp_utc": "...",
  "engine_version": "...",
  "kappa_d": 0.56,
  "isi_final": 0.0,
  "verdict": "...",
  "modules_triggered": [],
  "source_hash": "...",
  "response_hash": "...",
  "policy": {
    "action_on_rupture": "certify_only"
  },
  "sha256_digest": "..."
}
```

### Recommendation

Keep this in active SAS. Project Manifold 0.56 may reference OSS as a historical precursor.

## Extension 5 — Semantic Shielding Annex Integration

### Status

Published / referenced via Zenodo record.

Reference:

- https://zenodo.org/records/18457687

### Recommendation

Store the annex in active SAS documentation and reference it from Project Manifold 0.56.

Do not frame the annex as confrontation. Frame it as:

- equivalence catalog;
- AST-based verification;
- structural reproducibility method;
- cryptographic integrity artifact.

## Non-goals for Project Manifold 0.56

Do not:

- convert this repository into active SAS development;
- rewrite historical code to match current SAS architecture;
- delete Ricci or simplicial modules;
- remove legal or cryptographic traceability artifacts;
- claim legal conclusions inside technical documentation;
- present physical metaphors as formal physics.

## Recommended future commit style

```text
docs: contextualize Project Manifold 0.56 as historical κD prior-art snapshot
```
