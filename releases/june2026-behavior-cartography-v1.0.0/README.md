> **French version available below / Version française disponible plus bas**
> A full French translation of this README is available here: [README_FR.md](README_FR.md).

> **English version available / Version anglaise disponible**
> La version anglaise complète de ce README est disponible ici : [README.md](README.md).


# NeoMundi — June 2026 Behavioral Cartography

## A public exploratory release on observable AI behaviors

NeoMundi is developing a continuous measurement framework for generative AI systems.

The long-term objective is to better observe, document and govern AI behavior during use: not only by evaluating the final answer, but also by studying how outputs vary, converge, drift or trigger additional verification needs.

This June 2026 release is an early public research milestone.

It does not publish a ranking of providers.
It does not assign quality scores to individual models.
It does not claim that one observable regime is intrinsically better than another.

It publishes aggregated behavioral observations only.

---

## 1. Why this research matters

Most AI benchmarks evaluate a final answer.

That is useful, but incomplete.

A generative AI system can:

* produce different formulations when asked the same question several times;
* converge toward recurring textual forms;
* remain highly variable depending on the nature of the question;
* appear stable while still being factually incorrect;
* receive different evaluations depending on the judge used.

NeoMundi explores these additional dimensions as part of a broader program of continuous AI observation.

---

## 2. What NeoMundi is measuring

NeoMundi is progressively qualifying an instrument that separates several layers of observation.

| Observation layer                  | Human question                                                   | Current research focus                                              |
| ---------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------- |
| During generation                  | Does the answer remain under control while it is being produced? | Runtime signals, coherence variations, potential drift and alerts   |
| When the same question is repeated | Does the AI respond in the same way every time?                  | Textual anchoring, convergence, structured variation and dispersion |
| After the answer                   | How should the answer be evaluated?                              | Independent judges, agreement, disagreement and human review        |

These layers must not be confused.

A textually stable answer is not necessarily true.
A variable answer is not necessarily wrong.
A runtime signal is not, by itself, proof of an error.

---

## 3. Two complementary campaigns

This release brings together two distinct experimental perspectives.

### A. Wide TruthfulQA evaluation campaign

A large campaign based on the TruthfulQA corpus was used to study:

* evaluated positive-verdict rates;
* agreement and disagreement between automated judges;
* Cohen’s kappa;
* differences in evaluation depending on the judge.

The public files expose cohort-level summaries only.

No individual provider profile is published.

### B. Targeted repeatability campaign

A second campaign focused on repeated prompts:

```text
12 AI systems
× 8 targeted questions
× 15 repeated generations
= 1,440 observed responses
```

The purpose was to study observable textual behavior when exactly the same question is asked repeatedly.

For each question, several regimes can appear:

| Regime       | Description                                          |
| ------------ | ---------------------------------------------------- |
| `anchor`     | The same textual form returns frequently             |
| `convergent` | Responses remain close despite some variation        |
| `structured` | Several recurring or related forms appear            |
| `dispersed`  | Responses remain highly varied across repeated calls |

These regimes are descriptive.

They are not grades.

---

## 4. What this public release shows

Across the 96 observed system-question combinations:

```text
67 dispersed regimes
15 structured-variation regimes
9 convergent regimes
5 exact textual anchors
```

The main observation is simple:

> When the same question is asked repeatedly, AI systems do not all behave in the same way, and the observable regime changes depending on the question.

Some questions tend to tighten the range of responses.

Others create much more dispersion.

This suggests that AI behavior cannot be reduced to a single static score.

---

## 5. Why the public data is aggregated

This release intentionally publishes behaviors, not providers.

The public files contain:

* no provider names;
* no model names;
* no internal system identifiers;
* no pseudonyms;
* no system-level points;
* no individual profile rows.

For the repeated-question campaign, exact counts by question and regime also remain private.

The public version uses broad qualitative bands:

| Public band | Meaning                   |
| ----------- | ------------------------- |
| `none`      | No observed system        |
| `few`       | A small number of systems |
| `several`   | Several systems           |
| `most`      | Most systems              |
| `all`       | All systems               |

This prevents a reader from reconstructing individual system behavior through subtraction or cross-comparison.

---

## 6. Who judges the judges?

A targeted subset of 108 responses was evaluated independently by two automated judges.

The results were:

```text
108 evaluated responses
103 agreements
5 disagreements
95.4% raw agreement
Cohen’s κ = 0.905
```

This result must be interpreted carefully.

The subset was deliberately targeted and includes representative, contrasted and sometimes weakly discriminating items.

It is not a universal measure of automated-judge reliability.

Its purpose is methodological:

> even AI systems used to evaluate other AI systems are not perfectly interchangeable.

This is why automated judgment should remain auditable and, where necessary, complemented by human review.

---

## 7. Interpretation boundaries

This release supports several observations.

### What can be said

* Repeated prompts can produce distinct observable textual regimes.
* The nature of the question influences the degree of convergence or dispersion.
* Textual stability and factual evaluation are different dimensions.
* Automated judges can disagree.
* Continuous AI observation requires several complementary signals.

### What cannot be said

* A stable answer is necessarily correct.
* A variable answer is necessarily unreliable.
* A textual regime proves semantic equivalence.
* The published data ranks providers.
* The current release provides a final deployment recommendation.
* The present framework is already a fully qualified industry standard.

---

## 8. Current status of the NeoMundi instrument

NeoMundi is currently in an instrument-qualification phase.

The aim is not to overstate conclusions prematurely.

The aim is to progressively clarify:

* which signals are robust;
* which signals are reproducible;
* which signals remain context-dependent;
* which measurements are useful for monitoring;
* which thresholds may eventually support operational decisions;
* which parts of the framework should remain exploratory.

The long-term direction is continuous measurement:

```text
observe
→ qualify
→ compare
→ verify
→ govern
```

---

## 9. June 2026 research directions

The next phase will focus on several questions.

### Repeated-question behavior

* Which questions systematically create convergence?
* Which questions systematically create dispersion?
* Do recurring textual forms persist across time?
* Are observable regimes stable across model updates?

### Judge sensitivity

* Which types of answers create disagreement between judges?
* How should automated evaluation be calibrated?
* When should a human review be triggered?

### Runtime signals

* Which runtime indicators correlate with useful operational warnings?
* Which signals should remain descriptive?
* Which signals may eventually support real-time intervention?

### Longitudinal observation

* How do systems change across releases?
* Can the same protocol be repeated monthly?
* Which changes reflect model evolution, gateway changes or sampling conditions?

---

## 10. Public files

| File                                                 | Purpose                                         |
| ---------------------------------------------------- | ----------------------------------------------- |
| `13_public_measurement_layers.csv`                   | Explains the three observation layers           |
| `13_public_question_behavior_bands.csv`              | Aggregated behavioral bands by question         |
| `13_public_behavior_regime_totals.csv`               | Global distribution of observed regimes         |
| `13_public_wide_truthfulqa_cohort_summary.csv`       | Cohort-level TruthfulQA evaluation summary      |
| `13_public_double_judge_methodological_vignette.csv` | Aggregated double-judge methodological vignette |
| `13_public_storytelling_key_figures.json`            | Public key figures                              |
| `13_public_storytelling_manifest.json`               | Public release manifest                         |

---

## 11. Access to additional data

Some research artifacts remain private because they contain system-level information, internal mappings or detailed outputs.

Researchers, technical teams, institutions or journalists interested in deeper analysis may contact NeoMundi to discuss a possible controlled-access framework.

Access may depend on:

* the intended research purpose;
* confidentiality requirements;
* data minimisation;
* responsible-publication conditions;
* the maturity of the requested dataset.

Contact:

```text
[INSERT CONTACT EMAIL]
```

---

## 12. Open science and contributions

NeoMundi intends to progressively publish:

* reproducible public datasets;
* methodological notes;
* aggregated releases;
* selected public scripts;
* longitudinal observations;
* contribution guidelines.

Feedback is welcome, especially on:

* experimental design;
* behavioral taxonomy;
* judge calibration;
* runtime monitoring;
* reproducibility;
* legal and governance questions.

---

## 13. Final note

This release is not a finished theory.

It is a first public measurement milestone.

The objective is to make AI behavior more observable, more discussable and, over time, more governable.

---

# NeoMundi — Cartographie comportementale des IA — Juin 2026

## Une publication exploratoire sur les comportements observables des IA

NeoMundi développe un cadre de mesure continue des systèmes d’IA générative.

L’objectif à long terme est de mieux observer, documenter et gouverner les comportements des IA en situation d’usage : non seulement en évaluant la réponse finale, mais aussi en étudiant la manière dont les sorties varient, convergent, dérivent ou déclenchent un besoin de vérification supplémentaire.

Cette publication de juin 2026 constitue une première étape publique de recherche.

Elle ne publie pas de classement de fournisseurs.
Elle n’attribue pas de score de qualité à des modèles individuels.
Elle ne prétend pas qu’un régime observable serait intrinsèquement meilleur qu’un autre.

Elle publie uniquement des observations comportementales agrégées.

---

## 1. Pourquoi cette recherche est utile

La plupart des benchmarks d’IA évaluent une réponse finale.

Cette approche est utile, mais incomplète.

Un système d’IA générative peut :

* produire des formulations différentes lorsque la même question lui est posée plusieurs fois ;
* converger vers des formes textuelles récurrentes ;
* rester fortement variable selon la nature de la question ;
* apparaître stable tout en produisant une réponse factuellement incorrecte ;
* recevoir des évaluations différentes selon le juge utilisé.

NeoMundi explore ces dimensions complémentaires dans le cadre d’un programme plus large d’observation continue des IA.

---

## 2. Ce que mesure NeoMundi

NeoMundi qualifie progressivement un instrument distinguant plusieurs couches d’observation.

| Couche d’observation                 | Question humaine                                                     | Axe actuel de recherche                                                 |
| ------------------------------------ | -------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Pendant la génération                | La réponse reste-t-elle sous contrôle pendant qu’elle se construit ? | Signaux runtime, variations de cohérence, dérive potentielle et alertes |
| Lorsque la même question est répétée | L’IA répond-elle toujours sous la même forme ?                       | Ancrage textuel, convergence, variation structurée et dispersion        |
| Après la réponse                     | Comment évaluer la qualité de la sortie ?                            | Juges indépendants, accord, désaccord et relecture humaine              |

Ces couches ne doivent pas être confondues.

Une réponse textuellement stable n’est pas nécessairement vraie.
Une réponse variable n’est pas nécessairement mauvaise.
Un signal runtime ne constitue pas, à lui seul, une preuve d’erreur.

---

## 3. Deux campagnes complémentaires

Cette publication croise deux perspectives expérimentales distinctes.

### A. Campagne large d’évaluation TruthfulQA

Une campagne large fondée sur le corpus TruthfulQA a permis d’étudier :

* les taux de verdict positif évalués ;
* l’accord et le désaccord entre juges automatisés ;
* le coefficient κ de Cohen ;
* les écarts d’évaluation selon le juge utilisé.

Les fichiers publics exposent uniquement des résumés au niveau de la cohorte.

Aucun profil individuel de fournisseur n’est publié.

### B. Campagne ciblée de répétabilité

Une seconde campagne s’est concentrée sur la répétition de prompts :

```text
12 systèmes d’IA
× 8 questions ciblées
× 15 générations répétées
= 1 440 réponses observées
```

L’objectif était d’étudier les comportements textuels observables lorsque la même question est posée plusieurs fois.

Pour chaque question, plusieurs régimes peuvent apparaître :

| Régime       | Description                                              |
| ------------ | -------------------------------------------------------- |
| `anchor`     | Une même forme textuelle revient fréquemment             |
| `convergent` | Les réponses restent proches malgré certaines variations |
| `structured` | Plusieurs formes proches ou récurrentes apparaissent     |
| `dispersed`  | Les réponses restent fortement variées au fil des appels |

Ces régimes sont descriptifs.

Ils ne constituent pas des notes.

---

## 4. Ce que montre cette publication

Sur les 96 couples `système × question` observés :

```text
67 régimes dispersés
15 régimes de variation structurée
9 régimes convergents
5 ancrages textuels exacts
```

L’observation centrale est simple :

> Lorsque la même question est répétée, les systèmes d’IA ne se comportent pas tous de la même manière, et le régime observable varie selon la question posée.

Certaines questions resserrent la gamme des réponses.

D’autres provoquent une dispersion beaucoup plus importante.

Cela suggère qu’un comportement d’IA ne peut pas être résumé par une seule note statique.

---

## 5. Pourquoi les données publiques sont agrégées

Cette publication expose volontairement des comportements, pas des fournisseurs.

Les fichiers publics ne contiennent :

* aucun nom de fournisseur ;
* aucun nom de modèle ;
* aucun identifiant interne de système ;
* aucun pseudonyme ;
* aucun point individuel ;
* aucune ligne de profil individuel.

Pour la campagne de répétabilité, les comptages exacts par question et par régime restent également privés.

La version publique utilise des bandes qualitatives larges :

| Bande publique | Signification           |
| -------------- | ----------------------- |
| `none`         | Aucun système observé   |
| `few`          | Quelques systèmes       |
| `several`      | Plusieurs systèmes      |
| `most`         | La plupart des systèmes |
| `all`          | Tous les systèmes       |

Cette règle évite de reconstruire le comportement individuel d’un système par soustraction ou comparaison croisée.

---

## 6. Qui juge les juges ?

Un sous-panel ciblé de 108 réponses a été évalué indépendamment par deux juges automatisés.

Les résultats sont les suivants :

```text
108 réponses évaluées
103 accords
5 désaccords
95,4 % d’accord brut
κ de Cohen = 0,905
```

Ce résultat doit être interprété avec prudence.

Le sous-panel a été construit de manière ciblée. Il inclut des réponses représentatives, contrastées et parfois peu discriminantes.

Il ne constitue pas une mesure universelle de la fiabilité des juges automatisés.

Sa valeur est méthodologique :

> Même les systèmes d’IA utilisés pour juger d’autres systèmes d’IA ne sont pas parfaitement interchangeables.

Le jugement automatisé doit donc rester auditable et, lorsque cela est nécessaire, être complété par une relecture humaine.

---

## 7. Limites d’interprétation

Cette publication permet plusieurs observations.

### Ce que l’on peut dire

* La répétition d’une même question peut produire différents régimes textuels observables.
* La nature de la question influence le degré de convergence ou de dispersion.
* La stabilité textuelle et l’évaluation factuelle sont deux dimensions distinctes.
* Les juges automatisés peuvent être en désaccord.
* L’observation continue des IA nécessite plusieurs signaux complémentaires.

### Ce que l’on ne peut pas dire

* Une réponse stable est nécessairement correcte.
* Une réponse variable est nécessairement peu fiable.
* Un régime textuel prouve une équivalence sémantique.
* Les données publiées permettent de classer les fournisseurs.
* La publication actuelle fournit une recommandation définitive de déploiement.
* Le cadre présenté constitue déjà un standard industriel entièrement qualifié.

---

## 8. Statut actuel de l’instrument NeoMundi

NeoMundi se trouve actuellement dans une phase de qualification de son instrument.

L’objectif n’est pas de surinterpréter prématurément les résultats.

L’objectif est de préciser progressivement :

* quels signaux sont robustes ;
* quels signaux sont reproductibles ;
* quels signaux restent dépendants du contexte ;
* quelles mesures sont utiles pour la supervision ;
* quels seuils pourraient, à terme, soutenir une décision opérationnelle ;
* quelles dimensions doivent rester exploratoires.

La direction de long terme est celle d’une mesure continue :

```text
observer
→ qualifier
→ comparer
→ vérifier
→ gouverner
```

---

## 9. Axes de recherche pour juin 2026

La prochaine phase portera sur plusieurs questions.

### Comportements sous répétition

* Quelles questions provoquent régulièrement de la convergence ?
* Quelles questions provoquent régulièrement de la dispersion ?
* Les formes textuelles récurrentes persistent-elles dans le temps ?
* Les régimes observables résistent-ils aux mises à jour de modèles ?

### Sensibilité aux juges

* Quels types de réponses provoquent des désaccords entre juges ?
* Comment calibrer l’évaluation automatisée ?
* Dans quels cas déclencher une relecture humaine ?

### Signaux runtime

* Quels indicateurs runtime sont corrélés à des alertes opérationnelles utiles ?
* Quels signaux doivent rester descriptifs ?
* Quels signaux pourraient, à terme, permettre une intervention en temps réel ?

### Observation longitudinale

* Comment les systèmes évoluent-ils d’une version à l’autre ?
* Peut-on répéter ce protocole chaque mois ?
* Quels changements reflètent une évolution du modèle, du gateway ou des paramètres d’échantillonnage ?

---

## 10. Fichiers publics

| Fichier                                              | Rôle                                                       |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| `13_public_measurement_layers.csv`                   | Présente les trois couches d’observation                   |
| `13_public_question_behavior_bands.csv`              | Présente les bandes comportementales agrégées par question |
| `13_public_behavior_regime_totals.csv`               | Présente la distribution globale des régimes observés      |
| `13_public_wide_truthfulqa_cohort_summary.csv`       | Présente le résumé agrégé de la cohorte TruthfulQA         |
| `13_public_double_judge_methodological_vignette.csv` | Présente l’encadré méthodologique sur le double jugement   |
| `13_public_storytelling_key_figures.json`            | Rassemble les chiffres clés publics                        |
| `13_public_storytelling_manifest.json`               | Décrit le manifest public de la release                    |

---

## 11. Accès à des données complémentaires

Certains artefacts de recherche restent privés parce qu’ils contiennent des informations au niveau des systèmes, des mappings internes ou des sorties détaillées.

Les chercheurs, équipes techniques, institutions ou journalistes souhaitant approfondir l’analyse peuvent contacter NeoMundi afin d’étudier un éventuel cadre d’accès contrôlé.

Cet accès pourra dépendre :

* de l’objectif de recherche ;
* des exigences de confidentialité ;
* du principe de minimisation des données ;
* des conditions de publication responsable ;
* du niveau de maturité du dataset concerné.

Contact :

```text
[INSÉRER L’ADRESSE EMAIL DE CONTACT]
```

---

## 12. Open science et contributions

NeoMundi prévoit de publier progressivement :

* des datasets publics reproductibles ;
* des notes méthodologiques ;
* des releases agrégées ;
* certains scripts publics ;
* des observations longitudinales ;
* des lignes directrices pour les contributions.

Les retours sont particulièrement bienvenus sur :

* le design expérimental ;
* la taxonomie comportementale ;
* la calibration des juges ;
* la supervision runtime ;
* la reproductibilité ;
* les enjeux juridiques et de gouvernance.

---

## 13. Note finale

Cette publication ne constitue pas une théorie achevée.

Elle représente une première étape publique de mesure.

L’objectif est de rendre les comportements des IA plus observables, plus discutables et, progressivement, plus gouvernables.

