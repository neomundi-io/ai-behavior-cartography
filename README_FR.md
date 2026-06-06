# NeoMundi — Cartographie des profils TruthfulQA

- [English README](./README.md)
- [README français](./README_FR.md)
- [English methodology](./Methodology_EN.md)
- [Méthodologie française](./Methodologie_FR.md)
- [English usage guide](./USAGE_EN.md)
- [Guide d’utilisation en français](./USAGE_FR.md)
- [Open science and contributions](./OPEN_SCIENCE.md)

## Objectif

Ce dépôt documente une cartographie publique, reproductible et multidimensionnelle de profils IA pseudonymisés construits à partir :

* d’un corpus d’évaluation factuelle TruthfulQA ;
* d’une validation par double jugement ;
* de signaux comportementaux runtime séparés.

L’objectif n’est pas de publier un classement universel des modèles.

L’objectif est d’exposer des profils observables, auditables et reproductibles sans réduire le comportement des IA à une note unique.

## Ce que ce dépôt ne publie pas

Ce dépôt ne publie pas :

* les noms des providers ;
* les noms des modèles ;
* des classements ;
* des ratings ;
* des scores composites ;
* les réponses brutes ;
* les traces individuelles par question ;
* les justifications textuelles des juges.

## Release publique

Release figée actuelle :

```text
releases/truthfulqa-profiles-v1.0.0/
```

Elle contient :

* les profils pseudonymisés ;
* les profils runtime ;
* les métriques de validation méthodologique ;
* le dictionnaire public des données ;
* la checklist de publication ;
* le manifeste de release ;
* les checksums SHA-256.

## Principes méthodologiques

La méthodologie publique conserve séparées les couches suivantes :

1. évaluation factuelle ;
2. calibration inter-juges ;
3. signaux comportementaux runtime ;
4. répétabilité ;
5. profils publics pseudonymisés.

Aucun verdict binaire consolidé n’est traité comme une vérité absolue.

Les signaux runtime ne sont pas fusionnés dans un score universel de qualité.

## Scripts de validation

Les scripts reproductibles sont disponibles dans :

```text
scripts/validation/
```

Ils couvrent :

* l’audit de l’inventaire du corpus ;
* l’analyse de l’accord OpenAI ↔ Mistral ;
* l’analyse de la structure des désaccords.

## Script de publication

Le script d’export public conservateur est disponible ici :

```text
scripts/publication/export_public_profiles.py
```

Il :

* applique des identifiants pseudonymisés stables ;
* sépare les métadonnées privées des artefacts publics ;
* bloque les fuites de noms de providers et de modèles ;
* refuse les champs de classement, de rating et de score composite ;
* génère un manifeste, un dictionnaire public et des checksums SHA-256 ;
* exige une revue humaine avant publication.

## Résultats méthodologiques actuels

La release actuelle documente :

* 12 profils pseudonymisés ;
* 9 087 paires de jugements comparables ;
* 81,42 % d’accord observé ;
* Cohen kappa poolé = 0,6342 ;
* 1 688 désaccords ;
* une différence systématique de calibration entre les deux juges.

Ces résultats décrivent le comportement inter-juges.

Ils ne permettent pas d’établir qu’un juge constitue une référence absolue.

## Extensions prévues

Les prochains travaux incluent :

* un troisième juge indépendant ;
* une analyse de répétabilité intra-juge ;
* un panel stratifié d’adjudication humaine ;
* une réplication sur des corpus métier ;
* des releases séparées de cartographie comportementale sur panels répétés.

## Règle de gouvernance

> NeoMundi publie des profils IA observables, auditables et reproductibles — pas des classements.

## Licence

Apache License 2.0.
