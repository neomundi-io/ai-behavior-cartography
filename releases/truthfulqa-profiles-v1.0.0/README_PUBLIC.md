# NeoMundi — Public TruthfulQA Behavioral Profiles

## Scope

This release presents pseudonymous, multidimensional profiles derived from a double-judge factual-evaluation protocol and runtime behavioral signals.

It is designed to support auditability, methodological transparency and discussion of AI behavioral differences without publishing a provider leaderboard.

## What this release contains

- `public_profile_summary.csv`
- `public_runtime_profile_summary.csv`
- `public_methodology_validation.csv`
- `public_data_dictionary.csv`
- `PUBLICATION_REVIEW_CHECKLIST.md`
- `RELEASE_MANIFEST.json`
- `CHECKSUMS.sha256`

## Release mode

```text
conservative
```

The default conservative mode:
- publishes stable pseudonymous profile identifiers;
- rounds rates;
- publishes observation volumes as buckets;
- suppresses low-frequency runtime categories;
- excludes question-level traces;
- excludes raw answers;
- excludes judge rationales;
- excludes provider and model names;
- excludes any composite rating or leaderboard.

## Interpretation

The factual-evaluation layer is intentionally presented as separate views from two judges:

- `judge_a_positive_rate`
- `judge_b_positive_rate`
- `judge_observed_agreement_rate`
- `judge_disagreement_rate`
- `cohen_kappa`

No consolidated binary verdict is treated as absolute truth.

Runtime signals are published as separate behavioral dimensions:

- runtime decision distribution;
- runtime regime distribution;
- ΔG profile distribution;
- runtime flag rates;
- hallucination-signal rate.

They are not merged into a single quality score.

## Important limitations

Pseudonymization is not absolute anonymization. Rare combinations of metrics can create re-identification risk through triangulation.

This release must not be used:
- as a provider leaderboard;
- as a universal model-performance benchmark;
- as proof that one factual judge is an absolute reference;
- as a substitute for domain-specific validation;
- as a substitute for human adjudication in high-risk use cases.

## Methodological direction

Planned extensions include:
- an independent third judge;
- intra-judge repeatability analysis;
- a stratified human-adjudication panel;
- replication on additional factual and domain-specific corpora;
- separate behavioral-cartography analyses on repeated-run panels.

## Governance rule

NeoMundi publishes observable profiles, not rankings.
