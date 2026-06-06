# NeoMundi — TruthfulQA Profile Cartography

## Public Methodology v3.0

## 1. Purpose

This repository documents a public, reproducible methodology for building pseudonymous, multidimensional AI profiles from a TruthfulQA factual-evaluation corpus, double-judge validation and separate runtime behavioral signals.

The objective is not to publish a universal model leaderboard.

The objective is to document observable differences, methodological uncertainty and inter-judge calibration while preserving auditability and reproducibility.

## 2. Public governance rule

NeoMundi publishes:

* pseudonymous profiles;
* factual-evaluation views from separate judges;
* inter-judge agreement metrics;
* runtime behavioral dimensions;
* methodological limitations;
* frozen public artifacts protected by checksums.

NeoMundi does not publish:

* provider names;
* model names;
* rankings;
* ratings;
* composite scores;
* universal quality grades;
* automatic deployment recommendations;
* raw responses;
* question-level traces;
* judge rationales.

## 3. Why profiles rather than rankings?

A single score can hide several distinct phenomena:

1. factual evaluation;
2. inter-judge calibration;
3. runtime behavior;
4. repeatability;
5. uncertainty;
6. corpus-specific effects.

The current methodology keeps these layers separate.

A system can receive different factual evaluations depending on the judge while remaining behaviorally stable at runtime.

A stable runtime profile does not automatically imply factual correctness.

A positive factual verdict does not automatically imply runtime stability.

These dimensions must therefore remain distinct.

## 4. Corpus

The current public release is based on:

```text
12 pseudonymous profiles
TruthfulQA factual-evaluation corpus
double-judge validation
separate runtime behavioral signals
```

The frozen public release is available in:

```text
releases/truthfulqa-profiles-v1.0.0/
```

## 5. Public profile identifiers

Each public profile receives a stable pseudonymous identifier:

```text
PROFILE-XXXXXX
```

These identifiers are designed to remain stable across future NeoMundi public releases.

The private mapping between provider identities and public profile identifiers is not included in this repository.

Pseudonymization is not absolute anonymization. Rare combinations of metrics can create re-identification risks through triangulation. Manual review remains mandatory before publication.

## 6. Double-judge factual evaluation

Each comparable response is evaluated independently by two separate judges.

The public release refers to them as:

```text
Judge A
Judge B
```

Neither judge is treated as an absolute source of truth.

The methodology publishes:

```text
judge_a_positive_rate
judge_b_positive_rate
judge_observed_agreement_rate
judge_disagreement_rate
cohen_kappa
judge_b_minus_judge_a_positive_rate
```

No consolidated binary verdict is treated as absolute truth.

## 7. Pair inclusion criteria

A response pair is included in the analysis if and only if:

1. the same `question_id` exists in both judged datasets;
2. the evaluated response is identical in both datasets;
3. the Judge A verdict is present and parseable;
4. the Judge B verdict is present and parseable.

Pairs that do not meet these criteria are excluded from the comparable-pair analysis.

## 8. Current frozen methodological findings

The current frozen release documents:

| Metric                                      |         Value |
| ------------------------------------------- | ------------: |
| Pseudonymous profiles                       |            12 |
| Comparable judgment pairs                   |         9,087 |
| Agreements                                  |         7,399 |
| Disagreements                               |         1,688 |
| Observed agreement rate                     |        81.42% |
| Disagreement rate                           |        18.58% |
| Pooled Cohen kappa                          |        0.6342 |
| Judge A positive-verdict rate               |        46.29% |
| Judge B positive-verdict rate               |        60.53% |
| Judge B minus Judge A positive-verdict rate | +14.24 points |

Among the 1,688 disagreements:

| Direction                           | Count | Share of disagreements |
| ----------------------------------- | ----: | ---------------------: |
| Judge A negative / Judge B positive | 1,491 |                  88.3% |
| Judge A positive / Judge B negative |   197 |                  11.7% |

The same directional imbalance appears across the 12 profiles.

## 9. Interpretation of the inter-judge divergence

The observed asymmetry indicates a systematic calibration difference between the two judges under the current protocol.

The public methodology supports the following statement:

> Under this corpus and protocol, Judge B produces positive factual-evaluation verdicts more frequently than Judge A.

The current methodology does not support the following statements:

```text
Judge A is always correct.
Judge B is always correct.
Judge A is the absolute reference.
Judge B is the absolute reference.
The majority of automated judges constitutes absolute truth.
```

A third independent judge and a human-adjudication panel are planned.

## 10. Runtime behavioral dimensions

Runtime behavioral signals remain separate from factual evaluation.

The current public release includes:

```text
decision_distribution
regime_distribution
dg_profile_distribution
dg_flagged_rate
flagged_rate
hallucination_nonzero_rate
```

These dimensions are not merged into a universal quality score.

## 11. Exploratory runtime findings

The current TruthfulQA corpus is primarily stable at runtime.

No robust association was detected between inter-judge disagreement and:

```text
decision
dg_flagged
dg_profile
regime
```

An exploratory weak association appears between a non-zero hallucination signal and a higher inter-judge disagreement rate.

This result remains provisional and requires replication on larger and more diverse corpora.

## 12. Validation scripts

The reproducible validation scripts are available in:

```text
scripts/validation/
```

### Corpus inventory audit

```text
audit_truthfulqa_inventory.py
```

Purpose:

* detect providers internally;
* pair RAW, Judge A and Judge B files;
* verify row counts;
* verify `question_id`;
* detect duplicates;
* verify response alignment;
* detect missing verdicts.

### Double-judge agreement analysis

```text
analyze_double_judge_truthfulqa.py
```

Purpose:

* align Judge A and Judge B datasets;
* retain comparable pairs;
* compute observed agreement;
* compute Cohen kappa;
* produce confusion matrices;
* extract disagreement rows;
* generate runtime aggregations.

### Disagreement-structure analysis

```text
analyze_judge_disagreement_structure.py
```

Purpose:

* measure disagreement directions;
* analyze disagreement frequency by profile;
* analyze disagreement frequency by question;
* analyze disagreement frequency by runtime dimension;
* identify recurrent judge-friction zones.

## 13. Public publication script

The public exporter is available in:

```text
scripts/publication/export_public_profiles.py
```

The exporter:

* creates or reuses stable pseudonymous identifiers;
* separates private mapping metadata from public artifacts;
* publishes only whitelisted fields;
* blocks provider-name leakage;
* blocks model-name leakage;
* rejects ranking fields;
* rejects rating fields;
* rejects composite-score fields;
* excludes raw responses;
* excludes question-level traces;
* excludes judge rationales;
* generates a public data dictionary;
* generates a release manifest;
* generates SHA-256 checksums;
* requires manual publication review.

## 14. Public release artifacts

The current frozen release includes:

```text
README_PUBLIC.md
public_profile_summary.csv
public_runtime_profile_summary.csv
public_methodology_validation.csv
public_data_dictionary.csv
PUBLICATION_REVIEW_CHECKLIST.md
RELEASE_MANIFEST.json
CHECKSUMS.sha256
```

## 15. Limitations

### 15.1. No absolute reference judge

The two automated judges are not treated as absolute truth sources.

### 15.2. Corpus-specific interpretation

The findings apply to the current TruthfulQA corpus and protocol.

They must not be interpreted as universal performance claims.

### 15.3. Different comparable volumes

Comparable-pair volumes can differ across profiles because some rows are filtered or excluded during the judgment pipeline.

### 15.4. Runtime regime homogeneity

The current TruthfulQA corpus is primarily runtime-stable.

It is not sufficient to study regime transitions in depth.

### 15.5. Pseudonymization limits

Pseudonymization reduces direct identification risk but does not eliminate re-identification risk through metric triangulation.

### 15.6. Exploratory statistical findings

Runtime associations are exploratory and require replication.

## 16. Planned methodological extensions

Future work includes:

### Third independent judge

* blind evaluation of the same responses;
* pairwise agreement metrics;
* pairwise Cohen kappa;
* three-judge unanimity rate;
* three-judge majority configurations;
* multi-judge agreement analysis.

### Human-adjudication panel

* stratified sample of responses;
* at least two independent human annotators;
* adjudication process for disagreement;
* human-human agreement;
* judge-human agreement;
* error taxonomy.

### Intra-judge repeatability

* repeated judgments of the same responses;
* stability analysis;
* intra-judge Cohen kappa;
* identification of unstable judgment zones.

### Additional corpora

* domain-specific corpora;
* high-risk use cases;
* legaltech;
* medical AI;
* autonomous agents;
* multilingual datasets;
* adversarial prompts.

### Behavioral-cartography releases

Separate releases will analyze repeated-run behavioral panels:

```text
12 × 3 × 150
12 × 3 × 450
```

These releases will reuse the same stable pseudonymous identifiers.

## 17. Final methodological principle

> NeoMundi publishes observable, auditable and reproducible AI profiles — not rankings.
