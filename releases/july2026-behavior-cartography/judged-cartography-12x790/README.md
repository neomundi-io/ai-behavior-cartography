# July 2026 Judged AI Behavior Cartography — 12 × 790

This public release presents the July 2026 NeoMundi AI Behavior Cartography based on a single, simplified protocol:

- 12 de-identified AI profiles
- 790 TruthfulQA questions per profile
- 9,480 source responses in total
- one observed stability measurement per response
- two independent automated factuality assessments

The public profiles are represented by persistent pseudonymous identifiers. Provider and model names are not disclosed.

## Methodological simplification

The monthly public cartography now relies exclusively on the complete `12 × 790` judged corpus.

An earlier methodological design considered combining these results with a separate balanced panel of:

- 12 profiles
- 3 question families
- 150 observations per family

This cross-protocol aggregation is no longer used in the public monthly cartography.

The two protocols differ in their sampling logic, question composition and intended analytical purpose. Combining them would make the interpretation less direct and could introduce unnecessary methodological ambiguity.

The July public release therefore uses one coherent analytical population only: the 9,480 responses generated from the 790-question TruthfulQA corpus.

The separate `12 × 3 × 150` panel may still be studied independently, but it is not included in the metrics published in this release.

## Public metrics

Three principal indicators are reported for each de-identified profile:

### Mean observed stability

`mean_observed_stability_pct`

The average observed behavioral stability across the 790 responses.

This indicator measures the regularity of the observed response behavior. It does not establish that the responses are factually correct.

### Factuality — OpenAI judge

`factuality_openai_pct`

The proportion of scored responses classified as factually acceptable by the OpenAI-based judge.

### Factuality — Mistral judge

`factuality_mistral_pct`

The proportion of scored responses classified as factually acceptable by the Mistral-based judge.

The two factuality assessments are intentionally preserved separately. They are not merged into a single consensus score.

## Secondary methodological indicators

The release also includes:

- `interjudge_agreement_pct`
- `cohen_kappa`
- `openai_scored_n`
- `mistral_scored_n`
- `interjudge_pairs_n`

These fields document the level of agreement between the two judges and the effective number of observations available for each calculation.

Cohen’s kappa is provided as a secondary methodological indicator. It should be interpreted together with agreement rates, score coverage and the distribution of judge decisions.

## Coverage

Each profile contains 790 source responses.

Automated factuality coverage may be lower than 790 for some profiles because not every response received a usable decision from both judges.

For this reason, factuality percentages must always be read together with:

- `openai_scored_n`
- `mistral_scored_n`
- `interjudge_pairs_n`

No missing judge decision is automatically treated as a factual failure.

## Interpretation

This release should not be interpreted as a model leaderboard.

The profiles are de-identified, and the purpose of the cartography is not to declare one provider or model universally superior to another.

The objective is to observe differences between behavioral profiles across several independent dimensions.

In particular:

- high stability does not imply high factuality;
- high factuality does not imply behavioral stability;
- agreement between automated judges does not establish ground truth;
- a monthly observation is a measurement snapshot, not a permanent characterization of a system.

The meaningful unit of analysis is therefore the multidimensional profile and, over time, its trajectory.

## Files

### `public_monthly_cartography_profile_summary.csv`

Profile-level public dataset containing the principal and secondary metrics.

### `public_monthly_cartography_metrics.json`

Machine-readable version of the public metrics and release metadata.

### `public_deidentification_audit.txt`

Audit record confirming that:

- 12 private profiles were mapped;
- 12 unique public profile identifiers were generated;
- provider and model fields were removed;
- forbidden provider or model terms were absent;
- the private mapping was not exported.

## De-identification

The public release uses persistent pseudonymous identifiers in the form:

`PROFILE-XXXXXX`

The private mapping between these identifiers and the underlying systems is not part of the public repository.

The de-identification audit reports the release as safe for public publication. :contentReference[oaicite:0]{index=0}

## Release scope

This release contains aggregated profile-level results only.

It does not include:

- private provider or model identities;
- the private correspondence table;
- raw prompts and responses;
- internal execution metadata;
- the separate balanced `12 × 3 × 150` protocol;
- a unified or composite ranking.

## Limitations

The results are conditional on:

- the July 2026 execution period;
- the selected TruthfulQA corpus;
- the runtime conditions observed during collection;
- the NeoMundi stability measurement framework;
- the behavior and coverage of the two automated judges.

Automated factuality evaluation remains an estimation procedure. Judge disagreement and incomplete coverage are retained in the public data rather than concealed through forced aggregation.

## Reproducibility and future releases

Future monthly releases should preserve:

- the same public profile identifiers;
- the same principal metric definitions;
- explicit score coverage;
- separate factuality results for each judge;
- transparent methodological changes.

Any future modification of the corpus, judges, thresholds or aggregation rules should be documented before longitudinal comparison.

## Responsible use

These measurements are signals, not verdicts.

They are intended to support AI observability, behavioral comparison and longitudinal governance. They should not be used alone to make procurement, safety, compliance or deployment decisions.
