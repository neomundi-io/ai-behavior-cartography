# July 2026 Runtime Stability Cartography — 12 Profiles × 3 Waves × 150 Questions

This public release presents the July 2026 NeoMundi Runtime Stability Cartography.

The experiment was designed to observe the behavioral characteristics of 12 de-identified AI profiles across three repeated execution waves using the same balanced panel of 150 questions.

The resulting dataset contains:

- 12 de-identified AI profiles;
- 3 execution waves;
- 150 questions per profile and per wave;
- 450 observations per profile;
- 1,800 observations per wave;
- 5,400 observations in total.

The profiles are represented through persistent pseudonymous identifiers in the form:

`PROFILE-XXXXXX`

Provider and model identities are not part of the public release.

## Purpose of this release

This dataset studies runtime behavioral signals across repeated executions.

Its primary purpose is to observe:

- behavioral stability;
- variation between execution waves;
- semantic instability signals;
- changes in the NeoMundi runtime governance signals;
- operational characteristics such as latency and information density.

It is not designed to produce an external factuality ranking.

No external AI judge was used in this protocol.

## Relationship with the judged 12 × 790 cartography

This release is methodologically separate from the July 2026 Judged AI Behavior Cartography based on 12 profiles and 790 TruthfulQA questions.

The two datasets are no longer combined.

The judged `12 × 790` release is used for the public monthly comparison of:

- observed stability;
- factuality assessed by an OpenAI-based judge;
- factuality assessed by a Mistral-based judge;
- agreement between the two judges.

The present `12 × 3 × 150` release focuses instead on runtime behavioral measurements collected across three repeated waves.

Because the two protocols differ in their sampling design, repetition structure and interpretation, their metrics should not be aggregated into a single composite result.

This release is therefore published as an independent companion dataset.

## Experimental design

The protocol is identified as:

`balanced-150-v1`

For each of the 12 profiles:

1. the same balanced panel of 150 questions was executed;
2. the panel was repeated across three separate waves;
3. runtime measurements were collected for each execution;
4. results were aggregated by profile and across the full panel.

Expected observations:

| Level | Expected observations |
|---|---:|
| Per profile and per wave | 150 |
| Per profile across three waves | 450 |
| Per wave across 12 profiles | 1,800 |
| Full panel | 5,400 |

The release contains 5,400 observed rows, corresponding to the complete expected panel. :contentReference[oaicite:1]{index=1}

## Metrics

### Stability

`stability`

Observed regularity of the system’s runtime behavior.

The public release provides:

- mean;
- median;
- standard deviation;
- number of scored observations.

A higher stability score indicates more regular observed behavior under the NeoMundi measurement framework.

It does not establish factual correctness.

### Semantic instability

`semantic_instability`

Runtime signal intended to detect meaningful semantic variation in the observed output.

This is a measurement signal, not a definitive classification of error.

### Delta G

`delta_g`

Observed variation in the system’s runtime stability state.

Delta G is intended to capture changes in the measured behavioral regime rather than assess the truth of the generated content.

It should be interpreted together with stability, semantic instability and the final runtime regime.

### Factual signal

`factual_signal`

This field is derived from the NeoMundi runtime signal:

`factual_hallucination_score`

It is not the result of an external factuality judge and must not be interpreted as an independent factual verdict.

It is retained as a behavioral risk signal within the runtime measurement framework.

### Coherence

`coherence`

Internal runtime coherence signal available for supported observations.

A value of `1.0` does not mean that a response is factually correct, complete or suitable for deployment.

### Latency

`latency_ms`

Observed end-to-end execution latency, expressed in milliseconds.

Latency may be affected by:

- model provider infrastructure;
- network conditions;
- streaming behavior;
- retries;
- runtime configuration;
- execution date and time.

It should not be interpreted as a permanent provider benchmark.

### Information density

`information_density`

Internal signal estimating the informational concentration of the generated response.

This metric is available only where the corresponding runtime field was exported.

### Energy

`energy`

Internal normalized runtime signal produced by the NeoMundi measurement framework.

This is not a direct measurement of electricity consumption or physical energy use.

### Cost

`cost`

Internal normalized runtime field.

A constant value must not be interpreted as a monetary comparison between providers.

### Regime

`regime`

Final runtime governance state associated with the observation.

The profile summary includes:

- the dominant regime;
- the number of distinct regimes observed.

A regime is a governance signal produced by the measurement framework. It is not, by itself, an authorization or deployment decision.

## Coverage and missing values

The full source panel contains 5,400 observations.

Metric coverage differs depending on the availability of the underlying runtime fields:

- stability: 5,399 scored observations;
- semantic instability: 5,399;
- Delta G: 5,396;
- factual signal: 5,399;
- latency: 5,399;
- coherence: 4,949;
- cost: 4,949;
- information density: 4,949;
- energy: 4,949.

Missing metric values are not automatically interpreted as failures or zero scores.

One profile has no exported values for coherence, cost, information density or energy in this release. Comparisons involving these fields must therefore use the corresponding `scored_n` values.

## Data-quality note

The source panel contains the complete expected number of 5,400 rows and no duplicate profile-wave-item combinations were detected.

However, the automated quality metadata reports:

- one missing item identifier;
- 5,399 observations scored for several principal metrics instead of 5,400;
- 5,396 observations scored for Delta G;
- `structure_valid: false`.

The release is therefore suitable for exploratory behavioral analysis, but these quality conditions must be retained when interpreting aggregate results.

No missing observation or missing metric is silently converted into a zero value.

## Retry handling

For one profile, the initial files from each of the three waves were excluded and replaced by retry files.

Only the selected retry executions are included in the public aggregates.

The original and retry files were not combined, preventing duplicate observations.

This replacement is documented in the machine-readable metadata.

## Interpretation

This release should not be interpreted as a model leaderboard.

In particular:

- stability is not factuality;
- coherence is not truth;
- a factual runtime signal is not an external factual verdict;
- lower latency does not establish higher quality;
- a dominant `ALLOW` regime does not establish that every response is safe or correct;
- differences observed during one execution period may not remain unchanged after model, provider or infrastructure updates.

The meaningful object of analysis is the multidimensional behavioral profile and its evolution across waves.

## Files

### `public_balanced_cartography_profile_summary.csv`

Public profile-level summary containing aggregated metrics for each of the 12 pseudonymous profiles.

### `public_balanced_cartography_metrics.json`

Machine-readable release metadata, global metrics, coverage information, source-selection notes and profile-level summaries.

### `public_deidentification_audit.txt`

Public audit record confirming that the canonical pseudonymous profile identifiers were applied and that private provider or model identifiers were not included in the public datasets.

The public version of this audit must not contain the private profile correspondence table.

## De-identification policy

This release uses the same canonical public profile identifiers as the other NeoMundi cartography and barometer releases.

The mapping is managed through a private single source of truth.

No new public identifiers were generated specifically for this release.

The private correspondence between providers, models and public profile identifiers is not part of the intended public dataset.

## Release scope

The public release contains aggregated profile-level metrics.

It does not contain:

- raw provider names;
- raw model names;
- the private profile mapping;
- raw prompts;
- raw responses;
- private execution credentials;
- external factuality judgments;
- a composite ranking;
- a cross-aggregation with the judged `12 × 790` protocol.

## Limitations

The results are conditional on:

- the selected 150-question panel;
- the three July 2026 execution waves;
- the runtime conditions observed during collection;
- the versions of the tested systems at execution time;
- provider availability and latency;
- the NeoMundi measurement framework;
- the availability of exported runtime fields.

The three waves increase observational depth but do not establish long-term reproducibility on their own.

Longitudinal claims require repeated measurements over longer periods and explicit monitoring of model and infrastructure changes.

## Responsible use

These measurements are signals, not verdicts.

They are intended to support:

- AI observability;
- runtime metrology;
- behavioral comparison;
- reproducibility analysis;
- longitudinal governance.

They should not be used alone to make procurement, compliance, safety or deployment decisions.
