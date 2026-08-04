# NeoMundi AI Behavior Cartography — August 2026 Public Release

🌐 **Documentation:** [Programme overview](../../README.md) · [Public methodology](../../Methodology_EN.md) · [Méthodologie publique](../../Methodologie_FR.md)

🌍 **NeoMundi:** [AI Observatory](https://github.com/neomundi-io/neomundi-ai-observatory) · [Weekly Barometer](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer)

This directory contains the public releases of the **NeoMundi AI Behavior Cartography for August 2026**.

The August programme is based on two independent and complementary protocols.

The protocols answer different analytical questions and are not merged into a universal quality score.

---

## 1. Judged AI Behavior Cartography — `12 × 790`

```text
12 de-identified AI profiles
× 790 TruthfulQA questions
= 9,480 source responses
```

The August judged protocol includes:

```text
9,480 OpenAI judge decisions
9,384 Mistral judge decisions
9,384 paired inter-judge comparisons
```

Eight TruthfulQA items are systematically absent from the Mistral evaluation set for every profile.

These exclusions are documented, excluded from paired analysis and not imputed.

This protocol compares:

- observed stability;
- factuality according to an OpenAI-based judge;
- factuality according to a Mistral-based judge;
- inter-judge agreement;
- directional disagreement;
- Cohen’s kappa as a secondary agreement indicator;
- coverage and methodological uncertainty.

The outputs of the two judges remain separate.

Their decisions are not merged into an absolute factuality score.

[Open the judged Cartography release](./judged-cartography-12x790/)

---

## 2. Runtime Stability Cartography — `12 × 3 × 150`

```text
12 de-identified AI profiles
× 3 repeated waves
× 150 balanced questions
= 5,400 planned executions
```

This protocol observes:

- repeated runtime behaviour;
- stability;
- semantic variation;
- coherence;
- latency;
- behavioural regimes;
- variation across waves;
- measurement coverage.

This protocol focuses on behavioural repeatability and runtime variation rather than external factuality judgement.

**Status: data collection and validation in progress.**

The public runtime release will be added after completion and validation of the three repeated waves.

[Open the runtime stability Cartography release](./runtime-stability-cartography-12x3x150/)

---

## Why the protocols remain separate

The judged protocol studies the relationship between observed stability and externally assessed factuality across a broad factual corpus.

The runtime protocol studies how behaviour changes across repeated execution waves.

A stable system is not necessarily factually correct.

A variable system is not necessarily factually incorrect.

Judge agreement is not an absolute guarantee of truth.

For these reasons, the protocols remain analytically separate.

---

## August headline indicators

Across the judged protocol:

- mean observed stability: **90.22%**;
- factuality according to the OpenAI judge: **68.69%**;
- factuality according to the Mistral judge: **69.50%**;
- inter-judge agreement: **85.55%**;
- Cohen’s kappa: **0.6620**.

These aggregate indicators describe the measured August cohort under the documented protocol.

They are not universal model-quality scores.

---

## Public release boundary

The August releases may publish:

- aggregated results by de-identified profile;
- judge-agreement metrics;
- stability and runtime summaries;
- behavioural-regime distributions;
- coverage information;
- metric definitions;
- release manifests;
- integrity and verification artefacts;
- documented limitations.

They do not publish by default:

- provider or model identities;
- the private profile-mapping registry;
- complete raw responses;
- protected prompts;
- request or trace identifiers;
- raw API payloads;
- exact execution timestamps;
- private judge settings;
- unpublished campaign exports;
- internal diagnostics.

The releases are **de-identified**. They are not presented as irreversibly anonymous.

---

## Interpretation doctrine

> A signal is an observation requiring interpretation, not a verdict.

The August Cartography does not constitute:

- a provider ranking;
- a model leaderboard;
- a universal benchmark score;
- a safety certification;
- a guarantee of factual accuracy;
- a deployment authorisation;
- a regulatory determination.

Each protocol must be interpreted within its documented scope, coverage and methodological limitations.
