# NeoMundi — Cartographie des profils TruthfulQA

## Guide d’utilisation

## 1. Objectif

Ce dépôt fournit les outils reproductibles de validation et de publication associés à la méthodologie NeoMundi de cartographie des profils TruthfulQA.

Le workflow public est conçu pour exposer des profils IA pseudonymisés et multidimensionnels sans publier :

* les noms des providers ;
* les noms des modèles ;
* des classements ;
* des ratings ;
* des scores composites ;
* les réponses brutes ;
* les traces individuelles par question ;
* les justifications textuelles des juges.

## 2. Structure du dépôt

```text
cartography-truthfulqa-profiles/
├── README.md
├── Methodology_EN.md
├── Methodologie_FR.md
├── USAGE_EN.md
├── USAGE_FR.md
├── LICENSE
│
├── scripts/
│   ├── validation/
│   │   ├── README.md
│   │   ├── audit_truthfulqa_inventory.py
│   │   ├── analyze_double_judge_truthfulqa.py
│   │   └── analyze_judge_disagreement_structure.py
│   │
│   └── publication/
│       └── export_public_profiles.py
│
└── releases/
    └── truthfulqa-profiles-v1.0.0/
        ├── README.md
        ├── README_PUBLIC.md
        ├── public_profile_summary.csv
        ├── public_runtime_profile_summary.csv
        ├── public_methodology_validation.csv
        ├── public_data_dictionary.csv
        ├── PUBLICATION_REVIEW_CHECKLIST.md
        ├── RELEASE_MANIFEST.json
        └── CHECKSUMS.sha256
```

## 3. Prérequis

Environnement recommandé :

```text
Python 3.10+
pandas
```

Installer la dépendance :

```bash
python -m pip install pandas
```

## 4. Structure locale du corpus interne

Les scripts de validation attendent un dossier local structuré ainsi :

```text
truthfulqa_12_models/
├── 01_raw_results/
├── 02_openai_judged/
├── 03_mistral_judged/
├── 04_analysis_output/
├── audit_truthfulqa_inventory.py
├── analyze_double_judge_truthfulqa.py
└── analyze_judge_disagreement_structure.py
```

Formats attendus :

```text
01_raw_results/
truthfulqa_<provider>_dg_results.csv

02_openai_judged/
truthfulqa_<provider>_judged.csv

03_mistral_judged/
truthfulqa_<provider>_mistral_judged.csv
```

Les jeux de données sources internes ne sont pas inclus dans le dépôt public.

## 5. Étape 1 — Auditer l’inventaire du corpus

Lancer :

```bash
python audit_truthfulqa_inventory.py
```

Dossier de sortie attendu :

```text
04_analysis_output/
```

Rapports principaux :

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

Lire en priorité :

```text
audit_console_summary.txt
```

L’audit vérifie :

* la présence des fichiers ;
* les volumes ;
* l’alignement des `question_id` ;
* les doublons ;
* l’identité des réponses comparées ;
* la compatibilité des schémas ;
* les verdicts manquants.

## 6. Étape 2 — Analyser l’accord entre les deux juges

Lancer :

```bash
python analyze_double_judge_truthfulqa.py
```

Dossier de sortie attendu :

```text
04_analysis_output/double_judge_analysis/
```

Rapports principaux :

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

Lire en priorité :

```text
analysis_console_summary.txt
```

Le script calcule :

* le nombre de paires comparables ;
* le taux d’accord observé ;
* le taux de désaccord ;
* Cohen kappa poolé ;
* Cohen kappa par provider interne ;
* les matrices de confusion ;
* les directions de désaccord ;
* les agrégations runtime.

## 7. Étape 3 — Analyser la structure des désaccords

Déposer le script dans le dossier d’analyse double-jugée figé ou préciser explicitement le dossier source.

Exemple :

```bash
python analyze_judge_disagreement_structure.py \
  --input-dir "./04_analysis_output/double_judge_analysis_v1_2026-06-06"
```

Rapports principaux :

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

Lire en priorité :

```text
disagreement_structure_summary.txt
```

## 8. Étape 4 — Générer une release publique conservatrice

Le script de publication attend un dossier d’analyse interne figé contenant :

```text
double_judge_summary_by_provider.csv
global_double_judge_summary.csv
comparable_pairs_internal.csv
```

Lancer :

```bash
python export_public_profiles.py
```

Pour reconstruire une release existante :

```bash
python export_public_profiles.py --force
```

Le script génère :

```text
public_release_truthfulqa_profiles_v1_2026-06-06/
_private_release_metadata/
```

### Dossier public

Le dossier public contient :

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

### Dossier privé

Le dossier privé contient :

```text
profile_mapping_private.csv
release_build_log_private.txt
```

Ne jamais publier le dossier privé.

## 9. Identifiants pseudonymisés stables

Le fichier privé suivant doit être conservé de manière sécurisée :

```text
_private_release_metadata/profile_mapping_private.csv
```

Il permet de conserver des identifiants publics stables :

```text
PROFILE-XXXXXX
```

Le même identifiant pseudonymisé doit toujours désigner le même provider interne dans les futures releases :

```text
TruthfulQA
behavioral 12 × 3 × 150
behavioral 12 × 3 × 450
repeatability
releases métier
```

## 10. Garde-fous de publication

Le script d’export public :

* publie uniquement des champs autorisés ;
* bloque les fuites de noms de providers ;
* bloque les fuites de noms de modèles ;
* refuse les champs de classement ;
* refuse les champs de rating ;
* refuse les champs de score composite ;
* exclut les réponses brutes ;
* exclut les traces individuelles par question ;
* exclut les justifications textuelles des juges ;
* génère des checksums SHA-256 ;
* génère une checklist de revue humaine.

Avant publication, vérifier :

```text
PUBLICATION_REVIEW_CHECKLIST.md
```

## 11. Vérifier les checksums

Depuis le dossier public figé :

```bash
sha256sum -c CHECKSUMS.sha256
```

Sous Windows PowerShell, inspecter le fichier de checksums et comparer les empreintes SHA-256 avec :

```powershell
Get-FileHash .\README_PUBLIC.md -Algorithm SHA256
```

Répéter si nécessaire pour chaque artefact public.

## 12. Règle d’interprétation publique

La release doit être interprétée comme une publication de profils multidimensionnels.

Elle ne doit pas être interprétée comme :

* un classement de providers ;
* un benchmark universel ;
* une certification ;
* une recommandation universelle de déploiement ;
* la preuve qu’un juge automatisé constitue une source absolue de vérité.

## 13. Règle de gouvernance

> NeoMundi publie des profils IA observables, auditables et reproductibles — pas des classements.
