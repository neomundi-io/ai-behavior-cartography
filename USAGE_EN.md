# NeoMundi — TruthfulQA Profile Cartography

## Usage guide

## 1. Purpose

This repository provides reproducible validation and publication tooling for the NeoMundi TruthfulQA profile-cartography methodology.

The public workflow is designed to expose pseudonymous, multidimensional AI profiles without publishing:

* provider names;
* model names;
* rankings;
* ratings;
* composite scores;
* raw responses;
* question-level traces;
* judge rationales.

## 2. Repository structure

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

## 3. Requirements

Recommended environment:

```text
Python 3.10+
pandas
```

Install dependencies:

```bash
python -m pip install pandas
```

## 4. Internal corpus structure

The validation scripts expect a local working directory structured as follows:

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

Expected file patterns:

```text
01_raw_results/
truthfulqa_<provider>_dg_results.csv

02_openai_judged/
truthfulqa_<provider>_judged.csv

03_mistral_judged/
truthfulqa_<provider>_mistral_judged.csv
```

The local source datasets are not included in the public repository.

## 5. Step 1 — Audit the corpus inventory

Run:

```bash
python audit_truthfulqa_inventory.py
```

Expected output directory:

```text
04_analysis_output/
```

Main generated reports:

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

Review first:

```text
audit_console_summary.txt
```

The audit verifies:

* file presence;
* row counts;
* `question_id` alignment;
* duplicate identifiers;
* response alignment;
* schema compatibility;
* missing verdicts.

## 6. Step 2 — Analyze double-judge agreement

Run:

```bash
python analyze_double_judge_truthfulqa.py
```

Expected output directory:

```text
04_analysis_output/double_judge_analysis/
```

Main generated reports:

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

Review first:

```text
analysis_console_summary.txt
```

The script computes:

* comparable judgment pairs;
* observed agreement;
* disagreement rate;
* pooled Cohen kappa;
* Cohen kappa by internal provider;
* confusion matrices;
* disagreement directions;
* runtime aggregations.

## 7. Step 3 — Analyze disagreement structure

Place the script in the frozen double-judge analysis directory, or specify the source directory explicitly.

Example:

```bash
python analyze_judge_disagreement_structure.py \
  --input-dir "./04_analysis_output/double_judge_analysis_v1_2026-06-06"
```

Main generated reports:

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

Review first:

```text
disagreement_structure_summary.txt
```

## 8. Step 4 — Generate a conservative public release

The publication script expects a frozen internal analysis directory containing:

```text
double_judge_summary_by_provider.csv
global_double_judge_summary.csv
comparable_pairs_internal.csv
```

Run:

```bash
python export_public_profiles.py
```

To rebuild an existing release:

```bash
python export_public_profiles.py --force
```

The script generates:

```text
public_release_truthfulqa_profiles_v1_2026-06-06/
_private_release_metadata/
```

### Public directory

The public directory contains:

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

### Private directory

The private directory contains:

```text
profile_mapping_private.csv
release_build_log_private.txt
```

Never publish the private directory.

## 9. Stable pseudonymous identifiers

The private mapping file must be preserved securely:

```text
_private_release_metadata/profile_mapping_private.csv
```

It enables stable public identifiers across future NeoMundi releases:

```text
PROFILE-XXXXXX
```

The same pseudonymous identifier should refer to the same internal provider across:

```text
TruthfulQA releases
behavioral 12 × 3 × 150 releases
behavioral 12 × 3 × 450 releases
repeatability releases
domain-specific releases
```

## 10. Publication safeguards

The public exporter:

* publishes whitelisted fields only;
* blocks provider-name leakage;
* blocks model-name leakage;
* rejects ranking fields;
* rejects rating fields;
* rejects composite-score fields;
* excludes raw responses;
* excludes question-level traces;
* excludes judge rationales;
* generates SHA-256 checksums;
* creates a manual publication checklist.

Before publication, review:

```text
PUBLICATION_REVIEW_CHECKLIST.md
```

## 11. Verify checksums

From the frozen public-release directory:

```bash
sha256sum -c CHECKSUMS.sha256
```

On Windows PowerShell, inspect the checksum file and compare SHA-256 values with:

```powershell
Get-FileHash .\README_PUBLIC.md -Algorithm SHA256
```

Repeat for each public artifact if needed.

## 12. Public interpretation rule

The public release must be interpreted as a multidimensional profile release.

It must not be interpreted as:

* a provider leaderboard;
* a universal benchmark;
* a certification;
* a universal deployment recommendation;
* proof that one automated judge is an absolute source of truth.

## 13. Governance rule

> NeoMundi publishes observable, auditable and reproducible AI profiles — not rankings.
