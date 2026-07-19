# NeoMundi AI Behavior Cartography

🌐 **Language:** [English](./README.md) · [Français](./README_FR.md)

🌍 **NeoMundi:** [English website](https://neomundi.org/en/home) · [Site français](https://neomundi.org/)

The **NeoMundi AI Behavior Cartography** is a public and reproducible measurement programme designed to compare how generative AI systems behave across shared factual corpora, repeated executions and documented runtime conditions.

It does not rank providers or models.

It publishes de-identified, comparable and methodologically separated observations intended to make differences in stability, factuality, semantic variation, coherence, latency and behavioural regimes visible.

> A benchmark produces a score.  
> NeoMundi maps distinct behavioural properties without collapsing them into one verdict.

---

## Programme objective

The Cartography is designed to answer several complementary questions:

- How do observed AI systems behave under comparable conditions?
- How stable are their responses across repeated executions?
- How does observed stability relate to externally judged factuality?
- Where do independent factuality judges agree or disagree?
- Which systems exhibit greater semantic variation or regime change?
- How do runtime signals evolve across repeated waves?
- Which properties can be measured separately without producing a universal quality score?

The Cartography treats AI behaviour as a multidimensional measurement object.

It does not assume that stability implies truth, that factuality implies stability, or that one aggregate score can represent the full behaviour of an AI system.

---

## Programme structure

The repository contains six main components:

- **Judged AI Behavior Cartography** — comparative observation across a complete factual-evaluation corpus;
- **Runtime Stability Cartography** — repeated runtime observation across multiple waves;
- **Monthly releases** — dated public publication cycles;
- **Methodology** — active protocol definitions and interpretation boundaries;
- **Usage guides** — instructions for reproducing or reviewing the public workflows;
- **Open science framework** — contribution, review and public reuse principles.

---

## July 2026 methodological structure

The July 2026 Cartography is based on two independent public protocols.

These protocols answer different analytical questions and remain separate.

---

## Protocol 1 — Judged AI Behavior Cartography

The first protocol is based on:

```text
12 de-identified AI profiles
× 790 TruthfulQA questions
= 9,480 source responses
```

The protocol includes:

- 12 de-identified AI profiles;
- the complete 790-question TruthfulQA corpus;
- 9,480 source responses;
- observed stability measurements;
- factuality assessment by an OpenAI-based judge;
- factuality assessment by a Mistral-based judge;
- inter-judge agreement;
- Cohen’s kappa as a secondary agreement indicator;
- separate preservation of each judge’s decisions.

Its purpose is to compare observed response stability with externally judged factuality across a broad factual-evaluation corpus.

The two factuality judges are not merged into one absolute factuality score.

Their separate outputs make disagreement visible and preserve the limits of automated factuality assessment.

Release directory:

```text
releases/july2026-behavior-cartography/judged-cartography-12x790/
```

---

## Protocol 2 — Runtime Stability Cartography

The second protocol is based on:

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
- 5,400 executions;
- stability measurements;
- semantic-variation signals;
- coherence indicators;
- latency observations;
- behavioural-regime classification;
- comparison across repeated waves.

Its purpose is to observe runtime variability and changes in behavioural regime under repeated and documented execution conditions.

This protocol focuses on repeated behaviour rather than external factuality judgement.

Release directory:

```text
releases/july2026-behavior-cartography/runtime-stability-12x3x150/
```

---

## Why the protocols remain separate

The two protocols are complementary, but they are not interchangeable.

The judged protocol evaluates behaviour across a broad factual corpus and compares observed stability with two independent factuality assessments.

The runtime protocol evaluates how behaviour changes across repeated executions and waves.

They therefore answer different questions:

| Protocol | Primary question |
|---|---|
| Judged Cartography — `12 × 790` | How do stability and judged factuality compare across a broad factual corpus? |
| Runtime Cartography — `12 × 3 × 150` | How does behaviour vary across repeated runtime conditions? |

The protocols are not merged into a universal quality score.

A system may appear stable while producing factually weak answers.

A system may appear variable while still producing factually acceptable answers.

A judge may disagree with another judge without either result becoming an absolute truth guarantee.

---

## Monthly publication cycle

The Cartography is designed as a recurring monthly observation programme.

Each monthly cycle may include one or more protocols depending on:

- data availability;
- methodological maturity;
- campaign quality;
- coverage;
- validation status;
- publication readiness.

Monthly releases are published in dated directories and preserve their own:

- protocol version;
- scope;
- metrics;
- limitations;
- manifests;
- data boundaries;
- interpretation rules.

Longitudinal comparisons may be introduced as the number of compatible monthly releases increases.

No comparison across months should be made without first verifying that the underlying protocols, datasets, scoring rules and release conditions are compatible.

---

## Public data and evidence

Depending on the protocol and release, the public repository may expose:

- aggregated results by de-identified profile;
- aggregated results by question or question family;
- observed stability measurements;
- factuality results from each judge;
- inter-judge agreement;
- Cohen’s kappa;
- semantic-variation indicators;
- coherence indicators;
- latency summaries;
- behavioural-regime distributions;
- coverage and completeness information;
- metric definitions;
- methodology documents;
- protocol versions;
- release manifests;
- integrity hashes;
- analytical reports;
- visual cartographies;
- documented limitations.

Public evidence is designed to support:

- internal consistency checks;
- methodological review;
- independent analysis;
- comparison across profiles;
- comparison across releases;
- public discussion of observed behavioural properties.

---

## Protected and restricted data

Public transparency does not require uncontrolled disclosure of the operational assets that protect the integrity, security and continuity of the measurement programme.

Depending on the protocol, the protected measurement boundary may include:

- provider and model identities;
- the private profile-mapping registry;
- complete prompts where disclosure would compromise the protocol;
- complete raw responses;
- request IDs and trace IDs;
- raw API payloads;
- exact execution timestamps;
- API keys and infrastructure credentials;
- detailed unaggregated token and cost data;
- internal diagnostics;
- debugging material;
- judge configuration details;
- private campaign exports;
- internal pipeline versions;
- proprietary calculation logic;
- artefacts that could enable profile re-identification;
- unpublished results;
- experimental signals not yet qualified for public release;
- review notes and internal validation material.

This separation preserves public scrutiny while protecting operational continuity, confidentiality, research integrity and de-identification.

---

## De-identification

Public profiles use stable opaque identifiers in the format:

```text
PROFILE-XXXXXX
```

These identifiers are not derived from:

- provider names;
- model names;
- alphabetical order;
- performance;
- factuality;
- stability;
- score;
- ranking.

The private mapping between public profiles and observed systems is retained separately.

The releases are **de-identified**. They are not presented as irreversibly anonymous.

Residual re-identification risk is treated as a publication limitation.

---

## Observed signal families

Depending on the protocol and available coverage, the Cartography may publish or document:

- stability;
- semantic variation;
- coherence;
- factuality assessment;
- inter-judge agreement;
- Cohen’s kappa;
- behavioural regimes;
- inter-wave variation;
- latency;
- coverage and completeness;
- cost and token-consumption indicators where available;
- `delta_g`, reported as an advanced observable runtime-variation signal.

No individual indicator should be interpreted in isolation as a complete assessment of quality, truthfulness, safety, compliance or governability.

---

## Interpretation doctrine

The Cartography follows one fundamental rule:

> A signal is an observation requiring interpretation, not a verdict.

An observed difference does not, by itself, establish:

- the superiority of one system over another;
- a provider-side model update;
- a causal explanation;
- a safety level;
- regulatory compliance;
- deployment suitability;
- truthfulness across all domains;
- overall quality;
- governability in a specific operational context.

The appropriate formulation is:

> A behavioural difference was observed under the conditions of the protocol.

Causal attribution requires additional evidence.

---

## Reproducibility boundary

The public repository is designed to support transparent inspection of:

- methods;
- protocol structure;
- released metrics;
- aggregated data;
- coverage;
- manifests;
- integrity information;
- analytical limitations.

Full reproduction from source may require access to:

- protected campaign exports;
- private infrastructure configuration;
- restricted prompt material;
- private judge settings;
- non-public execution traces;
- internal validation artefacts.

Each release documents its own reproducibility boundary.

Public reproducibility means that released artefacts can be inspected, checked and analysed within the limits explicitly stated by the programme.

---

## What this programme is not

The NeoMundi AI Behavior Cartography is not:

- a provider ranking;
- a model leaderboard;
- a universal benchmark score;
- a safety certification;
- a guarantee of factual accuracy;
- a legal or regulatory determination;
- a deployment authorisation;
- a substitute for human review;
- a substitute for domain-specific validation;
- a substitute for runtime governance.

It is a public metrological instrument for mapping distinct properties of AI behaviour under documented conditions.

---

## Scientific principles

The programme follows seven principles:

1. **Measure before interpreting.**
2. **Keep distinct properties analytically separate.**
3. **Repeat before generalising.**
4. **Never confuse stability with truth.**
5. **Preserve judge disagreement rather than conceal it.**
6. **Distinguish observation, interpretation and causal attribution.**
7. **Treat every signal as an element of evidence, not as a verdict.**

---

## Repository navigation

| Resource | English | Français |
|---|---|---|
| Programme overview | [README.md](./README.md) | [README_FR.md](./README_FR.md) |
| Methodology | [Methodology_EN.md](./Methodology_EN.md) | [Methodologie_FR.md](./Methodologie_FR.md) |
| Usage guide | [USAGE_EN.md](./USAGE_EN.md) | [USAGE_FR.md](./USAGE_FR.md) |
| Open science and contributions | [OPEN_SCIENCE.md](./OPEN_SCIENCE.md) | [OPEN_SCIENCE.md](./OPEN_SCIENCE.md) |
| Monthly releases | [releases/](./releases/) | [releases/](./releases/) |
| Scripts | [scripts/](./scripts/) | [scripts/](./scripts/) |

---

## Related NeoMundi programmes

- [NeoMundi AI Observatory](https://github.com/neomundi-io/neomundi-ai-observatory)
- [NeoMundi Weekly Barometer](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer)
- [NeoMundi official website — English](https://neomundi.org/en/home)
- [NeoMundi official website — French](https://neomundi.org/)
- [From AI Observability to Governance Metrology](https://doi.org/10.5281/zenodo.21250268)
- [Theoretical Framework — Law E](https://doi.org/10.5281/zenodo.19385052)

---

## Open science and contributions

The repository supports methodological review, independent analysis and documented contribution.

See:

- [Open science and contributions](./OPEN_SCIENCE.md)
- [NeoMundi AI Observatory contribution framework](https://github.com/neomundi-io/neomundi-ai-observatory/tree/main/governance)

Contributions may concern:

- methodology;
- protocol review;
- data analysis;
- factuality evaluation;
- reproducibility;
- visualisation;
- scientific writing;
- translation;
- governance;
- interoperability;
- sector-specific interpretation.

Contributions do not create authority over the programme, the observed systems or NeoMundi’s institutional decisions unless explicitly agreed in writing.

---

## License

This repository uses the [Apache License 2.0](LICENSE).

Specific datasets, reports, scripts, external contributions or release artefacts may include additional notices where required.

---

**NeoMundi AI Behavior Cartography**  
*Comparative measurement without universal ranking.*
