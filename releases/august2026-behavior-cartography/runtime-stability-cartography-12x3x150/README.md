# August 2026 Runtime Stability Cartography — `12 × 3 × 150`

🌐 **Documentation:** [August 2026 release index](https://github.com/neomundi-io/ai-behavior-cartography/blob/main/releases/august2026-behavior-cartography/README.md) · [Programme overview](https://github.com/neomundi-io/ai-behavior-cartography/blob/main/README.md) · [Public methodology](https://github.com/neomundi-io/ai-behavior-cartography/blob/main/Methodology_EN.md) · [Méthodologie publique](https://github.com/neomundi-io/ai-behavior-cartography/blob/main/Methodologie_FR.md)

🌍 **NeoMundi:** [AI Observatory](https://github.com/neomundi-io/neomundi-ai-observatory) · [Weekly Barometer](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer)

This public release presents the **Runtime Stability Cartography** protocol of the August 2026 NeoMundi AI Behavior Cartography.

The experiment observes the behavioural characteristics of 12 de-identified AI profiles across three repeated execution waves using the same balanced panel of 150 questions.

The resulting source panel contains:

```text
12 de-identified AI profiles
× 3 execution waves
× 150 questions
= 5,400 observations
```

This corresponds to:

* 150 observations per profile and per wave;
* 450 observations per profile across three waves;
* 1,800 observations per wave across 12 profiles;
* 5,400 observations in total.

Observed systems are represented through stable opaque identifiers in the form:

```text
PROFILE-XXXXXX
```

Provider and model identities are not included in the public release.

---

## Purpose of this release

This dataset studies runtime behavioural signals across repeated executions.

Its purpose is to observe:

* behavioural stability;
* variation between execution waves;
* semantic-variation signals;
* coherence;
* changes in runtime signal regimes;
* latency;
* information-density indicators;
* measurement coverage;
* operational variation.

It is not designed to produce an external factuality ranking.

No external AI factuality judge was used in this protocol.

---

## Relationship with the judged `12 × 790` Cartography

This release is methodologically separate from the August 2026 Judged AI Behavior Cartography based on:

```text
12 de-identified AI profiles
× 790 TruthfulQA questions
= 9,480 source responses
```

The judged protocol evaluates source responses through external judging layers.

The present `12 × 3 × 150` release instead focuses on runtime behavioural measurements collected across three repeated execution waves.

Because the two protocols differ in sampling design, repetition structure, metric families and analytical purpose, their outputs must not be aggregated into a single universal or composite score.

[Open the August judged Cartography release](https://github.com/neomundi-io/ai-behavior-cartography/tree/main/releases/august2026-behavior-cartography/judged-cartography-12x790)

---

## Experimental design

The protocol is identified as:

```text
balanced-150-v1
```

For each of the 12 profiles:

1. the same balanced panel of 150 questions was executed;
2. the panel was repeated across three separate waves;
3. runtime measurements were collected for each execution;
4. results were aggregated by profile and across the full panel.

Expected and observed structure:

| Level                          | Observations |
| ------------------------------ | -----------: |
| Per profile and per wave       |          150 |
| Per profile across three waves |          450 |
| Per wave across 12 profiles    |        1,800 |
| Full panel                     |        5,400 |

The August release contains the complete expected source panel:

```text
Expected: 5,400
Observed: 5,400
```

All 12 profiles and all three waves are represented.

---

## Global August metrics

The public release reports the following global behavioural measurements.

| Metric               |         Mean |       Median | Scored observations |
| -------------------- | -----------: | -----------: | ------------------: |
| Stability            |     0.895956 |     0.923077 |               5,400 |
| Coherence            |     1.000000 |     1.000000 |               4,950 |
| Semantic instability |     0.004204 |     0.000000 |               5,400 |
| `delta_g`            |    -0.003101 |     0.000000 |               5,398 |
| Factual-risk signal  |     0.088148 |     0.000000 |               5,400 |
| Latency              | 27,319.20 ms | 25,211.50 ms |               5,400 |
| Cost signal          |     1.000000 |     1.000000 |               4,950 |
| Information density  |     0.640220 |     0.656200 |               4,950 |
| Energy signal        |     0.998451 |     0.999003 |               4,950 |

These measurements describe observed runtime behaviour under the NeoMundi measurement framework.

They must not be interpreted as a universal model-quality score.

---

## Public metrics

### Stability

```text
stability
```

Observed regularity of the system's runtime behaviour.

The public release provides, where available:

* mean;
* median;
* standard deviation;
* number of scored observations.

A higher stability score indicates more regular observed behaviour under the NeoMundi measurement framework.

It does not establish factual correctness.

---

### Semantic variation

```text
semantic_instability
```

Runtime signal intended to detect meaningful semantic variation in the observed output.

This is a measurement signal, not a definitive classification of error.

---

### Delta G

```text
delta_g
```

Observable runtime-variation signal associated with changes in the measured behavioural state.

`delta_g` does not assess the factual truth of generated content.

It must be interpreted together with stability, semantic variation, measurement coverage and the final runtime regime.

---

### Factual-risk signal

```text
factual_signal
```

This field is derived from the NeoMundi runtime signal:

```text
factual_hallucination_score
```

It is not the result of an external factuality judge and must not be interpreted as an independent factual verdict.

It is retained as a behavioural risk signal within the runtime measurement framework.

---

### Coherence

```text
coherence
```

Internal runtime coherence signal available for supported observations.

A value of `1.0` does not mean that a response is factually correct, complete, safe or suitable for deployment.

---

### Latency

```text
latency_ms
```

Observed end-to-end execution latency, expressed in milliseconds.

Latency may be affected by:

* provider infrastructure;
* network conditions;
* streaming behaviour;
* retries;
* runtime configuration;
* execution date and time.

It must not be interpreted as a permanent provider benchmark.

---

### Information density

```text
information_density
```

Internal signal estimating the informational concentration of a generated response.

This metric is available only where the corresponding runtime field was exported.

---

### Energy

```text
energy
```

Internal normalised runtime signal produced by the NeoMundi measurement framework.

It is not a direct measurement of electricity consumption or physical energy use.

---

### Cost

```text
cost
```

Internal normalised runtime field.

A constant value must not be interpreted as a monetary comparison between providers.

---

### Regime

```text
regime
```

Final runtime signal state associated with the observation.

The profile summary includes:

* the dominant regime;
* the number of distinct regimes observed.

A regime is an analytical runtime signal.

It is not, by itself:

* a safety certification;
* an authorisation;
* a deployment decision;
* a regulatory determination;
* a causal explanation.

---

## Coverage and missing values

The complete August source panel contains:

```text
5,400 observations
```

Metric coverage is:

| Metric              | Scored observations |
| ------------------- | ------------------: |
| Stability           |               5,400 |
| Semantic variation  |               5,400 |
| `delta_g`           |               5,398 |
| Factual-risk signal |               5,400 |
| Latency             |               5,400 |
| Coherence           |               4,950 |
| Cost                |               4,950 |
| Information density |               4,950 |
| Energy              |               4,950 |

Missing metric values are not automatically interpreted as failures or zero scores.

One de-identified profile has no exported values for coherence, cost, information density or energy in this release.

Comparisons involving these fields must therefore use their corresponding `scored_n` values.

---

## Data-quality status

The August behavioural panel passes the structural validation controls.

```text
Panel structure valid: TRUE
Source record keys complete: TRUE
Expected observations: 5,400
Observed observations: 5,400
Profiles observed: 12
Waves observed: 3
CSV files selected: 36
Missing source identifiers: 0
Duplicate technical rows: 0
```

The August release therefore contains a structurally complete `12 × 3 × 150` behavioural panel.

No missing observation or missing metric is silently converted into a zero value.

---

## Interpretation doctrine

This release must not be interpreted as a model leaderboard.

In particular:

* stability is not factuality;
* coherence is not truth;
* a runtime factual-risk signal is not an external factual verdict;
* lower latency does not establish higher quality;
* a dominant `ALLOW` regime does not establish that every response is safe or correct;
* a difference between waves does not establish a provider-side update;
* observations from one execution period may not remain unchanged after model, provider or infrastructure changes.

The meaningful object of analysis is the multidimensional behavioural profile and its evolution across repeated observations.

> **A signal is an observation requiring interpretation, not a verdict.**

---

## Public files

### `public_balanced_cartography_profile_summary.csv`

Public profile-level summary containing aggregated metrics for each of the 12 de-identified profiles.

Each profile represents 450 observations across three execution waves.

---

### `public_balanced_cartography_metrics.json`

Machine-readable release artefact containing:

* protocol metadata;
* panel structure;
* global metrics;
* measurement coverage;
* source-selection information;
* profile-level aggregates;
* public quality metadata;
* de-identification metadata.

---

### `public_deidentification_audit.txt`

Public audit record documenting that:

* the canonical public profile identifiers were applied;
* no new public profile identifiers were generated;
* the private profile correspondence table was not exported;
* no provider/model identity leakage was detected in the public CSV;
* no provider/model identity leakage was detected in the public JSON.

The public audit does not contain the private profile-mapping registry.

---

## De-identification policy

This release uses the same canonical public profile identifiers as compatible NeoMundi Cartography and Barometer releases.

The mapping is managed through a private single source of truth.

No new public identifiers were generated specifically for this release.

The private correspondence between providers, models and public profile identifiers is not part of the public dataset.

The release is **de-identified**. It is not presented as irreversibly anonymous.

---

## Public release boundary

The public release contains aggregated profile-level metrics and machine-readable public metadata.

It does not contain:

* provider names;
* model names;
* the private profile-mapping registry;
* raw prompts;
* complete raw responses;
* request IDs;
* trace IDs;
* raw API payloads;
* exact execution timestamps;
* private execution credentials;
* private judge settings;
* external factuality judgements;
* internal diagnostics;
* unpublished campaign exports;
* a composite ranking;
* a cross-aggregation with the judged `12 × 790` protocol.

Public transparency does not require uncontrolled disclosure of protected operational material.

---

## Limitations

The results are conditional on:

* the selected 150-question panel;
* the three August 2026 execution waves;
* the runtime conditions observed during collection;
* the versions of the tested systems at execution time;
* provider availability and latency;
* the NeoMundi measurement framework;
* the availability of exported runtime fields.

The three waves increase observational depth but do not establish long-term reproducibility on their own.

Longitudinal claims require repeated measurements over longer periods and explicit monitoring of protocol, model and infrastructure changes.

---

## Reproducibility boundary

The public artefacts can be inspected for:

* profile-level aggregation;
* metric coverage;
* wave structure;
* source-panel completeness;
* public de-identification controls;
* machine-readable release metadata;
* documented limitations.

Full reproduction from source may require access to protected material, including:

* private campaign exports;
* complete source responses;
* complete prompt material;
* private profile mappings;
* internal execution traces;
* infrastructure configuration;
* private validation artefacts.

Public reproducibility therefore applies within the boundaries explicitly documented by the release.

---

## Longitudinal compatibility

Compatible future runtime releases should preserve:

* stable public profile identifiers;
* explicit panel versions;
* explicit wave definitions;
* principal metric definitions;
* coverage by metric;
* exclusion and retry documentation where applicable;
* release manifests;
* integrity information;
* compatibility notes for longitudinal comparison.

Any modification to the panel, metric definitions, thresholds, retry rules, wave structure or aggregation logic must be documented before cross-month comparison.

Historical releases should not be silently rewritten.

The purpose of preserving this structure is to enable progressively richer longitudinal observation across monthly releases.

---

## Responsible use

These measurements are intended to support:

* AI observability;
* runtime metrology;
* behavioural comparison;
* reproducibility analysis;
* longitudinal governance evidence.

They should not be used alone to make:

* procurement decisions;
* compliance determinations;
* safety determinations;
* deployment decisions;
* universal quality claims;
* provider rankings.

---

**NeoMundi publishes observable, auditable and reproducible behavioural evidence — not rankings.**
