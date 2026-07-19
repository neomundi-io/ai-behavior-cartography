# Cartographie du comportement des IA NeoMundi — Méthodologie publique

🌐 **Langue :** [English](./Methodology_EN.md) · [Français](./Methodologie_FR.md)

📘 **Présentation du programme :** [English README](./README.md) · [README français](./README_FR.md)

🧭 **Guides d’utilisation :** [English](./USAGE_EN.md) · [Français](./USAGE_FR.md)

🔬 **Science ouverte :** [OPEN_SCIENCE.md](./OPEN_SCIENCE.md)

🌍 **NeoMundi :** [Observatoire IA](https://github.com/neomundi-io/neomundi-ai-observatory) · [Baromètre hebdomadaire](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer) · [Site français](https://neomundi.org/) · [English website](https://neomundi.org/en/home)

---

## Méthodologie publique v4.0

## 1. Objet

Le présent document définit la méthodologie publique utilisée par le programme **Cartographie du comportement des IA NeoMundi**.

La Cartographie est conçue pour observer et comparer des propriétés distinctes du comportement des IA génératives sur des corpus communs, lors d’exécutions répétées et dans des conditions runtime documentées.

Son objectif n’est pas de publier un classement universel des modèles.

Son objectif est de produire des éléments de preuve observables, auditables et reproductibles concernant :

- la stabilité des réponses ;
- l’évaluation de factualité ;
- l’accord inter-juges ;
- la variation sémantique ;
- la cohérence ;
- la latence ;
- les régimes comportementaux ;
- la variation runtime ;
- la couverture et la complétude ;
- l’incertitude méthodologique.

Le programme maintient ces dimensions analytiquement séparées.

> Un signal est une observation qui exige une interprétation, et non un verdict.

---

## 2. Périmètre de la méthodologie

La méthodologie publique actuelle couvre deux protocoles indépendants :

1. **Cartographie jugée du comportement des IA — `12 × 790`**
2. **Cartographie de stabilité runtime — `12 × 3 × 150`**

Ces protocoles répondent à des questions différentes et ne doivent pas être fusionnés en un score universel de qualité.

Le protocole jugé compare la stabilité et la factualité évaluée extérieurement sur un large corpus factuel.

Le protocole runtime observe la variation comportementale entre des vagues d’exécution répétées.

---

## 3. Règle de gouvernance publique

NeoMundi peut publier :

- des profils publics désidentifiés ;
- des résultats agrégés au niveau des profils ;
- des résultats agrégés au niveau des questions ou familles de questions ;
- des évaluations de factualité provenant de juges séparés ;
- des métriques d’accord inter-juges ;
- des dimensions comportementales runtime ;
- des informations de couverture et de complétude ;
- des limites méthodologiques ;
- des manifestes de release ;
- des empreintes d’intégrité ;
- des artefacts publics gelés ;
- de la documentation de reproductibilité ;
- des rapports analytiques et cartographies visuelles.

NeoMundi ne publie pas par défaut :

- les noms des fournisseurs ;
- les noms des modèles ;
- le registre privé de correspondance des profils ;
- des classements ;
- des notations ;
- des scores composites de qualité ;
- des notes universelles de qualité ;
- des recommandations automatiques de déploiement ;
- les réponses brutes complètes ;
- les prompts complets lorsque leur divulgation compromettrait le protocole ;
- les traces privées au niveau des questions ;
- les identifiants de requête ;
- les identifiants de trace ;
- les payloads API bruts ;
- les horodatages précis des exécutions ;
- les raisonnements privés des juges ;
- les clés API ;
- les identifiants d’infrastructure ;
- les exports de campagne non publiés ;
- les diagnostics internes ;
- la logique de calcul propriétaire.

La transparence publique n’exige pas la divulgation incontrôlée des actifs opérationnels protégés.

---

## 4. Pourquoi une cartographie plutôt qu’un classement ?

Un score unique peut dissimuler plusieurs phénomènes distincts :

1. l’évaluation factuelle ;
2. la calibration entre juges ;
3. la stabilité des réponses ;
4. la variation sémantique ;
5. la cohérence ;
6. les régimes runtime ;
7. la répétabilité ;
8. l’incertitude ;
9. les effets propres au corpus ;
10. les effets propres au protocole.

La méthodologie actuelle maintient ces couches séparées.

Un système peut recevoir des évaluations factuelles différentes selon le juge tout en restant stable à l’exécution.

Un profil runtime stable n’implique pas automatiquement une exactitude factuelle.

Un verdict factuel positif n’implique pas automatiquement une stabilité runtime.

Une réponse variable n’est pas automatiquement fausse.

Un signal de risque factuel n’est pas une détermination absolue de vérité.

Ces dimensions doivent donc rester distinctes.

---

## 5. Identifiants publics des profils

Chaque système observé est représenté publiquement par un identifiant opaque stable :

```text
PROFILE-XXXXXX
```

Ces identifiants sont conçus pour rester stables entre des releases publiques NeoMundi compatibles.

Les identifiants publics ne sont pas dérivés :

- des noms des fournisseurs ;
- des noms des modèles ;
- de l’ordre alphabétique ;
- de la performance ;
- de la factualité ;
- de la stabilité ;
- du score ;
- du classement.

La correspondance privée entre les systèmes observés et les identifiants publics est conservée séparément et n’est pas incluse dans ce dépôt.

Les releases publiques sont **désidentifiées**.

Elles ne sont pas présentées comme irréversiblement anonymes.

Des combinaisons rares de métriques publiques peuvent créer un risque résiduel de réidentification par triangulation. Une revue manuelle avant publication reste obligatoire.

---

# Partie I — Cartographie jugée du comportement des IA

## 6. Présentation du protocole 1

Le protocole jugé repose sur :

```text
12 profils d’IA désidentifiés
× 790 questions TruthfulQA
= 9 480 réponses sources
```

Le protocole comprend :

- le corpus complet de 790 questions TruthfulQA ;
- une réponse source par profil et par question ;
- des informations de stabilité observée lorsqu’elles sont disponibles ;
- une évaluation de factualité par un juge fondé sur OpenAI ;
- une évaluation de factualité par un juge fondé sur Mistral ;
- un filtrage des paires comparables ;
- l’accord inter-juges ;
- le kappa de Cohen comme indicateur secondaire d’accord ;
- des agrégations au niveau des profils et du corpus.

Son objectif est de comparer la stabilité observée et la factualité évaluée extérieurement sur un large corpus d’évaluation factuelle.

---

## 7. Corpus

Le corpus d’évaluation factuelle est TruthfulQA.

La release publique actuelle contient :

```text
12 profils désidentifiés
790 questions par profil
9 480 réponses sources
2 juges de factualité séparés
```

Le corpus est utilisé comme instrument d’évaluation factuelle.

Les résultats qui en sont issus ne doivent pas être interprétés comme des affirmations universelles de performance pour tous les domaines, langues, tâches ou contextes de déploiement.

---

## 8. Juges de factualité séparés

Chaque réponse comparable est évaluée indépendamment par deux juges automatisés distincts.

La release publique peut identifier les systèmes de jugement par famille ou implémentation lorsque cette divulgation est méthodologiquement appropriée.

Pour la campagne de juillet 2026, les deux évaluations factuelles sont conservées séparément comme :

```text
juge fondé sur OpenAI
juge fondé sur Mistral
```

Aucun juge n’est considéré comme une source absolue de vérité.

La méthodologie peut publier :

```text
judge_a_positive_rate
judge_b_positive_rate
judge_observed_agreement_rate
judge_disagreement_rate
cohen_kappa
judge_b_minus_judge_a_positive_rate
```

Aucun verdict binaire consolidé n’est traité comme une vérité absolue.

Le désaccord entre juges est conservé comme un résultat méthodologique, plutôt que masqué par une agrégation forcée.

---

## 9. Critères d’inclusion des paires comparables

Une paire de réponses jugées est incluse dans l’analyse des paires comparables si et seulement si :

1. le même `question_id` existe dans les deux jeux de données jugés ;
2. la réponse évaluée est identique dans les deux jeux ;
3. le verdict du premier juge est présent et interprétable ;
4. le verdict du second juge est présent et interprétable ;
5. l’identifiant du profil peut être associé de manière cohérente ;
6. aucune duplication ni erreur d’alignement n’invalide la ligne.

Les paires qui ne satisfont pas ces critères sont exclues des calculs de comparabilité.

Le nombre total de paires comparables peut donc être inférieur au nombre total de réponses sources.

La couverture doit être publiée avec les statistiques d’accord.

---

## 10. Métriques inter-juges

Le protocole jugé peut publier :

- le nombre total de paires de jugement comparables ;
- les accords ;
- les désaccords ;
- le taux d’accord observé ;
- le taux de désaccord ;
- le kappa de Cohen ;
- le taux de verdicts positifs de chaque juge ;
- le nombre de désaccords par direction ;
- la part de chaque direction de désaccord ;
- la divergence entre juges au niveau des profils ;
- la divergence entre juges au niveau des questions.

Le kappa de Cohen est traité comme un indicateur secondaire d’accord.

Il doit être interprété conjointement avec :

- l’accord observé ;
- l’équilibre des classes ;
- la prévalence des verdicts positifs ;
- le volume de paires comparables ;
- l’asymétrie directionnelle ;
- la composition du corpus.

Aucune statistique d’accord isolée ne suffit à établir la validité d’un juge.

---

## 11. Résultats gelés de juillet 2026 — protocole jugé

La release jugée gelée documente :

| Métrique | Valeur |
|---|---:|
| Profils désidentifiés | 12 |
| Réponses sources | 9 480 |
| Paires de jugement comparables | 9 087 |
| Accords | 7 399 |
| Désaccords | 1 688 |
| Taux d’accord observé | 81,42 % |
| Taux de désaccord | 18,58 % |
| Kappa de Cohen agrégé | 0,6342 |
| Taux de verdicts positifs du juge A | 46,29 % |
| Taux de verdicts positifs du juge B | 60,53 % |
| Juge B moins juge A — taux de verdicts positifs | +14,24 points |

Parmi les 1 688 désaccords :

| Direction | Nombre | Part des désaccords |
|---|---:|---:|
| Juge A négatif / juge B positif | 1 491 | 88,3 % |
| Juge A positif / juge B négatif | 197 | 11,7 % |

La même asymétrie directionnelle apparaît sur les 12 profils.

Ces chiffres décrivent uniquement la release gelée.

Ils ne doivent pas être traités comme des propriétés universelles des familles de juges en dehors de ce corpus et de ce protocole.

---

## 12. Interprétation de la divergence entre juges

L’asymétrie observée permet d’énoncer :

> Dans ce corpus et selon ce protocole, le juge B a produit des verdicts factuels positifs plus fréquemment que le juge A.

La méthodologie ne permet pas d’affirmer :

```text
Le juge A a toujours raison.
Le juge B a toujours raison.
Le juge A constitue la référence absolue.
Le juge B constitue la référence absolue.
La majorité des juges automatisés constitue une vérité absolue.
L’accord entre juges automatisés prouve l’exactitude factuelle.
```

La divergence entre juges est interprétée comme un signal de calibration et de méthode.

Elle n’est pas résolue par un vote majoritaire automatique.

---

## 13. La stabilité et la factualité restent séparées

Le protocole jugé peut comparer la stabilité observée avec les résultats de factualité.

Ces dimensions restent analytiquement distinctes.

Une réponse peut être :

- stable et évaluée factuellement positive ;
- stable et évaluée factuellement négative ;
- variable et évaluée factuellement positive ;
- variable et évaluée factuellement négative ;
- évaluée différemment par des juges distincts.

La méthodologie ne construit donc pas de score composite universel combinant stabilité et factualité.

---

# Partie II — Cartographie de stabilité runtime

## 14. Présentation du protocole 2

Le protocole runtime repose sur :

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
- des exécutions répétées dans des conditions documentées ;
- des mesures de stabilité ;
- des signaux de variation sémantique ;
- des indicateurs de cohérence ;
- des observations de latence ;
- une classification des régimes comportementaux ;
- des comparaisons entre vagues.

Son objectif est d’observer la variabilité runtime, la répétabilité et les changements de régime comportemental.

---

## 15. Panel équilibré de 150 questions

Le protocole runtime utilise un panel équilibré de 150 questions.

Ce panel est conçu pour fournir une surface d’observation comportementale plus large qu’un instrument hebdomadaire fondé sur un petit nombre de questions fixes.

Le jeu de données peut inclure plusieurs types de questions, domaines ou conditions de réponse.

La release publique doit documenter :

- la version du panel ;
- le nombre de questions ;
- le nombre de profils ;
- le nombre de vagues ;
- le nombre d’exécutions planifiées ;
- le nombre d’exécutions réalisées ;
- la couverture ;
- les règles d’exclusion ;
- les limites connues.

Toute modification de la version du panel crée une frontière méthodologique qui doit être documentée avant toute comparaison longitudinale.

---

## 16. Architecture en vagues répétées

L’architecture en trois vagues permet d’observer :

- la répétabilité intra-profil ;
- la variation entre vagues ;
- les changements de stabilité ;
- les changements de variation sémantique ;
- la persistance des régimes ;
- les transitions de régime ;
- les différences de latence ;
- les différences de couverture.

L’existence d’une différence entre deux vagues n’en établit pas la cause.

La formulation publique appropriée est :

> Une différence comportementale a été observée entre les vagues dans les conditions du protocole.

L’attribution à une mise à jour du modèle, une intervention du fournisseur, une modification de l’infrastructure ou un changement de politique exige des preuves complémentaires.

---

## 17. Familles de signaux runtime

Selon la couverture et la maturité de la release, le protocole runtime peut publier ou documenter :

```text
stability
semantic_variation
coherence
decision_distribution
regime_distribution
inter_wave_variation
latency
coverage
completeness
cost
token_consumption
delta_g
```

`delta_g` est publié comme un signal avancé observable de variation runtime.

Aucun signal runtime n’est interprété isolément comme une évaluation complète :

- de la véracité ;
- de la sécurité ;
- de la conformité ;
- de l’adéquation au déploiement ;
- de la qualité du modèle ;
- de la gouvernabilité.

---

## 18. Régimes comportementaux

Le protocole runtime peut classer les observations dans des régimes comportementaux documentés.

Un régime représente une catégorie analytique dérivée de signaux observés et de règles définies pour une release.

Un régime n’est pas :

- une certification ;
- un statut de sécurité ;
- une détermination juridique ;
- une autorisation de déploiement ;
- une explication causale.

Les définitions des régimes doivent être publiées avec la release ou le contrat de métriques correspondant.

Toute modification des seuils de régime ou de la logique de décision doit être versionnée.

---

## 19. Relation entre signaux runtime et factualité

Les signaux comportementaux runtime restent séparés de l’évaluation factuelle.

Un signal de variation sémantique n’établit pas, à lui seul, une erreur factuelle.

Un signal de risque factuel n’identifie pas automatiquement la cause d’une erreur.

Une réponse stable peut être systématiquement incorrecte.

Une réponse variable peut contenir plusieurs formulations acceptables.

La méthodologie interdit donc de réduire les dimensions runtime et factuelles à un score absolu unique.

---

# Partie III — Validation et publication

## 20. Principes de validation

Avant toute release publique, le pipeline de mesure doit être contrôlé concernant :

- la complétude du corpus ;
- la couverture des profils ;
- les nombres de lignes attendus ;
- les lignes dupliquées ;
- les identifiants manquants ;
- les verdicts manquants ;
- les verdicts malformés ;
- l’alignement des réponses ;
- l’alignement des questions ;
- la comparabilité entre juges ;
- la cohérence des calculs de métriques ;
- la cohérence des agrégations ;
- les fuites de noms de fournisseurs ;
- les fuites de noms de modèles ;
- les fuites de champs privés ;
- la complétude des manifestes ;
- la génération des empreintes d’intégrité.

La validation porte sur le processus de mesure et de publication.

Elle ne valide pas le système d’IA lui-même.

---

## 21. Scripts de validation

Les scripts de validation et d’analyse sont publiés dans :

```text
scripts/
```

Le dépôt peut inclure des scripts pour :

### Audit de l’inventaire du corpus

Fonctions typiques :

- détecter les fournisseurs en interne ;
- associer les fichiers sources et les fichiers jugés ;
- vérifier les nombres de lignes ;
- vérifier `question_id` ;
- détecter les doublons ;
- vérifier l’alignement des réponses ;
- détecter les verdicts manquants ;
- publier la couverture.

### Analyse d’accord entre deux juges

Fonctions typiques :

- aligner les jeux de données jugés ;
- conserver les paires comparables ;
- calculer l’accord observé ;
- calculer le kappa de Cohen ;
- produire les matrices de confusion ;
- extraire les lignes de désaccord ;
- agréger par profil ou question.

### Analyse de la structure des désaccords

Fonctions typiques :

- mesurer la direction des désaccords ;
- analyser la fréquence des désaccords par profil ;
- analyser la fréquence des désaccords par question ;
- analyser la fréquence des désaccords par dimension runtime ;
- identifier les zones récurrentes de friction entre juges.

### Analyse de la cartographie runtime

Fonctions typiques :

- comparer les vagues répétées ;
- calculer la stabilité ;
- calculer la variation sémantique ;
- calculer la cohérence ;
- classifier les régimes ;
- agréger la latence ;
- publier la couverture ;
- générer des synthèses publiques par profil.

Les noms des scripts et la structure des répertoires peuvent évoluer.

Le manifeste de release et les guides d’utilisation constituent les références canoniques pour une version publiée donnée.

---

## 22. Exigences applicables à l’exporteur public

Un exporteur public doit :

- créer ou réutiliser des identifiants stables de profils désidentifiés ;
- séparer les métadonnées privées de correspondance des artefacts publics ;
- publier uniquement des champs autorisés ;
- bloquer les fuites de noms de fournisseurs ;
- bloquer les fuites de noms de modèles ;
- rejeter les champs de classement ;
- rejeter les champs de notation ;
- rejeter les scores composites universels ;
- exclure les réponses brutes protégées ;
- exclure les traces privées au niveau des questions ;
- exclure les raisonnements privés des juges ;
- générer un dictionnaire public des données ;
- générer un manifeste de release ;
- générer des empreintes d’intégrité ;
- exiger une revue manuelle avant publication.

L’export automatisé ne remplace pas la revue humaine de la release.

---

## 23. Artefacts des releases publiques

Selon le protocole, une release publique peut inclure :

```text
README.md
README_PUBLIC.md
public_profile_summary.csv
public_question_summary.csv
public_runtime_profile_summary.csv
public_methodology_validation.csv
public_data_dictionary.csv
PUBLICATION_REVIEW_CHECKLIST.md
RELEASE_MANIFEST.json
CHECKSUMS.sha256
```

L’ensemble exact des fichiers peut varier selon la release.

Le README et le manifeste de la release définissent l’inventaire faisant autorité.

---

## 24. Frontière de publication publique

Les artefacts publics peuvent être examinés afin d’en vérifier la cohérence interne.

La reproduction complète depuis les sources peut nécessiter l’accès à des éléments protégés, notamment :

- les exports privés des campagnes ;
- les correspondances internes des fournisseurs ;
- les prompts complets ;
- les réponses sources complètes ;
- les détails de configuration des juges ;
- la configuration de l’infrastructure ;
- les traces d’exécution non publiques ;
- les artefacts internes de validation.

Chaque release doit documenter sa propre limite de reproductibilité.

La reproductibilité publique signifie que les artefacts publiés peuvent être vérifiés, analysés et examinés dans les limites explicitement définies par le programme.

---

## 25. Intégrité et releases gelées

Une release gelée doit conserver :

- un répertoire stable ;
- une référence méthodologique versionnée ;
- un manifeste de release ;
- les empreintes des fichiers ;
- les définitions publiques des données ;
- les limites connues ;
- la date de publication ;
- la version du protocole.

Les corrections apportées à une release gelée doivent être documentées au moyen :

- d’une nouvelle version ;
- d’une note de correction ;
- d’un manifeste amendé ;
- d’empreintes mises à jour ;
- d’un historique transparent des modifications.

Les artefacts historiques publiés ne doivent pas être réécrits silencieusement.

---

# Partie IV — Limites d’interprétation

## 26. Doctrine générale d’interprétation

La Cartographie suit une règle fondamentale :

> Un signal est une observation qui exige une interprétation, et non un verdict.

Une différence observée n’établit pas, à elle seule :

- la supériorité d’un système sur un autre ;
- une mise à jour du modèle côté fournisseur ;
- une dégradation ;
- une amélioration ;
- une explication causale ;
- la conformité réglementaire ;
- l’adéquation au déploiement ;
- la véracité dans tous les domaines ;
- la qualité globale ;
- la gouvernabilité dans un contexte donné.

L’attribution causale exige des preuves complémentaires.

---

## 27. Absence de juge de référence absolu

Les juges automatisés ne sont pas traités comme des sources absolues de vérité.

Leurs résultats sont des mesures produites dans le cadre d’un protocole de jugement déterminé.

L’accord entre juges ne prouve pas l’exactitude factuelle.

Le désaccord entre juges ne prouve pas qu’ils sont tous deux également peu fiables.

La revue humaine et des évaluations indépendantes supplémentaires restent nécessaires pour les interprétations à fort enjeu.

---

## 28. Interprétation propre au corpus

Les résultats s’appliquent au corpus, au protocole, à la configuration des juges et aux conditions d’exécution de la release concernée.

Ils ne doivent pas être interprétés comme des affirmations universelles de performance.

Un résultat obtenu sur TruthfulQA ne se généralise pas automatiquement :

- aux tâches juridiques ;
- aux tâches médicales ;
- aux tâches financières ;
- aux interactions multilingues ;
- aux workflows agentiques ;
- aux déploiements de production ;
- aux décisions à haut risque ;
- aux environnements adversariaux.

---

## 29. Différences de volumes comparables

Les volumes de paires comparables peuvent différer entre les profils, car certaines lignes peuvent être filtrées ou exclues durant le pipeline de jugement.

Les pourcentages d’accord doivent donc être interprétés conjointement avec :

- le nombre de paires comparables ;
- le nombre de réponses sources ;
- la couverture ;
- les motifs d’exclusion ;
- les différences de volume entre profils.

---

## 30. Limites des régimes runtime

Un corpus majoritairement stable à l’exécution peut être insuffisant pour étudier en profondeur les transitions de régime.

L’absence de changement de régime observé ne prouve pas qu’un système restera stable avec d’autres prompts, domaines, périodes ou conditions de déploiement.

---

## 31. Limites de la désidentification

La désidentification réduit le risque d’identification directe, mais n’élimine pas le risque résiduel de réidentification par triangulation métrique ou connaissance externe.

Une revue manuelle reste obligatoire avant publication.

Les identifiants publics ne doivent pas être rétro-ingénierés ni présentés comme des identités confirmées de fournisseurs sans preuve indépendante et autorisation.

---

## 32. Résultats statistiques exploratoires

Les associations exploratoires doivent être explicitement qualifiées comme telles.

Elles exigent une réplication avant d’être considérées comme robustes.

Une corrélation ou une association n’établit pas une causalité.

Les analyses par sous-groupes doivent tenir compte :

- de la taille de l’échantillon ;
- des comparaisons multiples ;
- du déséquilibre entre profils ;
- du déséquilibre entre questions ;
- des données manquantes ;
- des modifications de protocole.

---

# Partie V — Évolution méthodologique

## 33. Extensions prévues

Les travaux futurs peuvent inclure :

### Troisième juge indépendant

- évaluation à l’aveugle des mêmes réponses ;
- métriques d’accord par paire ;
- kappa de Cohen par paire ;
- taux d’unanimité entre trois juges ;
- configurations de majorité à trois juges ;
- analyse d’accord multi-juges.

### Panel d’adjudication humaine

- échantillon stratifié de réponses ;
- au moins deux annotateurs humains indépendants ;
- adjudication des désaccords ;
- accord humain-humain ;
- accord juge-humain ;
- taxonomie des erreurs.

### Répétabilité intra-juge

- jugements répétés des mêmes réponses ;
- analyse de stabilité ;
- kappa de Cohen intra-juge ;
- identification des zones de jugement instables.

### Corpus complémentaires

- corpus sectoriels ;
- cas d’usage à haut risque ;
- IA juridique ;
- IA médicale ;
- finance et assurance ;
- agents autonomes ;
- jeux de données multilingues ;
- prompts adversariaux.

### Panels runtime étendus

De futures structures runtime peuvent notamment inclure :

```text
12 × 3 × 450
vagues répétées supplémentaires
panels sectoriels
panels multilingues
```

Toute extension doit être versionnée et ne doit pas être présentée comme directement comparable aux releases antérieures tant que la compatibilité n’a pas été établie.

---

## 34. Gouvernance méthodologique mensuelle

La Cartographie est conçue comme un programme mensuel récurrent.

Une release mensuelle peut :

- réutiliser un protocole existant validé ;
- introduire une révision documentée du protocole ;
- ajouter un nouveau corpus ;
- ajouter un nouveau juge ;
- étendre un panel runtime ;
- ajouter un nouveau signal ;
- publier une correction ;
- préserver un protocole antérieur sans modification.

Les modifications méthodologiques doivent être documentées avant toute comparaison entre mois.

Le dépôt doit conserver :

- les versions méthodologiques ;
- les références de protocole propres aux releases ;
- les historiques de modifications ;
- les notes de compatibilité ;
- les ruptures connues de comparabilité.

---

## 35. Principes scientifiques

La méthodologie suit sept principes :

1. **Mesurer avant d’interpréter.**
2. **Maintenir séparées les propriétés distinctes.**
3. **Répéter avant de généraliser.**
4. **Ne jamais confondre stabilité et vérité.**
5. **Préserver les désaccords entre juges plutôt que les dissimuler.**
6. **Distinguer observation, interprétation et attribution causale.**
7. **Traiter chaque signal comme un élément de preuve, et non comme un verdict.**

---

## 36. Principe méthodologique final

> NeoMundi publie des profils de comportement des IA observables, auditables et reproductibles — pas des classements.

La Cartographie mesure des propriétés comportementales distinctes dans des conditions documentées.

Elle ne transforme pas la complexité méthodologique en verdict universel.
