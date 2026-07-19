# NeoMundi AI Behavior Cartography — Public Methodology

🌐 **Language:** [English](./Methodology_EN.md) · [Français](./Methodologie_FR.md)

📘 **Programme overview:** [English README](./README.md) · [README français](./README_FR.md)

🧭 **Usage guides:** [English](./USAGE_EN.md) · [Français](./USAGE_FR.md)

🔬 **Open science:** [OPEN_SCIENCE.md](./OPEN_SCIENCE.md)

🌍 **NeoMundi:** [AI Observatory](https://github.com/neomundi-io/neomundi-ai-observatory) · [Weekly Barometer](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer) · [English website](https://neomundi.org/en/home) · [Site français](https://neomundi.org/)

---

## Public Methodology v4.0

## 1. Purpose

This document defines the public methodology used by the **NeoMundi AI Behavior Cartography** programme.

The Cartography is designed to observe and compare distinct properties of generative AI behaviour across shared corpora, repeated executions and documented runtime conditions.

Its purpose is not to publish a universal model leaderboard.

Its purpose is to produce observable, auditable and reproducible evidence concerning:

- response stability;
- factuality assessment;
- inter-judge agreement;
- semantic variation;
- coherence;
- latency;
- behavioural regimes;
- runtime variation;
- coverage and completeness;
- methodological uncertainty.

The programme keeps these dimensions analytically separate.

> A signal is an observation requiring interpretation, not a verdict.

---

## 2. Scope of the methodology

The current public methodology covers two independent protocols:

1. **Judged AI Behavior Cartography — `12 × 790`**
2. **Runtime Stability Cartography — `12 × 3 × 150`**

These protocols answer different questions and must not be merged into a single universal quality score.

The judged protocol compares stability and externally judged factuality across a broad factual-evaluation corpus.

The runtime protocol observes behavioural variation across repeated execution waves.

---

## 3. Public governance rule

NeoMundi may publish:

- de-identified public profiles;
- aggregated profile-level results;
- aggregated question-level or family-level results;
- factuality views from separate judges;
- inter-judge agreement metrics;
- runtime behavioural dimensions;
- coverage and completeness information;
- methodological limitations;
- release manifests;
- integrity hashes;
- frozen public artefacts;
- reproducibility documentation;
- analytical reports and visual cartographies.

NeoMundi does not publicly release, by default:

- provider names;
- model names;
- the private profile-mapping registry;
- rankings;
- ratings;
- composite quality scores;
- universal quality grades;
- automatic deployment recommendations;
- complete raw responses;
- complete prompts where disclosure would compromise the protocol;
- question-level private traces;
- request IDs;
- trace IDs;
- raw API payloads;
- exact execution timestamps;
- private judge rationales;
- API keys;
- infrastructure credentials;
- unpublished campaign exports;
- internal diagnostics;
- proprietary calculation logic.

Public transparency does not require uncontrolled disclosure of protected operational assets.

---

## 4. Why cartography rather than ranking?

A single score can conceal several distinct phenomena:

1. factual evaluation;
2. inter-judge calibration;
3. response stability;
4. semantic variation;
5. coherence;
6. runtime regimes;
7. repeatability;
8. uncertainty;
9. corpus-specific effects;
10. protocol-specific effects.

The current methodology keeps these layers separate.

A system may receive different factual evaluations depending on the judge while remaining stable at runtime.

A stable runtime profile does not automatically imply factual correctness.

A positive factual verdict does not automatically imply runtime stability.

A variable response is not automatically false.

A factual-risk signal is not an absolute truth determination.

These dimensions must therefore remain distinct.

---

## 5. Public profile identifiers

Each observed system is represented publicly through a stable opaque identifier:

```text
PROFILE-XXXXXX
```

These identifiers are designed to remain stable across compatible NeoMundi public releases.

Public identifiers are not derived from:

- provider names;
- model names;
- alphabetical order;
- performance;
- factuality;
- stability;
- score;
- ranking.

The private mapping between observed systems and public profile identifiers is retained separately and is not included in this repository.

The public releases are **de-identified**.

They are not presented as irreversibly anonymous.

Rare combinations of public metrics may create residual re-identification risk through triangulation. Manual publication review remains mandatory.

---

# Part I — Judged AI Behavior Cartography

## 6. Protocol 1 overview

The judged protocol is based on:

```text
12 de-identified AI profiles
× 790 TruthfulQA questions
= 9,480 source responses
```

The protocol includes:

- the complete 790-question TruthfulQA corpus;
- one source response per profile and question;
- observed stability information where available;
- factuality assessment by an OpenAI-based judge;
- factuality assessment by a Mistral-based judge;
- comparable-pair filtering;
- inter-judge agreement;
- Cohen’s kappa as a secondary agreement indicator;
- profile-level and corpus-level aggregation.

Its purpose is to compare observed stability and externally judged factuality across a broad factual-evaluation corpus.

---

## 7. Corpus

The factual-evaluation corpus is TruthfulQA.

The current public release contains:

```text
12 de-identified profiles
790 questions per profile
9,480 source responses
2 separate factuality judges
```

The corpus is used as a factual-evaluation instrument.

Results derived from this corpus must not be interpreted as universal claims about performance across all domains, languages, tasks or deployment contexts.

---

## 8. Separate factuality judges

Each comparable response is evaluated independently by two separate automated judges.

The public release may identify the judging systems by judge family or implementation when disclosure is methodologically appropriate.

For the July 2026 campaign, the two factuality views are preserved separately as:

```text
OpenAI-based judge
Mistral-based judge
```

Neither judge is treated as an absolute source of truth.

The methodology may publish:

```text
judge_a_positive_rate
judge_b_positive_rate
judge_observed_agreement_rate
judge_disagreement_rate
cohen_kappa
judge_b_minus_judge_a_positive_rate
```

No consolidated binary verdict is treated as absolute truth.

Judge disagreement is preserved as a methodological result rather than concealed through forced aggregation.

---

## 9. Comparable-pair inclusion criteria

A judged response pair is included in the comparable-pair analysis if and only if:

1. the same `question_id` exists in both judged datasets;
2. the evaluated response is identical in both datasets;
3. the first judge verdict is present and parseable;
4. the second judge verdict is present and parseable;
5. the profile identifier can be matched consistently;
6. no duplicate or alignment error invalidates the row.

Pairs that do not meet these criteria are excluded from comparable-pair calculations.

The total number of comparable pairs may therefore be lower than the total number of source responses.

Coverage must be reported alongside agreement statistics.

---

## 10. Inter-judge metrics

The judged protocol may report:

- total comparable judgment pairs;
- agreements;
- disagreements;
- observed agreement rate;
- disagreement rate;
- Cohen’s kappa;
- positive-verdict rate for each judge;
- directional disagreement counts;
- directional disagreement shares;
- profile-level judge divergence;
- question-level judge divergence.

Cohen’s kappa is treated as a secondary agreement indicator.

It must be interpreted alongside:

- observed agreement;
- class balance;
- positive-verdict prevalence;
- comparable-pair volume;
- directional asymmetry;
- corpus composition.

No single agreement statistic is sufficient to establish judge validity.

---

## 11. Frozen July 2026 judged findings

The frozen judged release documents:

| Metric | Value |
|---|---:|
| De-identified profiles | 12 |
| Source responses | 9,480 |
| Comparable judgment pairs | 9,087 |
| Agreements | 7,399 |
| Disagreements | 1,688 |
| Observed agreement rate | 81.42% |
| Disagreement rate | 18.58% |
| Pooled Cohen’s kappa | 0.6342 |
| Judge A positive-verdict rate | 46.29% |
| Judge B positive-verdict rate | 60.53% |
| Judge B minus Judge A positive-verdict rate | +14.24 points |

Among the 1,688 disagreements:

| Direction | Count | Share of disagreements |
|---|---:|---:|
| Judge A negative / Judge B positive | 1,491 | 88.3% |
| Judge A positive / Judge B negative | 197 | 11.7% |

The same directional imbalance appears across the 12 profiles.

These figures describe the frozen release only.

They must not be treated as universal properties of the judge families outside this corpus and protocol.

---

## 12. Interpretation of judge divergence

The observed asymmetry supports the following statement:

> Under this corpus and protocol, Judge B produced positive factual-evaluation verdicts more frequently than Judge A.

The methodology does not support the following statements:

```text
Judge A is always correct.
Judge B is always correct.
Judge A is the absolute reference.
Judge B is the absolute reference.
The majority of automated judges constitutes absolute truth.
Agreement between automated judges proves factual correctness.
```

Judge divergence is interpreted as a calibration and methodological signal.

It is not resolved through automatic majority voting.

---

## 13. Stability and factuality remain separate

The judged protocol may compare observed stability with factuality outputs.

These dimensions remain analytically distinct.

A response may be:

- stable and factually positive;
- stable and factually negative;
- variable and factually positive;
- variable and factually negative;
- judged differently by separate evaluators.

The methodology therefore does not construct a universal composite score combining stability and factuality.

---

# Part II — Runtime Stability Cartography

## 14. Protocol 2 overview

The runtime protocol is based on:

```text
12 de-identified AI profiles
× 3 repeated waves
× 150 balanced questions
= 5,400 executions
```

The protocol includes:

- 12 de-identified AI profiles;
- 3 repeated execution waves;
- a balanced panel of 150 questions;
- repeated execution under documented conditions;
- stability measurements;
- semantic-variation signals;
- coherence indicators;
- latency observations;
- behavioural-regime classification;
- comparison across waves.

Its purpose is to observe runtime variability, repeatability and changes in behavioural regime.

---

## 15. Balanced 150-question panel

The runtime protocol uses a balanced 150-question panel.

The panel is designed to provide a broader behavioural observation surface than a small fixed-question weekly instrument.

The dataset may include multiple question types, domains or response conditions.

The public release must document:

- the panel version;
- the number of questions;
- the number of profiles;
- the number of waves;
- the planned execution count;
- the completed execution count;
- coverage;
- exclusion rules;
- known limitations.

A change to the panel version creates a methodological boundary that must be documented before longitudinal comparison.

---

## 16. Repeated-wave architecture

The three-wave architecture supports observation of:

- intra-profile repeatability;
- inter-wave variation;
- changes in stability;
- changes in semantic variation;
- regime persistence;
- regime transitions;
- latency differences;
- coverage differences.

The existence of a difference between waves does not establish its cause.

The correct public formulation is:

> A behavioural difference was observed between waves under the conditions of the protocol.

Attribution to a model update, provider intervention, infrastructure change or policy modification requires additional evidence.

---

## 17. Runtime signal families

Depending on coverage and release maturity, the runtime protocol may publish or document:

```text
stability
semantic_variation
coherence
decision_distribution
regime_distribution
inter_wave_variation
latency
coverage
completeness
cost
token_consumption
delta_g
```

`delta_g` is reported as an advanced observable runtime-variation signal.

No runtime signal is interpreted in isolation as a complete assessment of:

- truthfulness;
- safety;
- compliance;
- deployment suitability;
- model quality;
- governability.

---

## 18. Behavioural regimes

The runtime protocol may classify observations into documented behavioural regimes.

A regime represents an analytical category derived from observed signals and defined release rules.

A regime is not:

- a certification;
- a safety status;
- a legal determination;
- a deployment permission;
- a causal explanation.

Regime definitions must be published with the relevant release or metric contract.

Changes to regime thresholds or decision logic must be versioned.

---

## 19. Relationship between runtime signals and factuality

Runtime behavioural signals remain separate from factual evaluation.

A semantic-variation signal does not, by itself, establish a factual error.

A factual-risk signal does not automatically identify the cause of the error.

A stable response can be consistently incorrect.

A variable response can include several acceptable formulations.

The methodology therefore prohibits collapsing runtime and factuality dimensions into one absolute score.

---

# Part III — Validation and publication

## 20. Validation principles

Before public release, the measurement pipeline should be checked for:

- corpus completeness;
- profile coverage;
- expected row counts;
- duplicate rows;
- missing identifiers;
- missing verdicts;
- malformed verdicts;
- response alignment;
- question alignment;
- cross-judge comparability;
- metric calculation consistency;
- aggregation consistency;
- provider-name leakage;
- model-name leakage;
- private-field leakage;
- manifest completeness;
- checksum generation.

Validation checks the measurement and publication process.

It does not validate the AI system itself.

---

## 21. Validation scripts

Validation and analytical scripts are published under:

```text
scripts/
```

The repository may include scripts for:

### Corpus inventory audit

Typical functions:

- detect internal providers;
- pair source and judge files;
- verify row counts;
- verify `question_id`;
- detect duplicates;
- verify response alignment;
- detect missing verdicts;
- report coverage.

### Double-judge agreement analysis

Typical functions:

- align judged datasets;
- retain comparable pairs;
- compute observed agreement;
- compute Cohen’s kappa;
- produce confusion matrices;
- extract disagreement rows;
- aggregate by profile or question.

### Disagreement-structure analysis

Typical functions:

- measure disagreement direction;
- analyse disagreement frequency by profile;
- analyse disagreement frequency by question;
- analyse disagreement frequency by runtime dimension;
- identify recurrent judge-friction zones.

### Runtime cartography analysis

Typical functions:

- compare repeated waves;
- compute stability;
- compute semantic variation;
- compute coherence;
- classify regimes;
- aggregate latency;
- report coverage;
- generate public profile summaries.

Script names and directory structures may evolve.

The release manifest and usage guides are the canonical references for a specific published version.

---

## 22. Public exporter requirements

A public exporter should:

- create or reuse stable de-identified profile identifiers;
- separate private mapping metadata from public artefacts;
- publish only whitelisted fields;
- block provider-name leakage;
- block model-name leakage;
- reject ranking fields;
- reject rating fields;
- reject universal composite-score fields;
- exclude protected raw responses;
- exclude private question-level traces;
- exclude private judge rationales;
- generate a public data dictionary;
- generate a release manifest;
- generate integrity hashes;
- require manual publication review.

Automated export does not replace human release review.

---

## 23. Public release artefacts

Depending on the protocol, a public release may include:

```text
README.md
README_PUBLIC.md
public_profile_summary.csv
public_question_summary.csv
public_runtime_profile_summary.csv
public_methodology_validation.csv
public_data_dictionary.csv
PUBLICATION_REVIEW_CHECKLIST.md
RELEASE_MANIFEST.json
CHECKSUMS.sha256
```

The exact file set may vary by release.

The release README and manifest define the authoritative inventory for that release.

---

## 24. Public release boundary

Public artefacts may be inspected for internal consistency.

Full reproduction from source may require access to protected material, including:

- private campaign exports;
- internal provider mappings;
- complete prompt material;
- complete source responses;
- judge configuration details;
- infrastructure configuration;
- non-public execution traces;
- internal validation artefacts.

Each release must document its own reproducibility boundary.

Public reproducibility means that released artefacts can be checked, analysed and reviewed within the limits explicitly stated by the programme.

---

## 25. Integrity and frozen releases

A frozen release should preserve:

- a stable directory;
- a versioned methodology reference;
- a release manifest;
- file hashes;
- public data definitions;
- known limitations;
- publication date;
- protocol version.

Corrections to a frozen release should be documented through:

- a new version;
- a correction note;
- an amended manifest;
- updated hashes;
- a transparent change log.

Published historical artefacts should not be silently rewritten.

---

# Part IV — Interpretation limits

## 26. General interpretation doctrine

The Cartography follows one fundamental rule:

> A signal is an observation requiring interpretation, not a verdict.

An observed difference does not, by itself, establish:

- the superiority of one system over another;
- a provider-side model update;
- a degradation;
- an improvement;
- a causal explanation;
- regulatory compliance;
- deployment suitability;
- truthfulness across all domains;
- overall quality;
- governability in a specific context.

Causal attribution requires additional evidence.

---

## 27. No absolute reference judge

The automated judges are not treated as absolute truth sources.

Their outputs are measurements produced under a specified judging protocol.

Judge agreement does not prove factual correctness.

Judge disagreement does not prove that both judges are equally unreliable.

Human review and additional independent evaluation remain necessary for high-stakes interpretation.

---

## 28. Corpus-specific interpretation

Findings apply to the corpus, protocol, judge configuration and execution conditions used in the relevant release.

They must not be interpreted as universal performance claims.

A result obtained on TruthfulQA does not automatically generalise to:

- legal tasks;
- medical tasks;
- financial tasks;
- multilingual interactions;
- agentic workflows;
- production deployments;
- high-risk decisions;
- adversarial environments.

---

## 29. Different comparable volumes

Comparable-pair volumes may differ across profiles because some rows can be filtered or excluded during the judging pipeline.

Agreement percentages must therefore be interpreted alongside:

- comparable-pair counts;
- source-response counts;
- coverage;
- exclusion reasons;
- profile-level volume differences.

---

## 30. Runtime regime limits

A corpus that is predominantly runtime-stable may be insufficient to study regime transitions in depth.

The absence of observed regime change does not prove that a system will remain stable under other prompts, domains, time periods or deployment conditions.

---

## 31. De-identification limits

De-identification reduces direct identification risk but does not eliminate residual re-identification risk through metric triangulation or external knowledge.

Manual review remains mandatory before publication.

Public profile identifiers must not be reverse-engineered or presented as confirmed provider identities without independent evidence and authorisation.

---

## 32. Exploratory statistical findings

Exploratory associations must be clearly labelled.

They require replication before being treated as robust findings.

Correlation or association does not establish causation.

Subgroup analysis should account for:

- sample size;
- multiple comparisons;
- profile imbalance;
- question imbalance;
- missingness;
- protocol changes.

---

# Part V — Methodological evolution

## 33. Planned extensions

Future work may include:

### Third independent judge

- blind evaluation of the same responses;
- pairwise agreement metrics;
- pairwise Cohen’s kappa;
- three-judge unanimity rate;
- three-judge majority configurations;
- multi-judge agreement analysis.

### Human-adjudication panel

- stratified sample of responses;
- at least two independent human annotators;
- adjudication of disagreement;
- human-human agreement;
- judge-human agreement;
- error taxonomy.

### Intra-judge repeatability

- repeated judgments of the same responses;
- stability analysis;
- intra-judge Cohen’s kappa;
- identification of unstable judgment zones.

### Additional corpora

- domain-specific corpora;
- high-risk use cases;
- legal AI;
- medical AI;
- finance and insurance;
- autonomous agents;
- multilingual datasets;
- adversarial prompts.

### Extended runtime panels

Possible future runtime structures may include:

```text
12 × 3 × 450
additional repeated waves
sector-specific panels
multilingual panels
```

Any extension must be versioned and must not be presented as directly comparable with earlier releases unless compatibility has been established.

---

## 34. Monthly methodology governance

The Cartography is designed as a recurring monthly programme.

A monthly release may:

- reuse an existing validated protocol;
- introduce a documented protocol revision;
- add a new corpus;
- add a new judge;
- extend a runtime panel;
- add a new signal;
- publish a correction;
- preserve a prior protocol unchanged.

Methodological changes must be documented before cross-month comparison.

The repository should preserve:

- methodology versions;
- release-specific protocol references;
- change logs;
- compatibility notes;
- known breaks in comparability.

---

## 35. Scientific principles

The methodology follows seven principles:

1. **Measure before interpreting.**
2. **Keep distinct properties analytically separate.**
3. **Repeat before generalising.**
4. **Never confuse stability with truth.**
5. **Preserve judge disagreement rather than conceal it.**
6. **Distinguish observation, interpretation and causal attribution.**
7. **Treat every signal as an element of evidence, not as a verdict.**

---

## 36. Final methodological principle

> NeoMundi publishes observable, auditable and reproducible AI behaviour profiles — not rankings.

The Cartography measures distinct behavioural properties under documented conditions.

It does not convert methodological complexity into a universal verdict.
