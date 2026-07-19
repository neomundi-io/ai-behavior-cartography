# Cartographie du comportement des IA NeoMundi

🌐 **Langue :** [English](./README.md) · [Français](./README_FR.md)

🌍 **NeoMundi :** [Site français](https://neomundi.org/) · [English website](https://neomundi.org/en/home)

La **Cartographie du comportement des IA NeoMundi** est un programme public et reproductible de mesure comparative conçu pour observer comment les systèmes d’IA générative se comportent sur des corpus factuels communs, lors d’exécutions répétées et dans des conditions runtime documentées.

Elle ne classe ni les fournisseurs ni les modèles.

Elle publie des observations désidentifiées, comparables et méthodologiquement séparées afin de rendre visibles les différences de stabilité, de factualité, de variation sémantique, de cohérence, de latence et de régimes comportementaux.

> Un benchmark produit un score.  
> NeoMundi cartographie des propriétés comportementales distinctes sans les réduire à un verdict unique.

---

## Objectif du programme

La Cartographie vise à répondre à plusieurs questions complémentaires :

- Comment les systèmes d’IA observés se comportent-ils dans des conditions comparables ?
- Quel est le niveau de stabilité de leurs réponses lors d’exécutions répétées ?
- Comment la stabilité observée se rapporte-t-elle à la factualité évaluée par des juges externes ?
- Dans quelles situations les juges de factualité indépendants sont-ils d’accord ou en désaccord ?
- Quels systèmes présentent davantage de variation sémantique ou de changements de régime ?
- Comment les signaux runtime évoluent-ils entre des vagues répétées ?
- Quelles propriétés peuvent être mesurées séparément sans produire un score universel de qualité ?

La Cartographie considère le comportement des IA comme un objet de mesure multidimensionnel.

Elle ne suppose ni que la stabilité implique la vérité, ni que la factualité implique la stabilité, ni qu’un score agrégé unique puisse représenter l’ensemble du comportement d’un système d’IA.

---

## Structure du programme

Le dépôt contient six composantes principales :

- **Cartographie jugée du comportement des IA** — observation comparative sur un corpus complet d’évaluation factuelle ;
- **Cartographie de stabilité runtime** — observation runtime répétée sur plusieurs vagues ;
- **Releases mensuelles** — cycles publics de publication datés ;
- **Méthodologie** — définitions actives des protocoles et limites d’interprétation ;
- **Guides d’utilisation** — instructions pour reproduire ou examiner les workflows publics ;
- **Cadre de science ouverte** — principes de contribution, de revue et de réutilisation publique.

---

## Structure méthodologique de juillet 2026

La Cartographie de juillet 2026 repose sur deux protocoles publics indépendants.

Ces protocoles répondent à des questions analytiques différentes et restent séparés.

---

## Protocole 1 — Cartographie jugée du comportement des IA

Le premier protocole repose sur :

```text
12 profils d’IA désidentifiés
× 790 questions TruthfulQA
= 9 480 réponses sources
```

Le protocole comprend :

- 12 profils d’IA désidentifiés ;
- le corpus complet de 790 questions TruthfulQA ;
- 9 480 réponses sources ;
- des mesures de stabilité observée ;
- une évaluation de factualité par un juge fondé sur OpenAI ;
- une évaluation de factualité par un juge fondé sur Mistral ;
- l’accord inter-juges ;
- le kappa de Cohen comme indicateur secondaire d’accord ;
- la conservation séparée des décisions de chaque juge.

Son objectif est de comparer la stabilité observée des réponses avec leur factualité évaluée extérieurement sur un large corpus factuel.

Les deux juges de factualité ne sont pas fusionnés en un score absolu unique.

La séparation de leurs résultats rend leurs désaccords visibles et préserve les limites de l’évaluation automatisée de la factualité.

Répertoire de release :

```text
releases/july2026-behavior-cartography/judged-cartography-12x790/
```

---

## Protocole 2 — Cartographie de stabilité runtime

Le second protocole repose sur :

```text
12 profils d’IA désidentifiés
× 3 vagues répétées
× 150 questions équilibrées
= 5 400 exécutions
```

Le protocole comprend :

- 12 profils d’IA désidentifiés ;
- 3 vagues d’exécution répétées ;
- un panel équilibré de 150 questions ;
- 5 400 exécutions ;
- des mesures de stabilité ;
- des signaux de variation sémantique ;
- des indicateurs de cohérence ;
- des observations de latence ;
- une classification des régimes comportementaux ;
- des comparaisons entre vagues répétées.

Son objectif est d’observer la variabilité runtime et les changements de régime comportemental dans des conditions d’exécution répétées et documentées.

Ce protocole porte sur le comportement répété plutôt que sur un jugement externe de factualité.

Répertoire de release :

```text
releases/july2026-behavior-cartography/runtime-stability-12x3x150/
```

---

## Pourquoi les protocoles restent séparés

Les deux protocoles sont complémentaires, mais ils ne sont pas interchangeables.

Le protocole jugé évalue le comportement sur un large corpus factuel et compare la stabilité observée à deux évaluations indépendantes de factualité.

Le protocole runtime évalue la manière dont le comportement varie entre des exécutions et des vagues répétées.

Ils répondent donc à des questions différentes :

| Protocole | Question principale |
|---|---|
| Cartographie jugée — `12 × 790` | Comment la stabilité et la factualité jugée se comparent-elles sur un large corpus factuel ? |
| Cartographie runtime — `12 × 3 × 150` | Comment le comportement varie-t-il dans des conditions runtime répétées ? |

Les protocoles ne sont pas fusionnés en un score universel de qualité.

Un système peut paraître stable tout en produisant des réponses factuellement faibles.

Un système peut paraître variable tout en produisant des réponses factuellement acceptables.

Un juge peut être en désaccord avec un autre sans que le résultat de l’un ou de l’autre constitue une garantie absolue de vérité.

---

## Cycle de publication mensuel

La Cartographie est conçue comme un programme récurrent d’observation mensuelle.

Chaque cycle mensuel peut inclure un ou plusieurs protocoles selon :

- la disponibilité des données ;
- la maturité méthodologique ;
- la qualité de la campagne ;
- la couverture ;
- le statut de validation ;
- l’état de préparation de la publication.

Les releases mensuelles sont publiées dans des répertoires datés et conservent leurs propres :

- versions de protocole ;
- périmètres ;
- métriques ;
- limites ;
- manifestes ;
- frontières de publication des données ;
- règles d’interprétation.

Des comparaisons longitudinales pourront être introduites à mesure que le nombre de releases mensuelles compatibles augmentera.

Aucune comparaison entre mois ne doit être réalisée sans vérifier au préalable la compatibilité des protocoles, des jeux de données, des règles de scoring et des conditions de publication.

---

## Données et preuves publiques

Selon le protocole et la release, le dépôt public peut exposer :

- des résultats agrégés par profil désidentifié ;
- des résultats agrégés par question ou famille de questions ;
- des mesures de stabilité observée ;
- les résultats de factualité de chaque juge ;
- l’accord inter-juges ;
- le kappa de Cohen ;
- des indicateurs de variation sémantique ;
- des indicateurs de cohérence ;
- des synthèses de latence ;
- des distributions de régimes comportementaux ;
- des informations de couverture et de complétude ;
- les définitions des métriques ;
- les documents méthodologiques ;
- les versions des protocoles ;
- les manifestes de release ;
- les empreintes d’intégrité ;
- les rapports analytiques ;
- les cartographies visuelles ;
- les limites documentées.

Les preuves publiques sont conçues pour permettre :

- des contrôles de cohérence interne ;
- la revue méthodologique ;
- l’analyse indépendante ;
- la comparaison entre profils ;
- la comparaison entre releases ;
- la discussion publique des propriétés comportementales observées.

---

## Données protégées et restreintes

La transparence publique n’impose pas la divulgation incontrôlée des actifs opérationnels qui protègent l’intégrité, la sécurité et la continuité du programme de mesure.

Selon le protocole, la frontière de mesure protégée peut inclure :

- l’identité des fournisseurs et des modèles ;
- le registre privé de correspondance des profils ;
- les prompts complets lorsque leur publication compromettrait le protocole ;
- les réponses brutes complètes ;
- les identifiants de requête et de trace ;
- les payloads API bruts ;
- les horodatages précis des exécutions ;
- les clés API et identifiants d’infrastructure ;
- les données détaillées et non agrégées de tokens et de coûts ;
- les diagnostics internes ;
- les éléments de débogage ;
- les détails de configuration des juges ;
- les exports privés des campagnes ;
- les versions internes des pipelines ;
- la logique de calcul propriétaire ;
- les artefacts pouvant permettre la réidentification des profils ;
- les résultats non publiés ;
- les signaux expérimentaux non encore qualifiés pour une publication publique ;
- les notes de revue et les éléments internes de validation.

Cette séparation permet l’examen public tout en protégeant la continuité opérationnelle, la confidentialité, l’intégrité de la recherche et la désidentification.

---

## Désidentification

Les profils publics utilisent des identifiants opaques stables au format :

```text
PROFILE-XXXXXX
```

Ces identifiants ne sont pas dérivés :

- des noms de fournisseurs ;
- des noms de modèles ;
- de l’ordre alphabétique ;
- de la performance ;
- de la factualité ;
- de la stabilité ;
- du score ;
- du classement.

La correspondance privée entre les profils publics et les systèmes observés est conservée séparément.

Les releases sont **désidentifiées**. Elles ne sont pas présentées comme irréversiblement anonymes.

Le risque résiduel de réidentification est traité comme une limite de publication.

---

## Familles de signaux observés

Selon le protocole et la couverture disponible, la Cartographie peut publier ou documenter :

- la stabilité ;
- la variation sémantique ;
- la cohérence ;
- l’évaluation de factualité ;
- l’accord inter-juges ;
- le kappa de Cohen ;
- les régimes comportementaux ;
- la variation entre vagues ;
- la latence ;
- la couverture et la complétude ;
- les indicateurs de coûts et de consommation de tokens lorsqu’ils sont disponibles ;
- `delta_g`, publié comme signal avancé observable de variation runtime.

Aucun indicateur individuel ne doit être interprété isolément comme une évaluation complète de la qualité, de la véracité, de la sécurité, de la conformité ou de la gouvernabilité.

---

## Doctrine d’interprétation

La Cartographie suit une règle fondamentale :

> Un signal est une observation qui exige une interprétation, et non un verdict.

Une différence observée n’établit pas, à elle seule :

- la supériorité d’un système sur un autre ;
- une mise à jour du modèle côté fournisseur ;
- une explication causale ;
- un niveau de sécurité ;
- la conformité réglementaire ;
- l’adéquation au déploiement ;
- la véracité dans tous les domaines ;
- la qualité globale ;
- la gouvernabilité dans un contexte opérationnel donné.

La formulation appropriée est :

> Une différence comportementale a été observée dans les conditions du protocole.

L’attribution causale exige des preuves complémentaires.

---

## Limites de reproductibilité

Le dépôt public est conçu pour permettre l’examen transparent :

- des méthodes ;
- de la structure des protocoles ;
- des métriques publiées ;
- des données agrégées ;
- de la couverture ;
- des manifestes ;
- des informations d’intégrité ;
- des limites analytiques.

La reproduction complète depuis les sources peut nécessiter l’accès :

- aux exports protégés des campagnes ;
- à la configuration privée de l’infrastructure ;
- aux prompts restreints ;
- aux paramètres privés des juges ;
- aux traces d’exécution non publiques ;
- aux artefacts internes de validation.

Chaque release documente ses propres limites de reproductibilité.

La reproductibilité publique signifie que les artefacts publiés peuvent être examinés, vérifiés et analysés dans les limites explicitement définies par le programme.

---

## Ce que ce programme n’est pas

La Cartographie du comportement des IA NeoMundi n’est pas :

- un classement de fournisseurs ;
- un leaderboard de modèles ;
- un score universel de benchmark ;
- une certification de sécurité ;
- une garantie d’exactitude factuelle ;
- une détermination juridique ou réglementaire ;
- une autorisation de déploiement ;
- un substitut à la revue humaine ;
- un substitut à une validation métier ;
- un substitut à la gouvernance runtime.

Il s’agit d’un instrument métrologique public destiné à cartographier des propriétés distinctes du comportement des IA dans des conditions documentées.

---

## Principes scientifiques

Le programme suit sept principes :

1. **Mesurer avant d’interpréter.**
2. **Maintenir séparées les propriétés distinctes.**
3. **Répéter avant de généraliser.**
4. **Ne jamais confondre stabilité et vérité.**
5. **Préserver les désaccords entre juges plutôt que les dissimuler.**
6. **Distinguer observation, interprétation et attribution causale.**
7. **Traiter chaque signal comme un élément de preuve, et non comme un verdict.**

---

## Navigation du dépôt

| Ressource | English | Français |
|---|---|---|
| Présentation du programme | [README.md](./README.md) | [README_FR.md](./README_FR.md) |
| Méthodologie | [Methodology_EN.md](./Methodology_EN.md) | [Methodologie_FR.md](./Methodologie_FR.md) |
| Guide d’utilisation | [USAGE_EN.md](./USAGE_EN.md) | [USAGE_FR.md](./USAGE_FR.md) |
| Science ouverte et contributions | [OPEN_SCIENCE.md](./OPEN_SCIENCE.md) | [OPEN_SCIENCE.md](./OPEN_SCIENCE.md) |
| Releases mensuelles | [releases/](./releases/) | [releases/](./releases/) |
| Scripts | [scripts/](./scripts/) | [scripts/](./scripts/) |

---

## Programmes NeoMundi associés

- [Observatoire IA NeoMundi](https://github.com/neomundi-io/neomundi-ai-observatory)
- [NeoMundi Weekly Barometer](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer)
- [Site officiel NeoMundi — Français](https://neomundi.org/)
- [Site officiel NeoMundi — English](https://neomundi.org/en/home)
- [De l’observabilité des IA à la métrologie de gouvernance](https://doi.org/10.5281/zenodo.21250268)
- [Cadre théorique — Loi E](https://doi.org/10.5281/zenodo.19385052)

---

## Science ouverte et contributions

Le dépôt soutient la revue méthodologique, l’analyse indépendante et la contribution documentée.

Voir :

- [Science ouverte et contributions](./OPEN_SCIENCE.md)
- [Cadre de contribution de l’Observatoire IA NeoMundi](https://github.com/neomundi-io/neomundi-ai-observatory/tree/main/governance)

Les contributions peuvent porter sur :

- la méthodologie ;
- la revue des protocoles ;
- l’analyse de données ;
- l’évaluation de factualité ;
- la reproductibilité ;
- la visualisation ;
- la rédaction scientifique ;
- la traduction ;
- la gouvernance ;
- l’interopérabilité ;
- l’interprétation sectorielle.

Les contributions ne créent aucune autorité sur le programme, les systèmes observés ou les décisions institutionnelles de NeoMundi, sauf accord écrit explicite.

---

## Licence

Ce dépôt utilise la [licence Apache 2.0](LICENSE).

Certains jeux de données, rapports, scripts, contributions externes ou artefacts de release peuvent comporter des mentions complémentaires lorsque cela est nécessaire.

---

**Cartographie du comportement des IA NeoMundi**  
*Mesure comparative sans classement universel.*
