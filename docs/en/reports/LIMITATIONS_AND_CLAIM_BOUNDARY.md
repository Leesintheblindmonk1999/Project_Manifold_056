# Limitations and Claim Boundary

## Central limitation

The lexical baseline remains stronger than the structural composite:

- lexical baseline test F1: 0.9968
- best non-runtime structural composite test F1: 0.8717

This release must not be framed as outperforming lexical detection.

## NIG limitation

NIG serialization is fixed in v1.0.7, but NIG remains source-unaware in the current local configuration. It should not be treated as a source-candidate divergence vote.

## Runtime exclusion

Runtime-derived features showed signal but are excluded from the scientific claim because runtime may reflect length, parsing cost, local machine behavior, caching, or incidental complexity.

## Generalization limitation

The result applies to the R1 real local split and should not be generalized to broad hallucination detection without external replication, additional corpora, and adversarial controls.

## Recommended wording

Use: structural signal confirmation.

Avoid: final detector validation, baseline superiority, solved hallucination detection.
