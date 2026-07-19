# NeoMundi AI Behavior Cartography — Open Science and Contributions

🌐 **Language:** [English](./OPEN_SCIENCE.md) · [Français](./OPEN_SCIENCE_FR.md)

📘 **Programme overview:** [English README](./README.md) · [README français](./README_FR.md)

📐 **Methodology:** [English](./Methodology_EN.md) · [Français](./Methodologie_FR.md)

🧭 **Usage guides:** [English](./USAGE_EN.md) · [Français](./USAGE_FR.md)

🌍 **NeoMundi:** [AI Observatory](https://github.com/neomundi-io/neomundi-ai-observatory) · [Weekly Barometer](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer) · [English website](https://neomundi.org/en/home) · [Site français](https://neomundi.org/)

---

## 1. From benchmark scores to observable AI behaviour profiles

A leaderboard can answer one immediate question:

> Which system ranks first?

But it can conceal more important questions:

- Do two judges evaluate the same answer in the same way?
- Are disagreements random or structurally concentrated?
- Does runtime stability remain visible when factual judgements diverge?
- Can the same AI system exhibit different behavioural signatures across repeated panels?
- What information disappears when several dimensions are compressed into one score?
- Which observations are robust, and which remain protocol-dependent?

NeoMundi publishes multidimensional, de-identified AI behaviour profiles to make these questions observable.

The objective is not to replace one leaderboard with another.

The objective is to expose a reproducible cartography of:

- factual-evaluation views;
- inter-judge calibration;
- runtime behavioural signals;
- disagreement zones;
- repeatability;
- semantic variation;
- coherence;
- behavioural regimes;
- methodological uncertainty.

> A signal is an observation requiring interpretation, not a verdict.

---

## 2. Scope of the public Cartography

The NeoMundi AI Behavior Cartography currently includes two separate public protocols.

### Judged Cartography — `12 × 790`

```text
12 de-identified AI profiles
× 790 TruthfulQA questions
= 9,480 source responses
```

This protocol studies:

- observed stability;
- factuality according to an OpenAI-based judge;
- factuality according to a Mistral-based judge;
- inter-judge agreement;
- Cohen’s kappa;
- directional disagreement;
- methodological uncertainty.

### Runtime Cartography — `12 × 3 × 150`

```text
12 de-identified AI profiles
× 3 repeated waves
× 150 balanced questions
= 5,400 executions
```

This protocol studies:

- repeated runtime behaviour;
- stability;
- semantic variation;
- coherence;
- latency;
- behavioural regimes;
- inter-wave variation;
- measurement coverage.

The two protocols are complementary, but they are not merged into a universal quality score.

---

## 3. Open-science doctrine

NeoMundi treats open science as a commitment to make the following elements inspectable:

- methods;
- assumptions;
- public datasets;
- metric definitions;
- release manifests;
- integrity hashes;
- analytical limitations;
- validation logic;
- interpretation boundaries;
- documented corrections;
- public scripts where publication is compatible with security and research integrity.

Open science does not require uncontrolled disclosure of protected operational material.

> Open science means making methods, assumptions, released evidence, limitations and verification artefacts inspectable. It does not require uncontrolled publication of protected operational data.

Public transparency and operational protection are therefore treated as complementary requirements.

---

## 4. Source corpus

The judged protocol builds on the TruthfulQA benchmark introduced by Stephanie Lin, Jacob Hilton and Owain Evans.

- [Original paper — TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://arxiv.org/abs/2109.07958)
- [ACL Anthology publication](https://aclanthology.org/2022.acl-long.229/)
- [Official TruthfulQA repository](https://github.com/sylinrl/TruthfulQA)
- [Official public question and reference-answer file](https://github.com/sylinrl/TruthfulQA/blob/main/TruthfulQA.csv)

The original benchmark paper describes 817 questions across 38 categories.

The current NeoMundi judged Cartography uses the complete 790-question corpus retained by the active public protocol.

TruthfulQA is used as a factual-evaluation instrument. Results derived from it must not be interpreted as universal claims across all domains, languages, tasks or deployment contexts.

---

## 5. Public releases

The repository currently contains the following public release directories:

- [July 2026 Behavior Cartography](./releases/july2026-behavior-cartography/)
- [June 2026 Behavior Cartography v1.0.0](./releases/june2026-behavior-cartography-v1.0.0/)
- [TruthfulQA Profiles v1.0.0](./releases/truthfulqa-profiles-v1.0.0/)

The July 2026 programme separates:

- the judged `12 × 790` protocol;
- the runtime `12 × 3 × 150` protocol.

Each release has its own:

- protocol scope;
- methodology reference;
- data inventory;
- limitations;
- manifest;
- integrity information;
- reproducibility boundary.

Historical releases remain part of the public record and should not be silently rewritten.

---

## 6. Public evidence

Depending on the release, NeoMundi may publish:

- aggregated results by de-identified profile;
- aggregated results by question or question family;
- stability measurements;
- factuality outputs from separate judges;
- inter-judge agreement;
- Cohen’s kappa;
- semantic-variation indicators;
- coherence indicators;
- latency summaries;
- behavioural-regime distributions;
- inter-wave comparisons;
- coverage and completeness information;
- public data dictionaries;
- metric contracts;
- analytical reports;
- visual cartographies;
- release manifests;
- SHA-256 checksums;
- methodological limitations.

These artefacts are intended to support:

- internal consistency checks;
- independent review;
- methodological critique;
- reproducibility within documented boundaries;
- comparison across compatible releases;
- public discussion of observed AI behaviour.

---

## 7. Protected research material

The public repository does not represent the complete NeoMundi measurement record.

Depending on the protocol, protected material may include:

- provider and model identities;
- the private profile-mapping registry;
- complete raw responses;
- complete prompts where disclosure would compromise the protocol;
- request IDs;
- trace IDs;
- raw API payloads;
- exact execution timestamps;
- API keys;
- infrastructure credentials;
- private judge settings;
- detailed unaggregated token and cost data;
- unpublished campaign exports;
- internal diagnostics;
- debugging material;
- internal review notes;
- proprietary calculation logic;
- artefacts that could enable profile re-identification;
- experimental signals not yet qualified for publication.

This separation protects:

- confidentiality;
- operational continuity;
- research integrity;
- de-identification;
- security;
- future longitudinal comparability.

The public releases are **de-identified**. They are not presented as irreversibly anonymous.

---

## 8. Current methodological signals

The frozen judged release documents:

```text
12 de-identified profiles
9,480 source responses
9,087 comparable judgement pairs
81.42% observed inter-judge agreement
pooled Cohen’s kappa = 0.6342
1,688 disagreements
```

Among the disagreements:

```text
Judge A negative / Judge B positive: 1,491
Judge A positive / Judge B negative:   197
```

This directional asymmetry does not establish an absolute reference judge.

It shows that factual evaluation must itself be treated as a calibrated, traceable and observable layer.

The runtime `12 × 3 × 150` protocol separately documents repeated behavioural properties and must not be collapsed into the judged factuality results.

---

## 9. Why this matters

A model-selection or deployment decision cannot responsibly rely on a single public score.

A serious diagnostic may need to separate:

- factual evaluation;
- judge calibration;
- runtime stability;
- semantic variation;
- repeatability;
- coherence;
- latency;
- domain-specific risk;
- deployment context;
- cost and efficiency constraints;
- governance requirements.

The public Cartography intentionally exposes observable dimensions rather than universal recommendations.

---

## 10. Open questions

The following questions remain open:

1. Does inter-judge asymmetry persist with a third independent judge?
2. Which disagreement zones remain stable across repeated judging runs?
3. How much intra-judge variability exists under controlled conditions?
4. Which high-disagreement questions require human adjudication?
5. Do runtime behavioural signatures remain stable across repeated monthly panels?
6. Can reduced panels preserve the signal of larger behavioural corpora?
7. Which runtime dimensions become more informative in legal, medical, financial or agentic contexts?
8. How should multidimensional AI profiles be represented without recreating a hidden leaderboard?
9. Which protocol changes preserve longitudinal comparability?
10. Which public artefacts provide the strongest evidence without compromising de-identification?

---

## 11. Planned extensions

Future public work may include:

- a third independent judge;
- intra-judge repeatability analysis;
- a stratified human-adjudication panel;
- additional repeated-wave cartographies;
- sector-specific panels;
- multilingual corpora;
- adversarial protocols;
- independent replication;
- contributor-proposed analyses;
- additional runtime signals;
- longitudinal monthly comparisons.

Every extension must document its protocol, limits and compatibility with earlier releases.

---

## 12. Invitation to contribute

Researchers, engineers, auditors, statisticians, domain experts, translators and AI builders are invited to contribute.

Possible contributions include:

- methodological review;
- reproducibility testing;
- additional public panels;
- third-judge experiments;
- human-adjudication protocols;
- statistical analysis;
- data visualisation;
- legal, medical, financial or agentic use cases;
- multilingual datasets;
- documentation improvements;
- interoperability analysis;
- critical review of interpretation boundaries.

### Submit a contribution

- [Submit a contribution — English](https://neomundi.org/en/submit-a-contribution)
- [Proposer une contribution — Français](https://neomundi.org/proposez-une-contribution)
- [NeoMundi contribution and governance framework](https://github.com/neomundi-io/neomundi-ai-observatory/tree/main/governance)

Contributors should:

- state the hypothesis;
- document the corpus;
- document the protocol;
- version the scripts;
- disclose limitations;
- separate evidence from interpretation;
- avoid unsupported universal claims;
- respect protected-data boundaries;
- preserve attribution.

Contributions do not create authority over the programme, the observed systems or NeoMundi’s institutional decisions unless explicitly agreed in writing.

---

## 13. Contribution principle

> Contribute through evidence, methods and critical review.
>
> Open science requires transparency about what is published, what remains protected and why.

---

## 14. Contact

To propose a collaboration or request additional information:

- **Website:** [neomundi.org/en/home](https://neomundi.org/en/home)
- **Contribution form:** [Submit a contribution](https://neomundi.org/en/submit-a-contribution)
- **Email:** [contact@neomundi.org](mailto:contact@neomundi.org)
