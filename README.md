# NeoMundi — TruthfulQA Profile Cartography

- [English README](./README.md)
- [README français](./README_FR.md)
- [English methodology](./Methodology_EN.md)
- [Méthodologie française](./Methodologie_FR.md)
- [English usage guide](./USAGE_EN.md)
- [Guide d’utilisation en français](./USAGE_FR.md)
- [Open science and contributions](./OPEN_SCIENCE.md)

Public, reproducible cartography of pseudonymous AI profiles derived from a TruthfulQA factual-evaluation corpus, double-judge validation and separate runtime behavioral signals.

## Purpose

This repository documents a multidimensional AI cartography methodology.

It does not publish:

* provider names;
* model names;
* rankings;
* ratings;
* composite scores;
* raw responses;
* question-level traces;
* judge rationales.

The objective is to expose observable, auditable and reproducible profiles without reducing AI behavior to a single leaderboard.

## Public release

Current frozen release:

```text
releases/truthfulqa-profiles-v1.0.0/
```

This release includes:

* pseudonymous profile summaries;
* runtime profile summaries;
* methodology-validation metrics;
* a public data dictionary;
* a publication review checklist;
* a release manifest;
* SHA-256 checksums.

---

## Explore NeoMundi

NeoMundi is developing a continuous measurement framework to make AI behavior more observable, auditable and governable.

Test the instrument: https:controltower.neomundi.io
Discover NeoMundi & explore the technical documentation: https://github.com/neomundi-io
Follow the open-science program: https://neomundi.org
Contact: contact@neomundi.io

## Methodological principles

The public methodology keeps the following layers separate:

1. factual evaluation;
2. inter-judge calibration;
3. runtime behavioral signals;
4. repeatability;
5. pseudonymous public profiles.

No consolidated binary verdict is treated as absolute truth.

Runtime signals are not merged into a universal quality score.

## Validation scripts

Reproducible validation scripts are available in:

```text
scripts/validation/
```

They cover:

* corpus inventory audit;
* OpenAI ↔ Mistral agreement analysis;
* disagreement-structure analysis.

## Publication script

The conservative public exporter is available in:

```text
scripts/publication/export_public_profiles.py
```

It:

* applies stable pseudonymization;
* separates private mapping metadata from public artifacts;
* blocks provider and model-name leakage;
* rejects ranking, rating and composite-score fields;
* generates a public manifest, data dictionary and SHA-256 checksums;
* requires manual review before publication.

## Current methodological findings

The current TruthfulQA double-judge release documents:

* 12 pseudonymous profiles;
* 9,087 comparable judgment pairs;
* 81.42% observed agreement;
* pooled Cohen kappa = 0.6342;
* 1,688 disagreements;
* a systematic calibration difference between the two judges.

These results describe inter-judge behavior. They do not establish an absolute reference judge.

## Planned extensions

Future work includes:

* a third independent judge;
* intra-judge repeatability analysis;
* a stratified human-adjudication panel;
* replication on additional factual and domain-specific corpora;
* separate behavioral cartography releases on repeated-run panels.

## Governance rule

NeoMundi publishes observable profiles, not rankings.

## License

Apache License 2.0.
