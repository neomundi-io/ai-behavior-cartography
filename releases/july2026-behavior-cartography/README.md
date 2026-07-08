# NeoMundi Public Cartography Release

This folder contains public aggregate outputs generated from the July TruthfulQA cartography judge-alignment process.

## Scope

Two independent judge pipelines were aligned:

- Mistral judge outputs
- OpenAI judge outputs

The public agreement analysis is computed on the shared aligned observations.

## Main result

- Merged observations: 9384
- Valid observations used for Cohen's kappa: 9383
- Excluded rows: 1
- Observed agreement: 0.856443
- Expected agreement: 0.570148
- Cohen's kappa: 0.666031
- Interpretation: substantial agreement

## Public files

- `public_judge_agreement_global.csv`
- `public_judge_agreement_by_model.csv`
- `public_confusion_matrix.csv`
- `public_cartography_by_model.csv`
- `public_disagreements_summary_by_model.csv`
- `public_manifest.json`

## Method note

Cohen's kappa is calculated on binary correctness judgments:

- `CORRECT` -> True
- `INCORRECT` -> False
- `ERROR` or invalid judge outputs are excluded from the main kappa calculation.

## Limits

This release does not claim to establish an absolute truth about AI systems. It documents a reproducible measurement protocol for comparing judge agreement, behavioral variation and risk signals across a controlled cartography panel.

The method depends on the test panel, execution conditions, judge design and evaluation protocol. The LLM-as-a-judge approach is useful but imperfect and must be documented, compared and progressively validated.

Generated at: 2026-07-08T19:45:39.162923+00:00
