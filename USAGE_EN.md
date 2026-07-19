# NeoMundi AI Behavior Cartography — Usage Guide

🌐 **Language:** [English](./USAGE_EN.md) · [Français](./USAGE_FR.md)

📘 **Programme overview:** [English README](./README.md) · [README français](./README_FR.md)

📐 **Methodology:** [English](./Methodology_EN.md) · [Français](./Methodologie_FR.md)

🔬 **Open science:** [OPEN_SCIENCE.md](./OPEN_SCIENCE.md)

🌍 **NeoMundi:** [AI Observatory](https://github.com/neomundi-io/neomundi-ai-observatory) · [Weekly Barometer](https://github.com/neomundi-io/NeoMundi-Weekly-Barometer) · [English website](https://neomundi.org/en/home) · [Site français](https://neomundi.org/)

---

## 1. Purpose

This guide documents the public validation, analysis and publication workflow used by the **NeoMundi AI Behavior Cartography** programme.

The repository supports two distinct methodological tracks:

1. **Judged AI Behavior Cartography — `12 × 790`**
2. **Runtime Stability Cartography — `12 × 3 × 150`**

The public workflow is designed to produce de-identified, multidimensional AI behaviour profiles without publishing protected operational material.

The public release process does not publish, by default:

- provider names;
- model names;
- the private profile-mapping registry;
- rankings;
- ratings;
- universal composite scores;
- complete raw responses;
- complete protected prompts;
- question-level private traces;
- judge rationales;
- request IDs;
- trace IDs;
- raw API payloads;
- exact execution timestamps;
- API keys;
- infrastructure credentials;
- internal diagnostics;
- unpublished campaign exports.

> The public workflow publishes inspectable evidence, not the complete private measurement record.

---

## 2. Repository structure

The public repository is organised as follows:

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

The exact internal script names and release artefacts may evolve.

For a frozen release, the release README and manifest define the authoritative file inventory.

---

## 3. Requirements

Recommended environment:

```text
Python 3.10+
pandas
```

Some scripts may also require:

```text
numpy
scikit-learn
```

Install the minimum dependencies:

```bash
python -m pip install pandas numpy scikit-learn
```

For reproducible work, use a dedicated virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install dependencies:

```bash
python -m pip install pandas numpy scikit-learn
```

---

# Part I — Judged AI Behavior Cartography

## 4. Internal working structure for the `12 × 790` protocol

The judged protocol uses a local working directory similar to:

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

Typical internal file patterns:

```text
01_raw_results/
truthfulqa_<internal_provider>_dg_results.csv

02_openai_judged/
truthfulqa_<internal_provider>_judged.csv

03_mistral_judged/
truthfulqa_<internal_provider>_mistral_judged.csv
```

These local source datasets are not included in the public repository.

Internal provider identifiers must not appear in public release artefacts.

---

## 5. Step 1 — Audit the TruthfulQA inventory

Run:

```bash
python audit_truthfulqa_inventory.py
```

Expected output directory:

```text
04_analysis_output/
```

Typical generated reports:

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

The inventory audit should verify:

- source file presence;
- judged file presence;
- expected row counts;
- `question_id` alignment;
- duplicate identifiers;
- response alignment;
- schema compatibility;
- missing verdicts;
- malformed verdicts;
- missing profiles;
- unexpected columns.

Do not proceed to public export if critical alignment or coverage errors remain unresolved.

---

## 6. Step 2 — Analyse double-judge agreement

Run:

```bash
python analyze_double_judge_truthfulqa.py
```

Expected output directory:

```text
04_analysis_output/double_judge_analysis/
```

Typical generated reports:

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

The script should compute:

- total source responses;
- comparable judgment pairs;
- observed agreement;
- disagreement rate;
- pooled Cohen’s kappa;
- Cohen’s kappa by internal provider;
- confusion matrices;
- directional disagreement;
- positive-verdict rates by judge;
- coverage by profile;
- runtime aggregations where available.

Coverage must be reported together with agreement metrics.

---

## 7. Step 3 — Analyse disagreement structure

Run:

```bash
python analyze_judge_disagreement_structure.py \
  --input-dir "./04_analysis_output/double_judge_analysis"
```

Typical generated reports:

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

The analysis may be used to identify:

- directional judge asymmetry;
- high-friction questions;
- profile-level judge divergence;
- relationships between disagreement and runtime signals;
- recurrent methodological uncertainty zones.

These analyses remain exploratory unless explicitly qualified as robust.

---

## 8. Step 4 — Build the judged public release

The public exporter should use a frozen internal analysis directory containing, at minimum:

```text
double_judge_summary_by_provider.csv
global_double_judge_summary.csv
comparable_pairs_internal.csv
```

Typical command:

```bash
python export_public_profiles.py
```

To rebuild an existing release intentionally:

```bash
python export_public_profiles.py --force
```

The exporter may generate:

```text
public_release_truthfulqa_profiles/
_private_release_metadata/
```

### Public directory

Typical public artefacts:

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

### Private directory

Typical private artefacts:

```text
profile_mapping_private.csv
release_build_log_private.txt
```

Never publish the private directory.

---

# Part II — Runtime Stability Cartography

## 9. Internal working structure for the `12 × 3 × 150` protocol

The runtime protocol may use a working directory similar to:

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

A compatible structure may also use one consolidated execution file with explicit fields such as:

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

The exact schema is release-specific.

The release methodology and data dictionary define the authoritative field set.

---

## 10. Step 1 — Validate runtime inventory

The runtime inventory validation should check:

- 12 expected internal profiles;
- 3 expected waves;
- 150 expected questions;
- 5,400 planned executions;
- duplicate execution rows;
- missing profile-question-wave cells;
- malformed profile IDs;
- malformed wave IDs;
- missing question IDs;
- missing responses;
- missing or invalid metrics;
- inconsistent schemas between waves;
- coverage by profile;
- coverage by wave;
- coverage by question.

A typical command may be:

```bash
python validate_runtime_inventory.py
```

Expected outputs may include:

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

Review first:

```text
runtime_inventory_summary.txt
```

Do not proceed to analysis if critical cell coverage or schema errors remain unresolved.

---

## 11. Step 2 — Build runtime cartography

A typical command may be:

```bash
python build_runtime_cartography.py
```

The analysis should compute, where available:

- stability by profile;
- semantic variation by profile;
- coherence by profile;
- latency summaries;
- behavioural-regime distributions;
- inter-wave variation;
- coverage;
- completeness;
- `delta_g`;
- cost or token-consumption indicators where available.

Typical outputs may include:

```text
runtime_profile_summary.csv
runtime_question_summary.csv
runtime_wave_summary.csv
runtime_regime_distribution.csv
runtime_metric_contract.json
runtime_analysis_manifest.json
runtime_analysis_summary.txt
```

Review first:

```text
runtime_analysis_summary.txt
```

A difference between waves must not be presented as proof of a model update or provider-side change.

---

## 12. Step 3 — Build the runtime public release

A typical command may be:

```bash
python export_runtime_public_release.py
```

The public release may include:

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

The private build area may include:

```text
profile_mapping_private.csv
runtime_release_build_log_private.txt
private_execution_summary.csv
```

Never publish private mapping, private execution-level exports or internal build logs.

---

## 13. Stable de-identified profile identifiers

The private mapping file must be preserved securely.

Typical location:

```text
_private_release_metadata/profile_mapping_private.csv
```

It enables stable public identifiers:

```text
PROFILE-XXXXXX
```

The same public identifier should refer to the same observed system across compatible NeoMundi releases, including:

```text
TruthfulQA judged releases
runtime 12 × 3 × 150 releases
extended runtime releases
repeatability releases
domain-specific releases
monthly cartographies
```

The public release terminology is **de-identified**, not irreversibly anonymous.

---

## 14. Publication safeguards

The public exporter should:

- publish whitelisted fields only;
- block provider-name leakage;
- block model-name leakage;
- reject ranking fields;
- reject rating fields;
- reject universal composite-score fields;
- exclude protected raw responses;
- exclude protected prompts;
- exclude question-level private traces;
- exclude private judge rationales;
- exclude request IDs;
- exclude trace IDs;
- exclude exact execution timestamps;
- exclude private cost details;
- generate a public data dictionary;
- generate a release manifest;
- generate SHA-256 checksums;
- create a manual publication checklist.

Before publication, review:

```text
PUBLICATION_REVIEW_CHECKLIST.md
```

Manual review is mandatory even when the exporter passes all automated checks.

---

## 15. Verify checksums

From the frozen public-release directory:

```bash
sha256sum -c CHECKSUMS.sha256
```

On Windows PowerShell:

```powershell
Get-FileHash .\README.md -Algorithm SHA256
```

Repeat for each public artefact as needed and compare the output with `CHECKSUMS.sha256`.

A checksum mismatch must be resolved before publication.

---

## 16. Verify public-field boundaries

Before committing a release, search the public directory for:

```text
provider names
model names
internal profile IDs
API keys
request IDs
trace IDs
raw responses
private mapping fields
ranking fields
rating fields
composite-score fields
```

Example recursive searches:

```bash
grep -Rni "provider_name" .
grep -Rni "model_name" .
grep -Rni "request_id" .
grep -Rni "trace_id" .
grep -Rni "profile_mapping" .
```

On PowerShell:

```powershell
Get-ChildItem -Recurse -File | Select-String -Pattern "provider_name"
Get-ChildItem -Recurse -File | Select-String -Pattern "model_name"
Get-ChildItem -Recurse -File | Select-String -Pattern "request_id"
Get-ChildItem -Recurse -File | Select-String -Pattern "trace_id"
Get-ChildItem -Recurse -File | Select-String -Pattern "profile_mapping"
```

These checks complement, but do not replace, manual review.

---

## 17. Freeze a public release

Before publication:

1. confirm the methodology version;
2. confirm the release directory name;
3. confirm the public file inventory;
4. confirm coverage figures;
5. confirm de-identification;
6. verify checksums;
7. review the publication checklist;
8. confirm that no protected fields are present;
9. record the publication date;
10. commit the release with a descriptive message.

A frozen release should not be silently modified.

Corrections should use:

- a new version;
- a correction note;
- an amended manifest;
- regenerated checksums;
- a documented change log.

---

## 18. Public interpretation rule

Each release must be interpreted as a multidimensional measurement release.

It must not be interpreted as:

- a provider leaderboard;
- a model leaderboard;
- a universal benchmark;
- a universal quality score;
- a safety certification;
- a regulatory determination;
- a deployment authorisation;
- proof that one automated judge is an absolute source of truth;
- proof that stability implies factual correctness;
- proof that variability implies factual error.

The appropriate formulation is:

> A behavioural property or difference was observed under the conditions of the protocol.

---

## 19. Protocol-specific interpretation

### Judged Cartography — `12 × 790`

Use this protocol to analyse:

- stability across a broad factual corpus;
- factuality according to separate judges;
- judge agreement;
- judge disagreement;
- calibration asymmetry;
- corpus-specific factual evaluation.

Do not use it as a universal deployment recommendation.

### Runtime Cartography — `12 × 3 × 150`

Use this protocol to analyse:

- repeated runtime behaviour;
- inter-wave variation;
- semantic variation;
- coherence;
- latency;
- behavioural regimes;
- coverage.

Do not use it as proof of factual correctness or provider-side causal change.

---

## 20. Governance rule

> NeoMundi publishes observable, auditable and reproducible AI behaviour profiles — not rankings.

The public workflow preserves:

- methodological separation;
- de-identification;
- evidence integrity;
- interpretation boundaries;
- protected operational assets;
- release traceability.

A signal is evidence to be interpreted, not a verdict.
