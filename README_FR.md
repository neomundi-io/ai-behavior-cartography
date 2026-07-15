- [English README](./README.md)
- [README français](./README_FR.md)
- [English methodology](./Methodology_EN.md)
- [Méthodologie française](./Methodologie_FR.md)
- [English usage guide](./USAGE_EN.md)
- [Guide d’utilisation en français](./USAGE_FR.md)
- [Open science and contributions](./OPEN_SCIENCE.md)

# Cartographie des comportements des IA — NeoMundi

NeoMundi développe un cadre public et reproductible permettant d’observer le comportement des systèmes d’intelligence artificielle générative à partir de corpus d’évaluation factuelle, d’exécutions répétées et de signaux runtime.

Ce dépôt documente la qualification progressive de cet instrument de mesure.

Il publie des observations comportementales désidentifiées afin de rendre les systèmes d’IA plus observables, auditables et gouvernables dans le temps.

L’objectif n’est pas de classer les fournisseurs ni de désigner un modèle comme universellement supérieur.

L’objectif est de mesurer séparément différentes propriétés du comportement des IA, sans les réduire à un score unique.

## Contenu de ce dépôt

Ce dépôt rassemble actuellement plusieurs publications publiques complémentaires :

- une cartographie comportementale jugée reposant sur l’intégralité du corpus TruthfulQA de 790 questions ;
- une cartographie de stabilité runtime reposant sur trois vagues d’exécution répétées d’un panel équilibré de 150 questions ;
- une documentation méthodologique sur l’évaluation de la factualité, l’accord entre juges, la stabilité runtime, la variation sémantique et l’observation longitudinale ;
- des artefacts publics de désidentification et de contrôle des publications.

Chaque publication possède son propre protocole, son propre objectif analytique et ses propres limites.

Les protocoles sont publiés séparément et ne sont pas agrégés dans un score universel de qualité.

## Structure méthodologique actuelle

La cartographie de juillet 2026 repose sur deux protocoles publics indépendants.

### 1. Cartographie jugée des comportements des IA — 12 × 790

Ce protocole comprend :

- 12 profils d’IA désidentifiés ;
- 790 questions TruthfulQA par profil ;
- 9 480 réponses sources ;
- des mesures de stabilité observée ;
- une évaluation de la factualité par un juge fondé sur OpenAI ;
- une évaluation de la factualité par un juge fondé sur Mistral ;
- le taux d’accord entre les juges et le kappa de Cohen.

Son objectif est de comparer la stabilité observée et la factualité évaluée par des juges externes sur l’ensemble d’un corpus d’évaluation factuelle.

Les résultats des deux juges de factualité sont conservés séparément.

Leurs décisions ne sont pas fusionnées dans un score unique présenté comme une mesure absolue de factualité.

Répertoire de publication :

```text
releases/july2026-behavior-cartography/judged-cartography-12x790/
