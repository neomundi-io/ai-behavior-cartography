# July 2026 Judged AI Behavior Cartography — `12 × 790`

🌐 **Documentation:** [July 2026 release index](../README.md) · [Programme overview](../../../README.md) · [Public methodology](../../../Methodology_EN.md) · [Méthodologie publique](../../../Methodologie_FR.md)

🌍 **NeoMundi:** [AI Observatory](https://github.com/neomundi-io/neomundi-ai-observatory) · [Weekly Barometer](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer)

This public release presents the **judged protocol** of the July 2026 NeoMundi AI Behavior Cartography.

It is based on one coherent analytical population:

```text
12 de-identified AI profiles
× 790 TruthfulQA questions per profile
= 9,480 source responses
```

Each source response is associated with:

- one observed stability measurement;
- one factuality assessment from an OpenAI-based judge, where available;
- one factuality assessment from a Mistral-based judge, where available.

The two factuality assessments are preserved separately.

They are not merged into a single consensus or absolute factuality score.

---

## Scope of this release

This directory contains the public outputs of the **Judged AI Behavior Cartography — `12 × 790`** protocol only.

The sibling runtime protocol:

```text
12 de-identified AI profiles
× 3 repeated waves
× 150 balanced questions
= 5,400 planned executions
```

is published separately in:

[Runtime Stability Cartography — `12 × 3 × 150`](../runtime-stability-cartography-12x3x150/)

The two protocols differ in:

- sampling logic;
- question composition;
- execution structure;
- metric families;
- analytical purpose.

They therefore remain analytically separate and are not combined into a universal quality score.

---

## Public profile identifiers

Observed systems are represented through stable opaque identifiers in the format:

```text
PROFILE-XXXXXX
```

These public identifiers are not derived from:

- provider names;
- model names;
- alphabetical order;
- performance;
- factuality;
- stability;
- score;
- ranking.

The private mapping between public profile identifiers and observed systems is retained separately and is not included in this repository.

The release is **de-identified**. It is not presented as irreversibly anonymous.

---

## Principal public metrics

Three principal indicators are reported for each de-identified profile.

### Mean observed stability

```text
mean_observed_stability_pct
```

The average observed behavioural stability across the 790 source responses.

This indicator measures the regularity of observed response behaviour.

It does not establish that the responses are factually correct.

### Factuality — OpenAI-based judge

```text
factuality_openai_pct
```

The proportion of scored responses classified as factually acceptable by the OpenAI-based judge.

### Factuality — Mistral-based judge

```text
factuality_mistral_pct
```

The proportion of scored responses classified as factually acceptable by the Mistral-based judge.

The two factuality assessments remain separate.

Neither judge is treated as an absolute source of truth.

---

## Secondary methodological indicators

The release also includes:

```text
interjudge_agreement_pct
cohen_kappa
openai_scored_n
mistral_scored_n
interjudge_pairs_n
```

These fields document:

- the observed level of agreement between the two judges;
- the effective number of scored observations;
- the number of comparable judge pairs;
- the coverage available for each calculation.

Cohen’s kappa is provided as a secondary methodological indicator.

It must be interpreted together with:

- observed agreement;
- score coverage;
- class balance;
- positive-verdict prevalence;
- directional disagreement;
- the effective number of comparable pairs.

No single agreement statistic establishes judge validity or factual ground truth.

---

## Coverage

Each profile contains:

```text
790 source responses
```

Automated factuality coverage may be lower than 790 for some profiles because not every response received a usable decision from both judges.

Factuality percentages must therefore always be interpreted together with:

```text
openai_scored_n
mistral_scored_n
interjudge_pairs_n
```

A missing or invalid judge decision is not automatically treated as a factual failure.

Rows excluded from inter-judge comparison must remain visible through coverage reporting.

---

## Interpretation doctrine

This release must not be interpreted as a model leaderboard.

Its purpose is to observe differences among behavioural profiles across several distinct dimensions.

In particular:

- high stability does not imply high factuality;
- high factuality does not imply behavioural stability;
- agreement between automated judges does not establish ground truth;
- disagreement between judges is a methodological signal;
- a monthly observation is a measurement snapshot, not a permanent characterisation of a system.

The meaningful unit of analysis is the multidimensional profile and, over time, its trajectory.

> A signal is an observation requiring interpretation, not a verdict.

---

## Public files

### `public_monthly_cartography_profile_summary.csv`

Profile-level public dataset containing the principal and secondary metrics.

### `public_monthly_cartography_metrics.json`

Machine-readable release metadata and public metrics.

### `public_deidentification_audit.txt`

Audit record documenting that:

- 12 private profiles were mapped;
- 12 unique public profile identifiers were generated;
- provider and model fields were removed;
- forbidden provider or model terms were absent from the public export;
- the private mapping registry was not exported.

The release manifest or public directory inventory should be treated as authoritative when additional files are present.

---

## Public release boundary

This release contains aggregated profile-level results.

It does not include:

- provider or model identities;
- the private profile-mapping registry;
- raw prompts;
- complete raw responses;
- request IDs;
- trace IDs;
- raw API payloads;
- exact execution timestamps;
- internal execution metadata;
- private judge settings;
- internal diagnostics;
- unpublished campaign exports;
- the sibling runtime `12 × 3 × 150` dataset;
- a unified or composite ranking.

Public transparency does not require uncontrolled disclosure of protected operational material.

---

## Limitations

The results are conditional on:

- the July 2026 observation period;
- the selected TruthfulQA corpus;
- the execution conditions used during collection;
- the NeoMundi stability measurement framework;
- the behaviour and coverage of the two automated judges;
- the inclusion and exclusion rules applied during scoring;
- the aggregation rules used for this release.

Automated factuality evaluation remains an estimation procedure.

Judge disagreement and incomplete coverage are retained in the public data rather than concealed through forced aggregation.

The results must not be generalised automatically to:

- other corpora;
- other languages;
- other domains;
- production deployments;
- high-risk use cases;
- future model versions;
- future judge configurations.

---

## Reproducibility boundary

The public artefacts can be inspected for:

- internal consistency;
- metric definitions;
- score coverage;
- profile-level aggregation;
- release metadata;
- de-identification controls;
- methodological limitations.

Full reproduction from source may require access to protected material, including:

- private campaign exports;
- complete source responses;
- complete prompt material;
- private profile mappings;
- judge configuration details;
- internal execution traces;
- infrastructure configuration;
- validation artefacts not included in the public release.

Public reproducibility therefore applies within the boundaries explicitly documented by the release.

---

## Future monthly releases

Compatible future releases should preserve:

- stable public profile identifiers;
- the principal metric definitions;
- explicit judge coverage;
- separate factuality results for each judge;
- documented inter-judge metrics;
- transparent methodological changes;
- release manifests and integrity information;
- explicit compatibility notes for longitudinal comparison.

Any modification to the corpus, judges, thresholds, inclusion rules or aggregation logic must be documented before comparisons are made across months.

Historical releases should not be silently rewritten.

---

## Responsible use

These measurements are intended to support:

- AI observability;
- behavioural comparison;
- methodological review;
- longitudinal analysis;
- governance evidence.

They should not be used alone to make:

- procurement decisions;
- safety determinations;
- compliance determinations;
- deployment decisions;
- universal quality claims;
- provider rankings.

**NeoMundi publishes observable, auditable and reproducible behavioural evidence — not rankings.**
