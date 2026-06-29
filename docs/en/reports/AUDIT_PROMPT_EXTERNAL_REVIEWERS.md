# External Audit Prompt

Please review the attached R1 real local structural evaluation snapshot for SAS / kD=0.56 v1.0.7.

## Requested audit focus

1. Verify whether the claim boundary is technically appropriate.
2. Check whether the non-runtime structural evaluation is correctly separated from runtime artifacts.
3. Assess whether the Flow + CRE + Negation composite result is reported honestly.
4. Check whether the lexical baseline limitation is stated strongly enough.
5. Review whether NIG is correctly described as serialized but source-unaware / diagnostic-only.
6. Identify any reproducibility gaps before GitHub or Zenodo publication.

## Key reported result

Best non-runtime structural composite:

- Rule: Flow + CRE + Negation, score >= 1
- Test F1: 0.8717
- Precision: 0.9952
- Recall: 0.7755
- Accuracy: 0.8859

Baseline boundary:

- Lexical baseline test AUC: 0.9963
- Lexical baseline test F1: 0.9968

## Audit question

Is this package appropriately framed as a reproducible structural signal evaluation rather than a final detector superiority claim?
