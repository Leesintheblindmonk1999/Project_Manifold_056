# Release Checklist

## Local freeze

- [x] Freeze ID assigned: `R1_REAL_LOCAL_V107_STRUCTURAL_EVAL_PASS`
- [x] 18 files copied to freeze
- [x] missing: 0
- [x] Integrity manifest generated
- [x] Integrity manifest SHA-256 recorded: `eb2899292ae72384f9eff8e8fab8e57f09b00ea0962ee822a40fbcdac2574b4c`

## Technical checks

- [x] Dataset rows: 4698
- [x] Validation rows: 938
- [x] Test rows: 3760
- [x] Full runner v1.0.7 completed: 4698 / 4698
- [x] NIG conversion errors: 0 / 4698
- [x] Non-runtime calibrated evaluation completed
- [x] Composite ablation completed

## Before GitHub

- [ ] Review generated docs.
- [ ] Run `scripts/collect_release_artifacts.ps1` locally.
- [ ] Inspect the generated `release_upload` ZIP.
- [ ] Confirm no private secrets or credentials.
- [ ] Confirm dataset licensing / release safety.

## Before Zenodo

- [ ] Upload GitHub release or stable repository snapshot.
- [ ] Upload paper PDF and Markdown.
- [ ] Upload documentation package.
- [ ] Upload real local artifact ZIP if allowed.
- [ ] Use cautious claim boundary.
