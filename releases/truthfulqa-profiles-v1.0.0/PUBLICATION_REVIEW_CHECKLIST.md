# Publication review checklist

This checklist must be reviewed manually before publication.

## Identity leakage

- [ ] No provider name is present in any public file.
- [ ] No model name is present in any public file.
- [ ] No private mapping file is present in the public directory.
- [ ] No source path is present in the public manifest.
- [ ] No raw response is present in the public directory.
- [ ] No question-level trace is present in the public directory.
- [ ] No judge rationale is present in the public directory.

## Ranking leakage

- [ ] No rank column is present.
- [ ] No rating column is present.
- [ ] No grade column is present.
- [ ] No composite score is present.
- [ ] No best / worst wording is present.
- [ ] No leaderboard wording is present.

## Re-identification review

- [ ] Profile-level rates have been reviewed for triangulation risk.
- [ ] Rare runtime categories have been suppressed or grouped.
- [ ] Observation volumes are bucketed unless a detailed release was explicitly approved.
- [ ] The public release has been compared against earlier public artifacts for accidental re-identification clues.

## Methodology

- [ ] The README states that pseudonymization is not anonymization.
- [ ] The README states that the judges are presented separately.
- [ ] The README states that runtime signals are not merged into a composite score.
- [ ] The README states that the release is not a universal benchmark.
- [ ] Checksums have been generated.
