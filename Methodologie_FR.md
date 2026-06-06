# NeoMundi — Cartographie des profils TruthfulQA

## Méthodologie publique v3.0

## 1. Objectif

Ce dépôt documente une méthodologie publique et reproductible permettant de construire des profils IA pseudonymisés et multidimensionnels à partir :

* d’un corpus d’évaluation factuelle TruthfulQA ;
* d’une validation par double jugement ;
* de signaux comportementaux runtime distincts.

L’objectif n’est pas de publier un classement universel des modèles.

L’objectif est de documenter :

* des différences observables ;
* l’incertitude méthodologique ;
* la calibration inter-juges ;
* les dimensions comportementales runtime ;
* les limites du protocole ;
* la reproductibilité des analyses.

## 2. Règle de gouvernance publique

NeoMundi publie :

* des profils pseudonymisés ;
* des lectures factuelles séparées par juge ;
* des métriques d’accord inter-juges ;
* des dimensions comportementales runtime ;
* les limites méthodologiques ;
* des artefacts publics figés et protégés par checksum.

NeoMundi ne publie pas :

* les noms des providers ;
* les noms des modèles ;
* des classements ;
* des ratings ;
* des scores composites ;
* des grades universels de qualité ;
* des recommandations automatiques de déploiement ;
* les réponses brutes ;
* les traces individuelles par question ;
* les justifications textuelles des juges.

## 3. Pourquoi publier des profils plutôt que des classements ?

Un score unique peut masquer plusieurs phénomènes distincts :

1. l’évaluation factuelle ;
2. la calibration inter-juges ;
3. le comportement runtime ;
4. la répétabilité ;
5. l’incertitude ;
6. les effets propres au corpus.

La méthodologie actuelle conserve ces couches séparées.

Un système peut recevoir des évaluations factuelles différentes selon le juge tout en restant stable au runtime.

Un profil stable au runtime n’implique pas automatiquement une factualité parfaite.

Un verdict factuel positif n’implique pas automatiquement une stabilité comportementale.

Ces dimensions doivent donc rester distinctes.

## 4. Corpus

La release publique actuelle repose sur :

```text
12 profils pseudonymisés
un corpus d’évaluation factuelle TruthfulQA
une validation par double jugement
des signaux comportementaux runtime séparés
```

La release publique figée est disponible dans :

```text
releases/truthfulqa-profiles-v1.0.0/
```

## 5. Identifiants publics des profils

Chaque profil public reçoit un identifiant pseudonymisé stable :

```text
PROFILE-XXXXXX
```

Ces identifiants sont conçus pour rester stables entre les futures releases publiques NeoMundi.

La table privée reliant les identités réelles aux identifiants publics n’est pas incluse dans ce dépôt.

La pseudonymisation n’est pas une anonymisation absolue. Des combinaisons rares de métriques peuvent créer un risque de réidentification par triangulation. Une revue humaine reste obligatoire avant toute publication.

## 6. Évaluation factuelle par double jugement

Chaque réponse comparable est évaluée indépendamment par deux juges distincts.

La release publique les nomme :

```text
Juge A
Juge B
```

Aucun des deux juges n’est considéré comme une source absolue de vérité.

La méthodologie publie :

```text
judge_a_positive_rate
judge_b_positive_rate
judge_observed_agreement_rate
judge_disagreement_rate
cohen_kappa
judge_b_minus_judge_a_positive_rate
```

Aucun verdict binaire consolidé n’est traité comme une vérité absolue.

## 7. Critères d’inclusion des paires

Une paire est incluse dans l’analyse si et seulement si :

1. le même `question_id` existe dans les deux jeux de données jugés ;
2. la réponse évaluée est identique dans les deux jeux de données ;
3. le verdict du Juge A est présent et interprétable ;
4. le verdict du Juge B est présent et interprétable.

Les paires ne respectant pas ces critères sont exclues de l’analyse comparative.

## 8. Résultats méthodologiques figés

La release figée actuelle documente :

| Métrique                          |        Valeur |
| --------------------------------- | ------------: |
| Profils pseudonymisés             |            12 |
| Paires de jugements comparables   |         9 087 |
| Accords                           |         7 399 |
| Désaccords                        |         1 688 |
| Taux d’accord observé             |       81,42 % |
| Taux de désaccord                 |       18,58 % |
| Cohen kappa poolé                 |        0,6342 |
| Taux de verdict positif du Juge A |       46,29 % |
| Taux de verdict positif du Juge B |       60,53 % |
| Écart Juge B - Juge A             | +14,24 points |

Parmi les 1 688 désaccords :

| Direction                       | Nombre | Part des désaccords |
| ------------------------------- | -----: | ------------------: |
| Juge A négatif / Juge B positif |  1 491 |              88,3 % |
| Juge A positif / Juge B négatif |    197 |              11,7 % |

La même asymétrie directionnelle apparaît sur les 12 profils.

## 9. Interprétation de la divergence inter-juges

L’asymétrie observée indique une différence systématique de calibration entre les deux juges dans le cadre du protocole actuel.

La méthodologie permet d’écrire :

> Sur ce corpus et selon ce protocole, le Juge B attribue plus fréquemment un verdict factuel positif que le Juge A.

La méthodologie ne permet pas d’écrire :

```text
Le Juge A a toujours raison.
Le Juge B a toujours raison.
Le Juge A constitue la référence absolue.
Le Juge B constitue la référence absolue.
La majorité de juges automatisés constitue une vérité absolue.
```

Un troisième juge indépendant et un panel d’adjudication humaine sont prévus.

## 10. Dimensions comportementales runtime

Les signaux runtime restent séparés de l’évaluation factuelle.

La release publique inclut :

```text
decision_distribution
regime_distribution
dg_profile_distribution
dg_flagged_rate
flagged_rate
hallucination_nonzero_rate
```

Ces dimensions ne sont pas fusionnées dans un score universel de qualité.

## 11. Résultats runtime exploratoires

Le corpus TruthfulQA actuel est principalement stable au runtime.

Aucune association robuste n’a été détectée entre la divergence inter-juges et :

```text
decision
dg_flagged
dg_profile
regime
```

Une association exploratoire faible apparaît entre un signal `hallucination` non nul et une fréquence plus élevée de divergence inter-juges.

Ce résultat reste provisoire et devra être répliqué sur des corpus plus larges et plus diversifiés.

## 12. Scripts de validation

Les scripts reproductibles sont disponibles dans :

```text
scripts/validation/
```

### Audit d’inventaire

```text
audit_truthfulqa_inventory.py
```

Fonctions :

* détecter les providers en interne ;
* apparier les fichiers RAW, Juge A et Juge B ;
* vérifier les volumes ;
* vérifier les `question_id` ;
* détecter les doublons ;
* vérifier l’alignement des réponses ;
* détecter les verdicts manquants.

### Analyse du double jugement

```text
analyze_double_judge_truthfulqa.py
```

Fonctions :

* aligner les fichiers Juge A et Juge B ;
* conserver les paires comparables ;
* calculer l’accord observé ;
* calculer Cohen kappa ;
* générer les matrices de confusion ;
* extraire les désaccords ;
* produire les agrégations runtime.

### Analyse de la structure des désaccords

```text
analyze_judge_disagreement_structure.py
```

Fonctions :

* mesurer les directions de désaccord ;
* analyser les désaccords par profil ;
* analyser les désaccords par question ;
* analyser les désaccords par dimension runtime ;
* identifier les zones récurrentes de friction entre juges.

## 13. Script de publication publique

Le script d’export public est disponible dans :

```text
scripts/publication/export_public_profiles.py
```

Il :

* crée ou réutilise des identifiants pseudonymisés stables ;
* sépare les métadonnées privées des artefacts publics ;
* sélectionne uniquement des champs autorisés ;
* bloque les fuites de noms de providers ;
* bloque les fuites de noms de modèles ;
* refuse les champs de classement ;
* refuse les champs de rating ;
* refuse les champs de score composite ;
* exclut les réponses brutes ;
* exclut les traces individuelles par question ;
* exclut les justifications textuelles des juges ;
* génère un dictionnaire public ;
* génère un manifeste ;
* génère des checksums SHA-256 ;
* exige une revue humaine avant publication.

## 14. Artefacts de la release publique

La release publique figée inclut :

```text
README_PUBLIC.md
public_profile_summary.csv
public_runtime_profile_summary.csv
public_methodology_validation.csv
public_data_dictionary.csv
PUBLICATION_REVIEW_CHECKLIST.md
RELEASE_MANIFEST.json
CHECKSUMS.sha256
```

## 15. Limites

### 15.1. Absence de juge de référence absolu

Les deux juges automatisés ne sont pas traités comme des sources absolues de vérité.

### 15.2. Interprétation propre au corpus

Les résultats s’appliquent au corpus TruthfulQA actuel et au protocole documenté.

Ils ne doivent pas être interprétés comme des affirmations universelles de performance.

### 15.3. Volumes comparables variables

Les volumes de paires comparables peuvent varier selon les profils, car certaines lignes sont filtrées ou exclues au cours du pipeline.

### 15.4. Homogénéité des régimes runtime

Le corpus TruthfulQA actuel est principalement stable au runtime.

Il ne suffit pas pour étudier finement les transitions de régime.

### 15.5. Limites de la pseudonymisation

La pseudonymisation réduit le risque d’identification directe, mais n’élimine pas le risque de réidentification par triangulation des métriques.

### 15.6. Résultats statistiques exploratoires

Les associations runtime sont exploratoires et doivent être répliquées.

## 16. Extensions méthodologiques prévues

### Troisième juge indépendant

* évaluation en aveugle des mêmes réponses ;
* métriques d’accord par paire de juges ;
* Cohen kappa par paire ;
* taux d’unanimité à trois juges ;
* configurations de majorité ;
* analyse multi-juges.

### Panel d’adjudication humaine

* échantillon stratifié de réponses ;
* au moins deux annotateurs humains indépendants ;
* processus d’adjudication en cas de désaccord ;
* accord humain-humain ;
* accord juge-humain ;
* taxonomie d’erreurs.

### Répétabilité intra-juge

* jugements répétés sur les mêmes réponses ;
* analyse de stabilité ;
* Cohen kappa intra-juge ;
* identification des zones de jugement instables.

### Corpus complémentaires

* corpus métier ;
* cas à haut risque ;
* legaltech ;
* IA médicale ;
* agents autonomes ;
* jeux de données multilingues ;
* prompts adversariaux.

### Releases de cartographie comportementale

Des releases séparées analyseront les panels comportementaux répétés :

```text
12 × 3 × 150
12 × 3 × 450
```

Ces releases réutiliseront les mêmes identifiants pseudonymisés stables.

## 17. Principe méthodologique final

> NeoMundi publie des profils IA observables, auditables et reproductibles — pas des classements.
