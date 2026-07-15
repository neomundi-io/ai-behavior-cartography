# NeoMundi — AI Behavioral Cartography

- [English README](./README.md)
- [README français](./README_FR.md)
- [English methodology](./Methodology_EN.md)
- [Méthodologie française](./Methodologie_FR.md)
- [English usage guide](./USAGE_EN.md)
- [Guide d’utilisation en français](./USAGE_FR.md)
- [Open science and contributions](./OPEN_SCIENCE.md)

# NeoMundi AI Behavior Cartography

NeoMundi develops a public and reproducible framework for observing how generative AI systems behave across factual-evaluation corpora, repeated executions and runtime signals.

This repository documents the progressive qualification of that measurement instrument.

It publishes de-identified behavioral observations designed to make AI systems more observable, auditable and governable over time.

The objective is not to rank providers or declare a universally superior model.

The objective is to measure distinct properties of AI behavior without collapsing them into a single score.

## What this repository contains

The repository currently brings together several complementary public releases:

- a judged behavioral cartography based on a complete 790-question TruthfulQA corpus;
- a runtime stability cartography based on three repeated waves of a balanced 150-question panel;
- methodological documentation on factuality assessment, judge agreement, runtime stability, semantic variation and longitudinal observation;
- public de-identification and release-control artifacts.

Each release has its own protocol, analytical purpose and limitations.

The protocols are published separately and are not aggregated into a universal quality score.

## Current methodological structure

The July 2026 cartography is based on two independent public protocols.

### 1. Judged AI Behavior Cartography — 12 × 790

This protocol contains:

- 12 de-identified AI profiles;
- 790 TruthfulQA questions per profile;
- 9,480 source responses;
- observed stability measurements;
- factuality assessment by an OpenAI-based judge;
- factuality assessment by a Mistral-based judge;
- inter-judge agreement and Cohen’s kappa.

Its purpose is to compare observed stability and externally judged factuality across a complete factual-evaluation corpus.

The two factuality judges are preserved separately.

Their decisions are not merged into a single absolute factuality score.

Release directory:

```text
releases/july2026-behavior-cartography/judged-cartography-12x790/
