# NeoMundi — Open Science, Source Corpus and Contributions

[English README](./README.md) · [README français](./README_FR.md)
[English methodology](./Methodology_EN.md) · [Méthodologie française](./Methodologie_FR.md)
[English usage guide](./USAGE_EN.md) · [Guide d’utilisation en français](./USAGE_FR.md)

---

# English

## From benchmark scores to observable AI profiles

A leaderboard can answer one immediate question:

> Which system ranks first?

But it can hide more important questions:

* Do two judges evaluate the same answer in the same way?
* Are disagreements random or structurally concentrated?
* Does runtime stability remain visible when factual judgments diverge?
* Can the same AI system exhibit different behavioral signatures across repeated panels?
* What information disappears when several dimensions are compressed into one score?

NeoMundi publishes multidimensional, pseudonymous profiles to make these questions observable.

The objective is not to replace one leaderboard with another.

The objective is to expose a reproducible map of:

* factual-evaluation views;
* inter-judge calibration;
* runtime behavioral signals;
* disagreement zones;
* repeatability;
* methodological uncertainty.

## Open source corpus

This repository builds on the TruthfulQA benchmark introduced by Stephanie Lin, Jacob Hilton and Owain Evans.

Original paper:

```text
TruthfulQA: Measuring How Models Mimic Human Falsehoods
https://arxiv.org/abs/2109.07958
```

ACL Anthology publication:

```text
https://aclanthology.org/2022.acl-long.229/
```

Official source repository:

```text
https://github.com/sylinrl/TruthfulQA
```

Official public list of benchmark questions and reference answers:

```text
https://github.com/sylinrl/TruthfulQA/blob/main/TruthfulQA.csv
```

The original benchmark paper describes 817 questions spanning 38 categories, including health, law, finance and politics.

The official repository maintains the current source questions and reference answers and documents later benchmark updates.

## NeoMundi public release

The current frozen NeoMundi release is available in:

```text
releases/truthfulqa-profiles-v1.0.0/
```

It publishes:

* 12 stable pseudonymous profiles;
* multidimensional factual-evaluation summaries;
* runtime behavioral summaries;
* inter-judge agreement metrics;
* a public data dictionary;
* a release manifest;
* SHA-256 checksums.

It does not publish:

* provider names;
* model names;
* rankings;
* ratings;
* composite scores;
* raw answers;
* profile-linked question-level traces;
* judge rationales.

## Current methodological signal

The current release documents:

```text
12 pseudonymous profiles
9,087 comparable judgment pairs
81.42% observed inter-judge agreement
pooled Cohen kappa = 0.6342
1,688 disagreements
```

Among the disagreements, the directional imbalance is systematic:

```text
Judge A negative / Judge B positive: 1,491
Judge A positive / Judge B negative:   197
```

This result does not establish an absolute reference judge.

It shows that factual evaluation itself must be observed as a calibrated, traceable layer.

## Why this matters

A model-selection decision cannot rely on a single public score.

A serious diagnostic may need to separate:

* factual evaluation;
* judge calibration;
* runtime stability;
* repeatability;
* domain-specific risk;
* deployment context;
* cost and efficiency constraints.

The public release intentionally exposes observable profiles rather than universal recommendations.

## Open questions

The following questions remain open:

1. Does the inter-judge asymmetry persist with a third independent judge?
2. Which disagreement zones remain stable across repeated judging runs?
3. How much intra-judge variability exists at controlled temperature?
4. Which high-disagreement questions require human adjudication?
5. Do runtime behavioral signatures remain stable across repeated panels?
6. Can a reduced 150-question panel reproduce the behavioral signal of a 450-question panel?
7. Which runtime dimensions become more informative in legal, medical or agentic contexts?
8. How should multidimensional AI profiles be represented without recreating a hidden leaderboard?

## Planned extensions

Future public work includes:

* a third independent judge;
* intra-judge repeatability analysis;
* a stratified human-adjudication panel;
* behavioral cartography on repeated-run panels;
* domain-specific panels;
* multilingual extensions;
* contributor-proposed analyses.

## Invitation to contribute

Researchers, engineers, auditors, domain experts and AI builders are invited to contribute.

Possible contributions include:

* methodological review;
* reproducibility testing;
* additional public panels;
* third-judge experiments;
* human-adjudication protocols;
* statistical analysis;
* data visualization;
* legaltech, medical-AI or autonomous-agent use cases;
* multilingual datasets;
* documentation improvements.

To contribute:

* open a GitHub issue;
* propose a pull request;
* describe the hypothesis;
* document the corpus;
* document the protocol;
* version the scripts;
* disclose limitations;
* avoid unsupported universal claims.

## Contribution principle

> Contribute evidence, not hype.
> Publish observable profiles, not rankings.

---

## Contact

To contribute, propose a collaboration or request additional information:

* Website: [neomundi.org](https://neomundi.org)
* Email: `contact@neomundi.org`

---

# Français

## Des scores de benchmark aux profils IA observables

Un classement répond immédiatement à une question :

> Quel système arrive en tête ?

Mais il peut masquer des questions plus importantes :

* Deux juges évaluent-ils la même réponse de la même manière ?
* Les désaccords sont-ils aléatoires ou concentrés dans certaines zones ?
* La stabilité runtime reste-t-elle observable lorsque les jugements factuels divergent ?
* Un même système IA présente-t-il des signatures différentes selon les panels répétés ?
* Quelles informations disparaissent lorsque plusieurs dimensions sont compressées dans une note unique ?

NeoMundi publie des profils pseudonymisés et multidimensionnels afin de rendre ces questions observables.

L’objectif n’est pas de remplacer un classement par un autre.

L’objectif est d’exposer une cartographie reproductible :

* des lectures factuelles ;
* de la calibration inter-juges ;
* des signaux comportementaux runtime ;
* des zones de divergence ;
* de la répétabilité ;
* de l’incertitude méthodologique.

## Corpus open source

Ce dépôt s’appuie sur le benchmark TruthfulQA introduit par Stephanie Lin, Jacob Hilton et Owain Evans.

Article original :

```text
TruthfulQA: Measuring How Models Mimic Human Falsehoods
https://arxiv.org/abs/2109.07958
```

Publication ACL Anthology :

```text
https://aclanthology.org/2022.acl-long.229/
```

Dépôt officiel :

```text
https://github.com/sylinrl/TruthfulQA
```

Liste publique officielle des questions et réponses de référence :

```text
https://github.com/sylinrl/TruthfulQA/blob/main/TruthfulQA.csv
```

L’article original décrit 817 questions couvrant 38 catégories, dont la santé, le droit, la finance et la politique.

Le dépôt officiel maintient la version courante des questions et réponses de référence et documente les évolutions ultérieures du benchmark.

## Release publique NeoMundi

La release NeoMundi figée est disponible ici :

```text
releases/truthfulqa-profiles-v1.0.0/
```

Elle publie :

* 12 profils pseudonymisés stables ;
* des synthèses multidimensionnelles d’évaluation factuelle ;
* des synthèses comportementales runtime ;
* des métriques d’accord inter-juges ;
* un dictionnaire public ;
* un manifeste ;
* des checksums SHA-256.

Elle ne publie pas :

* les noms des providers ;
* les noms des modèles ;
* des classements ;
* des ratings ;
* des scores composites ;
* les réponses brutes ;
* des traces individuelles reliées aux profils ;
* les justifications textuelles des juges.

## Signal méthodologique actuel

La release documente :

```text
12 profils pseudonymisés
9 087 paires de jugements comparables
81,42 % d’accord inter-juges observé
Cohen kappa poolé = 0,6342
1 688 désaccords
```

Parmi les désaccords, l’asymétrie directionnelle est systématique :

```text
Juge A négatif / Juge B positif : 1 491
Juge A positif / Juge B négatif :   197
```

Ce résultat ne permet pas de désigner un juge comme référence absolue.

Il montre que l’évaluation factuelle doit elle-même être observée comme une couche calibrée et traçable.

## Pourquoi c’est important

Une décision d’achat ou de déploiement ne peut pas reposer uniquement sur une note publique.

Un diagnostic sérieux peut nécessiter de séparer :

* l’évaluation factuelle ;
* la calibration des juges ;
* la stabilité runtime ;
* la répétabilité ;
* les risques métier ;
* le contexte de déploiement ;
* les contraintes de coût et d’efficience.

La release publique expose volontairement des profils observables plutôt que des recommandations universelles.

## Questions ouvertes

Les questions suivantes restent ouvertes :

1. L’asymétrie inter-juges persiste-t-elle avec un troisième juge indépendant ?
2. Quelles zones de désaccord restent stables entre plusieurs répétitions du jugement ?
3. Quelle est la variabilité intra-juge à température contrôlée ?
4. Quelles questions à forte divergence nécessitent une adjudication humaine ?
5. Les signatures comportementales runtime persistent-elles sur des panels répétés ?
6. Un panel réduit de 150 questions reproduit-il le signal comportemental d’un panel de 450 questions ?
7. Quelles dimensions runtime deviennent plus informatives dans des contextes juridiques, médicaux ou agentiques ?
8. Comment représenter des profils IA multidimensionnels sans recréer implicitement un classement ?

## Extensions prévues

Les prochains travaux publics incluent :

* un troisième juge indépendant ;
* une analyse de répétabilité intra-juge ;
* un panel stratifié d’adjudication humaine ;
* une cartographie comportementale sur panels répétés ;
* des panels métier ;
* des extensions multilingues ;
* des analyses proposées par des contributeurs.

## Invitation à contribuer

Chercheurs, ingénieurs, auditeurs, experts métier et concepteurs IA sont invités à contribuer.

Les contributions peuvent porter sur :

* la revue méthodologique ;
* les tests de reproductibilité ;
* de nouveaux panels publics ;
* l’ajout d’un troisième juge ;
* les protocoles d’adjudication humaine ;
* l’analyse statistique ;
* la visualisation des données ;
* les cas d’usage legaltech, IA médicale ou agents autonomes ;
* les jeux de données multilingues ;
* l’amélioration de la documentation.

Pour contribuer :

* ouvrir une issue GitHub ;
* proposer une pull request ;
* expliciter l’hypothèse ;
* documenter le corpus ;
* documenter le protocole ;
* versionner les scripts ;
* exposer les limites ;
* éviter toute affirmation universelle insuffisamment étayée.

## Principe de contribution

> Contribuer des preuves, pas du bruit.
> Publier des profils observables, pas des classements.

---

## Contact

Pour contribuer, proposer une collaboration ou demander des informations complémentaires :

* Site : [neomundi.org](https://neomundi.org)
* Email : `contact@neomundi.org`

