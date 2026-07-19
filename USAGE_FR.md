# Cartographie du comportement des IA NeoMundi — Guide d’utilisation

🌐 **Langue :** [English](./USAGE_EN.md) · [Français](./USAGE_FR.md)

📘 **Présentation du programme :** [English README](./README.md) · [README français](./README_FR.md)

📐 **Méthodologie :** [English](./Methodology_EN.md) · [Français](./Methodologie_FR.md)

🔬 **Science ouverte :** [OPEN_SCIENCE.md](./OPEN_SCIENCE.md)

🌍 **NeoMundi :** [Observatoire IA](https://github.com/neomundi-io/neomundi-ai-observatory) · [Baromètre hebdomadaire](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer) · [Site français](https://neomundi.org/) · [English website](https://neomundi.org/en/home)

---

## 1. Objet

Ce guide documente le workflow public de validation, d’analyse et de publication utilisé par le programme **Cartographie du comportement des IA NeoMundi**.

Le dépôt prend en charge deux axes méthodologiques distincts :

1. **Cartographie jugée du comportement des IA — `12 × 790`**
2. **Cartographie de stabilité runtime — `12 × 3 × 150`**

Le workflow public est conçu pour produire des profils multidimensionnels et désidentifiés du comportement des IA sans publier les éléments opérationnels protégés.

Le processus de publication publique ne publie pas par défaut :

- les noms des fournisseurs ;
- les noms des modèles ;
- le registre privé de correspondance des profils ;
- les classements ;
- les notations ;
- les scores composites universels ;
- les réponses brutes complètes ;
- les prompts complets protégés ;
- les traces privées au niveau des questions ;
- les raisonnements des juges ;
- les identifiants de requête ;
- les identifiants de trace ;
- les payloads API bruts ;
- les horodatages précis des exécutions ;
- les clés API ;
- les identifiants d’infrastructure ;
- les diagnostics internes ;
- les exports de campagne non publiés.

> Le workflow public publie des preuves inspectables, et non l’intégralité du registre privé de mesure.

---

## 2. Structure du dépôt

Le dépôt public est organisé comme suit :

```text
ai-behavior-cartography/
├── README.md
├── README_FR.md
├── Methodology_EN.md
├── Methodologie_FR.md
├── USAGE_EN.md
├── USAGE_FR.md
├── OPEN_SCIENCE.md
├── LICENSE
│
├── scripts/
│   ├── validation/
│   ├── analysis/
│   └── publication/
│
└── releases/
    └── july2026-behavior-cartography/
        ├── judged-cartography-12x790/
        └── runtime-stability-12x3x150/
```

Les noms exacts des scripts internes et des artefacts de release peuvent évoluer.

Pour une release gelée, le README et le manifeste de la release définissent l’inventaire de fichiers faisant autorité.

---

## 3. Prérequis

Environnement recommandé :

```text
Python 3.10+
pandas
```

Certains scripts peuvent également nécessiter :

```text
numpy
scikit-learn
```

Installer les dépendances minimales :

```bash
python -m pip install pandas numpy scikit-learn
```

Pour un travail reproductible, utiliser un environnement virtuel dédié :

```bash
python -m venv .venv
```

L’activer sous Linux ou macOS :

```bash
source .venv/bin/activate
```

L’activer sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Puis installer les dépendances :

```bash
python -m pip install pandas numpy scikit-learn
```

---

# Partie I — Cartographie jugée du comportement des IA

## 4. Structure de travail interne du protocole `12 × 790`

Le protocole jugé utilise un répertoire de travail local similaire à :

```text
truthfulqa_12_profiles/
├── 01_raw_results/
├── 02_openai_judged/
├── 03_mistral_judged/
├── 04_analysis_output/
├── audit_truthfulqa_inventory.py
├── analyze_double_judge_truthfulqa.py
└── analyze_judge_disagreement_structure.py
```

Formats internes typiques des fichiers :

```text
01_raw_results/
truthfulqa_<internal_provider>_dg_results.csv

02_openai_judged/
truthfulqa_<internal_provider>_judged.csv

03_mistral_judged/
truthfulqa_<internal_provider>_mistral_judged.csv
```

Ces jeux de données sources locaux ne sont pas inclus dans le dépôt public.

Les identifiants internes des fournisseurs ne doivent pas apparaître dans les artefacts publics.

---

## 5. Étape 1 — Auditer l’inventaire TruthfulQA

Exécuter :

```bash
python audit_truthfulqa_inventory.py
```

Répertoire de sortie attendu :

```text
04_analysis_output/
```

Rapports généralement générés :

```text
inventory_audit_summary.csv
missing_or_mismatched_files.csv
row_counts_by_provider.csv
question_id_alignment_report.csv
response_alignment_report.csv
schema_comparison_report.csv
missing_verdicts_report.csv
audit_manifest.json
audit_console_summary.txt
```

À examiner en premier :

```text
audit_console_summary.txt
```

L’audit d’inventaire doit vérifier :

- la présence des fichiers sources ;
- la présence des fichiers jugés ;
- les nombres de lignes attendus ;
- l’alignement des `question_id` ;
- les identifiants dupliqués ;
- l’alignement des réponses ;
- la compatibilité des schémas ;
- les verdicts manquants ;
- les verdicts malformés ;
- les profils manquants ;
- les colonnes inattendues.

Ne pas poursuivre vers l’export public tant que des erreurs critiques d’alignement ou de couverture restent non résolues.

---

## 6. Étape 2 — Analyser l’accord entre les deux juges

Exécuter :

```bash
python analyze_double_judge_truthfulqa.py
```

Répertoire de sortie attendu :

```text
04_analysis_output/double_judge_analysis/
```

Rapports généralement générés :

```text
global_double_judge_summary.csv
double_judge_summary_by_provider.csv
confusion_matrix_by_provider.csv
judge_disagreements.csv
question_disagreement_frequency.csv
analysis_quality_report.csv
analysis_issues.csv
comparable_pairs_internal.csv
analysis_manifest.json
analysis_console_summary.txt
```

À examiner en premier :

```text
analysis_console_summary.txt
```

Le script doit calculer :

- le nombre total de réponses sources ;
- les paires de jugement comparables ;
- l’accord observé ;
- le taux de désaccord ;
- le kappa de Cohen agrégé ;
- le kappa de Cohen par fournisseur interne ;
- les matrices de confusion ;
- la direction des désaccords ;
- les taux de verdicts positifs par juge ;
- la couverture par profil ;
- les agrégations runtime lorsqu’elles sont disponibles.

La couverture doit être publiée conjointement avec les métriques d’accord.

---

## 7. Étape 3 — Analyser la structure des désaccords

Exécuter :

```bash
python analyze_judge_disagreement_structure.py \
  --input-dir "./04_analysis_output/double_judge_analysis"
```

Rapports généralement générés :

```text
disagreement_direction_summary.csv
disagreement_by_provider.csv
disagreement_by_question_frequency.csv
high_disagreement_questions.csv
disagreement_rows_internal.csv
disagreement_by_provider_and_decision.csv
disagreement_by_decision_global.csv
disagreement_by_provider_and_regime.csv
disagreement_by_regime_global.csv
disagreement_by_provider_and_dg_profile.csv
disagreement_by_dg_profile_global.csv
disagreement_by_provider_and_dg_flagged.csv
disagreement_by_dg_flagged_global.csv
disagreement_by_provider_and_hallucination.csv
disagreement_by_hallucination_global.csv
disagreement_structure_manifest.json
disagreement_structure_summary.txt
```

À examiner en premier :

```text
disagreement_structure_summary.txt
```

L’analyse peut servir à identifier :

- les asymétries directionnelles entre juges ;
- les questions à forte friction ;
- les divergences entre juges au niveau des profils ;
- les relations entre désaccord et signaux runtime ;
- les zones récurrentes d’incertitude méthodologique.

Ces analyses restent exploratoires tant qu’elles ne sont pas explicitement qualifiées comme robustes.

---

## 8. Étape 4 — Construire la release publique jugée

L’exporteur public doit utiliser un répertoire d’analyse interne gelé contenant au minimum :

```text
double_judge_summary_by_provider.csv
global_double_judge_summary.csv
comparable_pairs_internal.csv
```

Commande typique :

```bash
python export_public_profiles.py
```

Pour reconstruire volontairement une release existante :

```bash
python export_public_profiles.py --force
```

L’exporteur peut générer :

```text
public_release_truthfulqa_profiles/
_private_release_metadata/
```

### Répertoire public

Artefacts publics typiques :

```text
README.md
README_PUBLIC.md
public_profile_summary.csv
public_runtime_profile_summary.csv
public_methodology_validation.csv
public_data_dictionary.csv
PUBLICATION_REVIEW_CHECKLIST.md
RELEASE_MANIFEST.json
CHECKSUMS.sha256
```

### Répertoire privé

Artefacts privés typiques :

```text
profile_mapping_private.csv
release_build_log_private.txt
```

Ne jamais publier le répertoire privé.

---

# Partie II — Cartographie de stabilité runtime

## 9. Structure de travail interne du protocole `12 × 3 × 150`

Le protocole runtime peut utiliser un répertoire de travail similaire à :

```text
runtime_cartography_12x3x150/
├── 01_wave_1/
├── 02_wave_2/
├── 03_wave_3/
├── 04_combined/
├── 05_analysis_output/
├── validate_runtime_inventory.py
├── build_runtime_cartography.py
└── export_runtime_public_release.py
```

Une structure compatible peut également utiliser un fichier consolidé d’exécutions comportant des champs explicites tels que :

```text
profile_internal_id
question_id
wave_id
response
stability
semantic_variation
coherence
latency
regime
delta_g
```

Le schéma exact dépend de la release.

La méthodologie et le dictionnaire de données de la release définissent l’ensemble de champs faisant autorité.

---

## 10. Étape 1 — Valider l’inventaire runtime

La validation de l’inventaire runtime doit vérifier :

- les 12 profils internes attendus ;
- les 3 vagues attendues ;
- les 150 questions attendues ;
- les 5 400 exécutions planifiées ;
- les lignes d’exécution dupliquées ;
- les cellules profil-question-vague manquantes ;
- les identifiants de profil malformés ;
- les identifiants de vague malformés ;
- les identifiants de question manquants ;
- les réponses manquantes ;
- les métriques manquantes ou invalides ;
- les schémas incohérents entre vagues ;
- la couverture par profil ;
- la couverture par vague ;
- la couverture par question.

Une commande typique peut être :

```bash
python validate_runtime_inventory.py
```

Les sorties attendues peuvent inclure :

```text
runtime_inventory_summary.csv
missing_cells.csv
duplicate_rows.csv
schema_report.csv
coverage_by_profile.csv
coverage_by_wave.csv
coverage_by_question.csv
runtime_inventory_manifest.json
runtime_inventory_summary.txt
```

À examiner en premier :

```text
runtime_inventory_summary.txt
```

Ne pas poursuivre vers l’analyse tant que des erreurs critiques de couverture des cellules ou de schéma restent non résolues.

---

## 11. Étape 2 — Construire la cartographie runtime

Une commande typique peut être :

```bash
python build_runtime_cartography.py
```

L’analyse doit calculer, lorsqu’ils sont disponibles :

- la stabilité par profil ;
- la variation sémantique par profil ;
- la cohérence par profil ;
- les synthèses de latence ;
- les distributions des régimes comportementaux ;
- la variation entre vagues ;
- la couverture ;
- la complétude ;
- `delta_g` ;
- les indicateurs de coûts ou de consommation de tokens lorsqu’ils sont disponibles.

Les sorties typiques peuvent inclure :

```text
runtime_profile_summary.csv
runtime_question_summary.csv
runtime_wave_summary.csv
runtime_regime_distribution.csv
runtime_metric_contract.json
runtime_analysis_manifest.json
runtime_analysis_summary.txt
```

À examiner en premier :

```text
runtime_analysis_summary.txt
```

Une différence entre les vagues ne doit pas être présentée comme la preuve d’une mise à jour du modèle ou d’une modification côté fournisseur.

---

## 12. Étape 3 — Construire la release publique runtime

Une commande typique peut être :

```bash
python export_runtime_public_release.py
```

La release publique peut inclure :

```text
README.md
public_profile_summary.csv
public_question_summary.csv
public_wave_summary.csv
public_regime_distribution.csv
public_metric_contract.json
public_data_dictionary.csv
PUBLICATION_REVIEW_CHECKLIST.md
RELEASE_MANIFEST.json
CHECKSUMS.sha256
```

La zone privée de construction peut inclure :

```text
profile_mapping_private.csv
runtime_release_build_log_private.txt
private_execution_summary.csv
```

Ne jamais publier la correspondance privée, les exports privés au niveau des exécutions ni les journaux internes de construction.

---

## 13. Identifiants stables des profils désidentifiés

Le fichier privé de correspondance doit être conservé de manière sécurisée.

Emplacement typique :

```text
_private_release_metadata/profile_mapping_private.csv
```

Il permet de produire des identifiants publics stables :

```text
PROFILE-XXXXXX
```

Le même identifiant public doit renvoyer au même système observé entre les releases NeoMundi compatibles, notamment :

```text
releases TruthfulQA jugées
releases runtime 12 × 3 × 150
releases runtime étendues
releases de répétabilité
releases sectorielles
cartographies mensuelles
```

La terminologie publique est **désidentifié**, et non irréversiblement anonyme.

---

## 14. Garde-fous de publication

L’exporteur public doit :

- publier uniquement les champs autorisés ;
- bloquer les fuites de noms de fournisseurs ;
- bloquer les fuites de noms de modèles ;
- rejeter les champs de classement ;
- rejeter les champs de notation ;
- rejeter les scores composites universels ;
- exclure les réponses brutes protégées ;
- exclure les prompts protégés ;
- exclure les traces privées au niveau des questions ;
- exclure les raisonnements privés des juges ;
- exclure les identifiants de requête ;
- exclure les identifiants de trace ;
- exclure les horodatages précis des exécutions ;
- exclure les détails privés de coûts ;
- générer un dictionnaire public des données ;
- générer un manifeste de release ;
- générer des empreintes SHA-256 ;
- créer une checklist manuelle de publication.

Avant publication, examiner :

```text
PUBLICATION_REVIEW_CHECKLIST.md
```

La revue manuelle est obligatoire même lorsque tous les contrôles automatiques sont validés.

---

## 15. Vérifier les empreintes

Depuis le répertoire public gelé :

```bash
sha256sum -c CHECKSUMS.sha256
```

Sous Windows PowerShell :

```powershell
Get-FileHash .\README.md -Algorithm SHA256
```

Répéter pour chaque artefact public si nécessaire et comparer le résultat avec `CHECKSUMS.sha256`.

Toute divergence d’empreinte doit être résolue avant publication.

---

## 16. Vérifier les frontières des champs publics

Avant de committer une release, rechercher dans le répertoire public :

```text
noms de fournisseurs
noms de modèles
identifiants internes de profils
clés API
identifiants de requête
identifiants de trace
réponses brutes
champs de correspondance privée
champs de classement
champs de notation
champs de score composite
```

Exemples de recherches récursives :

```bash
grep -Rni "provider_name" .
grep -Rni "model_name" .
grep -Rni "request_id" .
grep -Rni "trace_id" .
grep -Rni "profile_mapping" .
```

Sous PowerShell :

```powershell
Get-ChildItem -Recurse -File | Select-String -Pattern "provider_name"
Get-ChildItem -Recurse -File | Select-String -Pattern "model_name"
Get-ChildItem -Recurse -File | Select-String -Pattern "request_id"
Get-ChildItem -Recurse -File | Select-String -Pattern "trace_id"
Get-ChildItem -Recurse -File | Select-String -Pattern "profile_mapping"
```

Ces contrôles complètent la revue manuelle, mais ne la remplacent pas.

---

## 17. Geler une release publique

Avant publication :

1. confirmer la version méthodologique ;
2. confirmer le nom du répertoire de release ;
3. confirmer l’inventaire des fichiers publics ;
4. confirmer les chiffres de couverture ;
5. confirmer la désidentification ;
6. vérifier les empreintes ;
7. examiner la checklist de publication ;
8. confirmer l’absence de champs protégés ;
9. enregistrer la date de publication ;
10. committer la release avec un message descriptif.

Une release gelée ne doit pas être modifiée silencieusement.

Les corrections doivent utiliser :

- une nouvelle version ;
- une note de correction ;
- un manifeste amendé ;
- des empreintes régénérées ;
- un historique documenté des modifications.

---

## 18. Règle d’interprétation publique

Chaque release doit être interprétée comme une publication de mesure multidimensionnelle.

Elle ne doit pas être interprétée comme :

- un classement de fournisseurs ;
- un classement de modèles ;
- un benchmark universel ;
- un score universel de qualité ;
- une certification de sécurité ;
- une détermination réglementaire ;
- une autorisation de déploiement ;
- la preuve qu’un juge automatisé constitue une source absolue de vérité ;
- la preuve que la stabilité implique l’exactitude factuelle ;
- la preuve que la variabilité implique une erreur factuelle.

La formulation appropriée est :

> Une propriété ou une différence comportementale a été observée dans les conditions du protocole.

---

## 19. Interprétation propre à chaque protocole

### Cartographie jugée — `12 × 790`

Utiliser ce protocole pour analyser :

- la stabilité sur un large corpus factuel ;
- la factualité selon des juges séparés ;
- l’accord entre juges ;
- le désaccord entre juges ;
- les asymétries de calibration ;
- l’évaluation factuelle propre au corpus.

Ne pas l’utiliser comme recommandation universelle de déploiement.

### Cartographie runtime — `12 × 3 × 150`

Utiliser ce protocole pour analyser :

- le comportement runtime répété ;
- la variation entre vagues ;
- la variation sémantique ;
- la cohérence ;
- la latence ;
- les régimes comportementaux ;
- la couverture.

Ne pas l’utiliser comme preuve d’exactitude factuelle ou de changement causal côté fournisseur.

---

## 20. Règle de gouvernance

> NeoMundi publie des profils de comportement des IA observables, auditables et reproductibles — pas des classements.

Le workflow public préserve :

- la séparation méthodologique ;
- la désidentification ;
- l’intégrité des preuves ;
- les limites d’interprétation ;
- les actifs opérationnels protégés ;
- la traçabilité des releases.

Un signal est un élément de preuve à interpréter, et non un verdict.
