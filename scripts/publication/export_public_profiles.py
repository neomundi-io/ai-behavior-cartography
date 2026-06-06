#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
export_public_profiles.py

Construit une release publique pseudonymisée à partir de l'analyse interne figée
TruthfulQA double-jugée NeoMundi.

OBJECTIFS
---------
- Importer les résultats internes figés.
- Créer ou réutiliser une pseudonymisation stable.
- Ne publier aucun nom de provider ou de modèle.
- Exposer des profils descriptifs, jamais un classement.
- Sélectionner les colonnes par whitelist stricte.
- Refuser toute colonne interdite.
- Scanner les exports publics pour détecter une fuite éventuelle.
- Autoriser les README à documenter explicitement les pratiques interdites.
- Générer un manifeste, un dictionnaire de données, un README public et des checksums.
- Conserver la table de correspondance dans un dossier privé séparé.

ARBORESCENCE CONSEILLÉE
----------------------
double_judge_analysis_v1_2026-06-06/
├── README_INTERNAL_ANALYSIS.md
├── double_judge_summary_by_provider.csv
├── global_double_judge_summary.csv
├── comparable_pairs_internal.csv
├── judge_disagreement_structure/
│   └── disagreement_by_provider.csv
└── export_public_profiles.py

UTILISATION SIMPLE
------------------
Depuis le dossier figé :

    python .\export_public_profiles.py

Le script créera par défaut, à côté du dossier figé :

    public_release_truthfulqa_profiles_v1_2026-06-06/
    _private_release_metadata/

UTILISATION AVEC CHEMINS EXPLICITES
----------------------------------
    python .\export_public_profiles.py `
        --input-dir ".\double_judge_analysis_v1_2026-06-06" `
        --output-dir ".\public_release_truthfulqa_profiles_v1_2026-06-06"

MODE DE PUBLICATION
-------------------
Le mode par défaut est "conservative" :
- taux arrondis ;
- volumes par profils publiés sous forme de tranches ;
- aucune ligne question-level ;
- aucune réponse brute ;
- aucune justification de juge ;
- aucune matrice de désaccord détaillée par provider ;
- distributions runtime limitées aux catégories suffisamment représentées.

Un mode "detailed" existe pour une release publique plus riche, après revue humaine :

    python .\export_public_profiles.py --mode detailed

IMPORTANT
---------
La pseudonymisation n'est pas une anonymisation absolue. Une combinaison rare de
métriques peut permettre une ré-identification par triangulation. Toute publication
doit faire l'objet d'une revue humaine avant mise en ligne.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import secrets
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

VERSION = "1.0.3"
DEFAULT_ANALYSIS_DIR_NAME = "double_judge_analysis_v1_2026-06-06"
DEFAULT_PUBLIC_DIR_NAME = "public_release_truthfulqa_profiles_v1_2026-06-06"
DEFAULT_PRIVATE_DIR_NAME = "_private_release_metadata"

SUMMARY_FILE = "double_judge_summary_by_provider.csv"
GLOBAL_FILE = "global_double_judge_summary.csv"
PAIRS_FILE = "comparable_pairs_internal.csv"
STRUCTURE_PROVIDER_FILE = Path("judge_disagreement_structure") / "disagreement_by_provider.csv"

MAPPING_FILE = "profile_mapping_private.csv"
BUILD_LOG_FILE = "release_build_log_private.txt"

PUBLIC_FILES = [
    "README_PUBLIC.md",
    "public_profile_summary.csv",
    "public_runtime_profile_summary.csv",
    "public_methodology_validation.csv",
    "public_data_dictionary.csv",
    "PUBLICATION_REVIEW_CHECKLIST.md",
    "RELEASE_MANIFEST.json",
    "CHECKSUMS.sha256",
]

# Colonnes interdites : défense en profondeur.
FORBIDDEN_COLUMN_PATTERNS = [
    r"(^|_)rank($|_)",
    r"(^|_)ranking($|_)",
    r"leaderboard",
    r"best",
    r"worst",
    r"rating",
    r"grade",
    r"aaa",
    r"bbb",
    r"composite",
    r"final_score",
    r"score_total",
    r"provider_name",
    r"model_name",
    r"vendor",
    r"company",
    r"endpoint",
    r"api_key",
    r"raw_response",
    r"response_text",
    r"judge_reason",
]

# Mots interdits dans les contenus publics.
FORBIDDEN_CONTENT_PATTERNS = [
    r"\bleaderboard\b",
    r"\branking\b",
    r"\bbest model\b",
    r"\bworst model\b",
    r"\bAAA\b",
    r"\bBBB\b",
]

# Providers connus dans ce corpus. Ils sont détectés dynamiquement depuis
# les sources internes, mais cette liste protège aussi contre des fuites
# dans des textes statiques.
KNOWN_PROVIDER_TOKENS = [
    "anthropic",
    "apertus",
    "cohere",
    "deepseek",
    "google",
    "infomaniak",
    "mistral",
    "openai",
    "perplexity",
    "qwen",
    "together",
    "xai",
]

PROFILE_PREFIX = "PROFILE"

RUNTIME_DISTRIBUTION_COLUMNS = [
    "decision",
    "regime",
    "dg_profile",
]

RUNTIME_RATE_COLUMNS = [
    "dg_flagged",
    "flagged",
]

MIN_CATEGORY_COUNT_CONSERVATIVE = 50
ROUND_DIGITS_CONSERVATIVE = 3
ROUND_DIGITS_DETAILED = 4


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def normalize_column_name(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def normalize_scalar(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def normalize_bool(value: object) -> Optional[bool]:
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return value
    text = normalize_scalar(value).lower()
    if text in {"true", "1", "yes", "y", "correct", "allow", "flag"}:
        return True
    if text in {"false", "0", "no", "n", "incorrect"}:
        return False
    return None


def safe_float(value: object) -> float:
    try:
        result = float(value)
        if math.isnan(result):
            return float("nan")
        return result
    except (TypeError, ValueError):
        return float("nan")


def safe_div(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator else float("nan")


def round_or_blank(value: object, digits: int) -> object:
    number = safe_float(value)
    if math.isnan(number):
        return ""
    return round(number, digits)


def read_csv_flexible(path: Path) -> pd.DataFrame:
    attempts: list[str] = []
    for encoding in ["utf-8-sig", "utf-8", "cp1252", "latin-1"]:
        for separator in [",", ";", "\t"]:
            try:
                df = pd.read_csv(path, encoding=encoding, sep=separator, low_memory=False)
                if len(df.columns) > 1:
                    return df
                attempts.append(f"{encoding}/{repr(separator)}: une colonne")
            except Exception as exc:  # noqa: BLE001
                attempts.append(f"{encoding}/{repr(separator)}: {type(exc).__name__}")

    for encoding in ["utf-8-sig", "utf-8", "cp1252", "latin-1"]:
        try:
            return pd.read_csv(path, encoding=encoding, sep=None, engine="python")
        except Exception as exc:  # noqa: BLE001
            attempts.append(f"{encoding}/auto: {type(exc).__name__}")

    raise RuntimeError(f"Impossible de lire {path}. Essais : {' | '.join(attempts)}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_input_dir(explicit: Optional[Path]) -> Path:
    if explicit:
        candidate = explicit.expanduser().resolve()
        if (candidate / SUMMARY_FILE).exists() and (candidate / PAIRS_FILE).exists():
            return candidate
        raise FileNotFoundError(
            f"Le dossier indiqué ne contient pas {SUMMARY_FILE} et {PAIRS_FILE} : {candidate}"
        )

    cwd = Path.cwd().resolve()

    if (cwd / SUMMARY_FILE).exists() and (cwd / PAIRS_FILE).exists():
        return cwd

    candidates = [
        cwd / DEFAULT_ANALYSIS_DIR_NAME,
        cwd / "04_analysis_output" / DEFAULT_ANALYSIS_DIR_NAME,
        cwd / "04_analysis_output" / "double_judge_analysis",
    ]

    for candidate in candidates:
        if (candidate / SUMMARY_FILE).exists() and (candidate / PAIRS_FILE).exists():
            return candidate.resolve()

    found = sorted(
        {
            path.parent.resolve()
            for path in cwd.rglob(SUMMARY_FILE)
            if (path.parent / PAIRS_FILE).exists()
        }
    )

    if len(found) == 1:
        return found[0]

    if not found:
        raise FileNotFoundError(
            f"Aucun dossier contenant {SUMMARY_FILE} et {PAIRS_FILE} n'a été trouvé depuis {cwd}"
        )

    formatted = "\n".join(f"  - {candidate}" for candidate in found)
    raise RuntimeError(
        "Plusieurs dossiers d'analyse détectés. Relance avec --input-dir.\n" + formatted
    )


def make_profile_id(existing_ids: set[str]) -> str:
    while True:
        token = secrets.token_hex(3).upper()
        profile_id = f"{PROFILE_PREFIX}-{token}"
        if profile_id not in existing_ids:
            return profile_id


def sample_bucket(n: int) -> str:
    if n < 650:
        return "<650"
    if n < 700:
        return "650-699"
    if n < 750:
        return "700-749"
    if n < 780:
        return "750-779"
    if n < 800:
        return "780-799"
    return "800+"


def reject_forbidden_columns(df: pd.DataFrame, label: str) -> None:
    forbidden = []
    for column in df.columns:
        normalized = normalize_column_name(column)
        for pattern in FORBIDDEN_COLUMN_PATTERNS:
            if re.search(pattern, normalized, flags=re.IGNORECASE):
                forbidden.append(str(column))
                break

    if forbidden:
        raise RuntimeError(
            f"Export refusé pour {label}. Colonnes interdites détectées : {forbidden}"
        )


def scan_provider_tokens(text: str, providers: Iterable[str], label: str) -> list[str]:
    """
    Recherche les noms de providers dans tous les fichiers publics.
    Cette vérification reste stricte, y compris dans les README et manifests.
    """
    findings: list[str] = []
    lower_text = text.lower()

    for provider in sorted(set(providers) | set(KNOWN_PROVIDER_TOKENS)):
        token = provider.strip().lower()
        if token and re.search(rf"(?<![a-z0-9_]){re.escape(token)}(?![a-z0-9_])", lower_text):
            findings.append(f"{label}: token provider interdit détecté : {provider}")

    return findings


def scan_forbidden_structured_content(text: str, label: str) -> list[str]:
    """
    Recherche les marqueurs de classement uniquement dans les exports structurés.
    Les README et checklists peuvent légitimement expliquer que les classements
    sont interdits ; ils ne doivent donc pas être bloqués pour cette raison.
    """
    findings: list[str] = []

    for pattern in FORBIDDEN_CONTENT_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            findings.append(f"{label}: motif interdit détecté : {pattern}")

    return findings


def scan_public_directory_for_leaks(output_dir: Path, providers: Iterable[str]) -> list[str]:
    findings: list[str] = []

    for path in sorted(output_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name == "CHECKSUMS.sha256":
            # Ce fichier ne contient que les hashes des autres fichiers.
            continue
        if path.suffix.lower() not in {".csv", ".md", ".json", ".txt"}:
            continue

        text = path.read_text(encoding="utf-8-sig", errors="replace")

        # Les noms de providers sont interdits dans tous les fichiers publics.
        findings.extend(scan_provider_tokens(text, providers, path.name))

        # Les marqueurs de classement sont interdits dans les exports de données.
        # Ils restent autorisés dans les documents explicatifs lorsqu'ils décrivent
        # précisément les pratiques exclues.
        if path.suffix.lower() == ".csv":
            findings.extend(scan_forbidden_structured_content(text, path.name))

    return findings


def write_checksums(output_dir: Path) -> None:
    rows = []
    for path in sorted(output_dir.iterdir()):
        if not path.is_file():
            continue
        if path.name == "CHECKSUMS.sha256":
            continue
        rows.append(f"{sha256_file(path)}  {path.name}")

    (output_dir / "CHECKSUMS.sha256").write_text(
        "\n".join(rows) + "\n",
        encoding="utf-8",
    )


def category_distribution_json(
    df: pd.DataFrame,
    column: str,
    mode: str,
    min_category_count: int,
    digits: int,
) -> str:
    if column not in df.columns:
        return "{}"

    series = df[column].map(lambda value: normalize_scalar(value) or "<missing>")
    counts = series.value_counts(dropna=False)
    total = int(counts.sum())

    distribution: dict[str, object] = {}
    suppressed_count = 0

    for category, count in counts.items():
        category_text = str(category)
        count_int = int(count)

        if mode == "conservative" and count_int < min_category_count:
            suppressed_count += count_int
            continue

        distribution[category_text] = round(safe_div(count_int, total), digits)

    if suppressed_count:
        distribution["<other_or_suppressed>"] = round(
            safe_div(suppressed_count, total),
            digits,
        )

    return json.dumps(distribution, ensure_ascii=False, sort_keys=True)


def boolean_rate(df: pd.DataFrame, column: str, digits: int) -> object:
    if column not in df.columns:
        return ""

    parsed = df[column].map(normalize_bool).dropna()
    if parsed.empty:
        return ""

    return round(float(parsed.astype(bool).mean()), digits)


def nonzero_rate(df: pd.DataFrame, column: str, digits: int) -> object:
    """
    Calcule la part des valeurs strictement supérieures à zéro.

    Tolère les nombres déjà numériques et les chaînes utilisant une virgule
    décimale, par exemple "0,2". Refuse silencieusement les valeurs manquantes,
    mais lève une erreur lorsque la colonne existe, contient des valeurs et
    qu'aucune valeur n'est interprétable.
    """
    if column not in df.columns:
        return ""

    raw = df[column]
    non_missing = raw.dropna()

    if non_missing.empty:
        return ""

    normalized = (
        non_missing.astype(str)
        .str.strip()
        .str.replace(",", ".", regex=False)
    )

    numeric = pd.to_numeric(normalized, errors="coerce").dropna()

    if numeric.empty:
        sample = " | ".join(normalized.head(5).tolist())
        raise RuntimeError(
            f"Colonne {column} présente mais aucune valeur numérique interprétable. "
            f"Exemples : {sample}"
        )

    return round(float((numeric > 0).mean()), digits)


# ---------------------------------------------------------------------------
# Mapping privé
# ---------------------------------------------------------------------------

def load_or_create_mapping(
    providers: list[str],
    private_dir: Path,
) -> tuple[pd.DataFrame, Path, bool]:
    private_dir.mkdir(parents=True, exist_ok=True)
    mapping_path = private_dir / MAPPING_FILE
    created = False

    if mapping_path.exists():
        mapping = read_csv_flexible(mapping_path)

        required = {"provider", "profile_id"}
        if not required.issubset(set(mapping.columns)):
            raise RuntimeError(
                f"Le mapping privé existant est invalide : colonnes attendues {sorted(required)}"
            )
    else:
        mapping = pd.DataFrame(columns=["provider", "profile_id", "created_at"])
        created = True

    existing_provider_to_profile = {
        str(row["provider"]): str(row["profile_id"])
        for _, row in mapping.iterrows()
    }

    existing_ids = set(existing_provider_to_profile.values())
    now = datetime.now().isoformat(timespec="seconds")
    new_rows = []

    for provider in sorted(providers):
        if provider in existing_provider_to_profile:
            continue

        profile_id = make_profile_id(existing_ids)
        existing_ids.add(profile_id)

        new_rows.append(
            {
                "provider": provider,
                "profile_id": profile_id,
                "created_at": now,
            }
        )

    if new_rows:
        mapping = pd.concat([mapping, pd.DataFrame(new_rows)], ignore_index=True)
        created = True

    # Défense : un provider ne doit pointer que vers un seul profil et inversement.
    if mapping["provider"].duplicated().any():
        raise RuntimeError("Le mapping privé contient des providers dupliqués.")

    if mapping["profile_id"].duplicated().any():
        raise RuntimeError("Le mapping privé contient des profile_id dupliqués.")

    mapping = mapping.sort_values("provider", kind="stable").reset_index(drop=True)
    mapping.to_csv(mapping_path, index=False, encoding="utf-8-sig")

    return mapping, mapping_path, created


# ---------------------------------------------------------------------------
# Construction des exports publics
# ---------------------------------------------------------------------------

def build_profile_summary(
    summary_df: pd.DataFrame,
    mapping_df: pd.DataFrame,
    mode: str,
) -> pd.DataFrame:
    digits = ROUND_DIGITS_CONSERVATIVE if mode == "conservative" else ROUND_DIGITS_DETAILED

    merged = summary_df.merge(mapping_df[["provider", "profile_id"]], on="provider", how="left")

    required_columns = [
        "provider",
        "profile_id",
        "n_comparable_pairs",
        "observed_agreement_rate",
        "disagreement_rate",
        "cohen_kappa",
        "openai_correct_rate",
        "mistral_correct_rate",
        "mistral_minus_openai_correct_rate",
    ]

    missing = [column for column in required_columns if column not in merged.columns]
    if missing:
        raise RuntimeError(f"Colonnes internes attendues absentes du résumé : {missing}")

    public_rows = []

    for _, row in merged.iterrows():
        n = int(row["n_comparable_pairs"])

        public_row = {
            "profile_id": row["profile_id"],
            "observation_count_bucket": sample_bucket(n),
            "judge_observed_agreement_rate": round_or_blank(row["observed_agreement_rate"], digits),
            "judge_disagreement_rate": round_or_blank(row["disagreement_rate"], digits),
            "cohen_kappa": round_or_blank(row["cohen_kappa"], digits),
            "judge_a_positive_rate": round_or_blank(row["openai_correct_rate"], digits),
            "judge_b_positive_rate": round_or_blank(row["mistral_correct_rate"], digits),
            "judge_b_minus_judge_a_positive_rate": round_or_blank(
                row["mistral_minus_openai_correct_rate"],
                digits,
            ),
        }

        if mode == "detailed":
            public_row["n_comparable_pairs"] = n

        public_rows.append(public_row)

    result = pd.DataFrame(public_rows).sort_values("profile_id", kind="stable")
    reject_forbidden_columns(result, "public_profile_summary.csv")
    return result.reset_index(drop=True)


def build_runtime_summary(
    pairs_df: pd.DataFrame,
    mapping_df: pd.DataFrame,
    mode: str,
) -> pd.DataFrame:
    digits = ROUND_DIGITS_CONSERVATIVE if mode == "conservative" else ROUND_DIGITS_DETAILED
    min_count = MIN_CATEGORY_COUNT_CONSERVATIVE if mode == "conservative" else 1

    merged = pairs_df.merge(mapping_df[["provider", "profile_id"]], on="provider", how="left")

    rows = []

    for profile_id, group in merged.groupby("profile_id", dropna=False):
        row = {
            "profile_id": profile_id,
            "observation_count_bucket": sample_bucket(len(group)),
            "decision_distribution": category_distribution_json(
                group,
                "decision",
                mode=mode,
                min_category_count=min_count,
                digits=digits,
            ),
            "regime_distribution": category_distribution_json(
                group,
                "regime",
                mode=mode,
                min_category_count=min_count,
                digits=digits,
            ),
            "dg_profile_distribution": category_distribution_json(
                group,
                "dg_profile",
                mode=mode,
                min_category_count=min_count,
                digits=digits,
            ),
            "dg_flagged_rate": boolean_rate(group, "dg_flagged", digits),
            "flagged_rate": boolean_rate(group, "flagged", digits),
            "hallucination_nonzero_rate": nonzero_rate(group, "hallucination", digits),
        }

        if mode == "detailed":
            row["n_runtime_observations"] = int(len(group))

        rows.append(row)

    result = pd.DataFrame(rows).sort_values("profile_id", kind="stable")
    reject_forbidden_columns(result, "public_runtime_profile_summary.csv")
    return result.reset_index(drop=True)


def reject_fully_empty_public_columns(df: pd.DataFrame, label: str) -> None:
    """
    Bloque une release lorsqu'une colonne de métrique publique est entièrement vide.
    Les identifiants et tranches d'observations sont exclus de ce contrôle.
    """
    exempt = {"profile_id", "observation_count_bucket"}
    fully_empty = []

    for column in df.columns:
        if column in exempt:
            continue

        series = df[column]
        if series.isna().all() or series.astype(str).str.strip().isin({"", "nan", "None"}).all():
            fully_empty.append(column)

    if fully_empty:
        raise RuntimeError(
            f"Export refusé pour {label}. Colonnes publiques entièrement vides : {fully_empty}"
        )


def build_methodology_validation(
    global_df: pd.DataFrame,
    provider_count: int,
    mode: str,
) -> pd.DataFrame:
    if len(global_df) != 1:
        raise RuntimeError(
            f"{GLOBAL_FILE} doit contenir exactement une ligne. Lignes détectées : {len(global_df)}"
        )

    digits = ROUND_DIGITS_CONSERVATIVE if mode == "conservative" else ROUND_DIGITS_DETAILED
    row = global_df.iloc[0]

    fields = [
        ("methodology_name", "TruthfulQA double-judge factual evaluation"),
        ("release_mode", mode),
        ("profile_count", provider_count),
        ("n_comparable_pairs", int(row["n_comparable_pairs"])),
        ("judge_observed_agreement_rate", round_or_blank(row["observed_agreement_rate"], digits)),
        ("judge_disagreement_rate", round_or_blank(row["disagreement_rate"], digits)),
        ("cohen_kappa_pooled", round_or_blank(row["cohen_kappa"], digits)),
        ("judge_a_positive_rate", round_or_blank(row["openai_correct_rate"], digits)),
        ("judge_b_positive_rate", round_or_blank(row["mistral_correct_rate"], digits)),
        (
            "judge_b_minus_judge_a_positive_rate",
            round_or_blank(row["mistral_minus_openai_correct_rate"], digits),
        ),
        (
            "interpretation_note",
            (
                "Judge A and Judge B are presented separately. No consolidated verdict "
                "is treated as absolute truth. Runtime signals remain distinct from factual evaluation."
            ),
        ),
    ]

    result = pd.DataFrame(fields, columns=["metric", "value"])
    reject_forbidden_columns(result, "public_methodology_validation.csv")
    return result


def build_data_dictionary(mode: str) -> pd.DataFrame:
    rows = [
        {
            "file": "public_profile_summary.csv",
            "field": "profile_id",
            "description": "Stable pseudonymous profile identifier. Private mapping is not included in the public release.",
        },
        {
            "file": "public_profile_summary.csv",
            "field": "observation_count_bucket",
            "description": "Bucketed number of comparable factual-evaluation pairs for the profile.",
        },
        {
            "file": "public_profile_summary.csv",
            "field": "judge_observed_agreement_rate",
            "description": "Share of comparable pairs on which Judge A and Judge B produce the same binary verdict.",
        },
        {
            "file": "public_profile_summary.csv",
            "field": "judge_disagreement_rate",
            "description": "Share of comparable pairs on which Judge A and Judge B produce different binary verdicts.",
        },
        {
            "file": "public_profile_summary.csv",
            "field": "cohen_kappa",
            "description": "Inter-judge agreement coefficient corrected for agreement expected by chance.",
        },
        {
            "file": "public_profile_summary.csv",
            "field": "judge_a_positive_rate",
            "description": "Share of comparable pairs receiving a positive verdict from Judge A.",
        },
        {
            "file": "public_profile_summary.csv",
            "field": "judge_b_positive_rate",
            "description": "Share of comparable pairs receiving a positive verdict from Judge B.",
        },
        {
            "file": "public_profile_summary.csv",
            "field": "judge_b_minus_judge_a_positive_rate",
            "description": "Difference between the positive-verdict rates produced by Judge B and Judge A.",
        },
        {
            "file": "public_runtime_profile_summary.csv",
            "field": "decision_distribution",
            "description": "JSON distribution of runtime decisions for the pseudonymous profile.",
        },
        {
            "file": "public_runtime_profile_summary.csv",
            "field": "regime_distribution",
            "description": "JSON distribution of runtime regimes for the pseudonymous profile.",
        },
        {
            "file": "public_runtime_profile_summary.csv",
            "field": "dg_profile_distribution",
            "description": "JSON distribution of runtime ΔG profile categories for the pseudonymous profile.",
        },
        {
            "file": "public_runtime_profile_summary.csv",
            "field": "dg_flagged_rate",
            "description": "Share of observations with a positive ΔG flag, when available.",
        },
        {
            "file": "public_runtime_profile_summary.csv",
            "field": "flagged_rate",
            "description": "Share of observations carrying a generic flag, when available.",
        },
        {
            "file": "public_runtime_profile_summary.csv",
            "field": "hallucination_nonzero_rate",
            "description": "Share of observations with a non-zero hallucination signal, when available.",
        },
        {
            "file": "public_methodology_validation.csv",
            "field": "interpretation_note",
            "description": "Public guardrail: factual judges remain separate and runtime signals are not merged into a composite score.",
        },
        {
            "file": "public_runtime_profile_summary.csv",
            "field": "profile_id",
            "description": "Stable pseudonymous profile identifier. Private mapping is not included in the public release.",
        },
        {
            "file": "public_runtime_profile_summary.csv",
            "field": "observation_count_bucket",
            "description": "Bucketed number of runtime observations for the profile.",
        },
        {
            "file": "public_methodology_validation.csv",
            "field": "metric",
            "description": "Name of the public methodology-validation indicator.",
        },
        {
            "file": "public_methodology_validation.csv",
            "field": "value",
            "description": "Public value associated with the methodology-validation indicator.",
        },
    ]

    if mode == "detailed":
        rows.append(
            {
                "file": "public_profile_summary.csv",
                "field": "n_comparable_pairs",
                "description": "Exact number of comparable factual-evaluation pairs. Detailed mode only.",
            }
        )

    result = pd.DataFrame(rows)
    reject_forbidden_columns(result, "public_data_dictionary.csv")
    return result


def public_readme(mode: str) -> str:
    return f"""# NeoMundi — Public TruthfulQA Behavioral Profiles

## Scope

This release presents pseudonymous, multidimensional profiles derived from a double-judge factual-evaluation protocol and runtime behavioral signals.

It is designed to support auditability, methodological transparency and discussion of AI behavioral differences without publishing a provider leaderboard.

## What this release contains

- `public_profile_summary.csv`
- `public_runtime_profile_summary.csv`
- `public_methodology_validation.csv`
- `public_data_dictionary.csv`
- `PUBLICATION_REVIEW_CHECKLIST.md`
- `RELEASE_MANIFEST.json`
- `CHECKSUMS.sha256`

## Release mode

```text
{mode}
```

The default conservative mode:
- publishes stable pseudonymous profile identifiers;
- rounds rates;
- publishes observation volumes as buckets;
- suppresses low-frequency runtime categories;
- excludes question-level traces;
- excludes raw answers;
- excludes judge rationales;
- excludes provider and model names;
- excludes any composite rating or leaderboard.

## Interpretation

The factual-evaluation layer is intentionally presented as separate views from two judges:

- `judge_a_positive_rate`
- `judge_b_positive_rate`
- `judge_observed_agreement_rate`
- `judge_disagreement_rate`
- `cohen_kappa`

No consolidated binary verdict is treated as absolute truth.

Runtime signals are published as separate behavioral dimensions:

- runtime decision distribution;
- runtime regime distribution;
- ΔG profile distribution;
- runtime flag rates;
- hallucination-signal rate.

They are not merged into a single quality score.

## Important limitations

Pseudonymization is not absolute anonymization. Rare combinations of metrics can create re-identification risk through triangulation.

This release must not be used:
- as a provider leaderboard;
- as a universal model-performance benchmark;
- as proof that one factual judge is an absolute reference;
- as a substitute for domain-specific validation;
- as a substitute for human adjudication in high-risk use cases.

## Methodological direction

Planned extensions include:
- an independent third judge;
- intra-judge repeatability analysis;
- a stratified human-adjudication panel;
- replication on additional factual and domain-specific corpora;
- separate behavioral-cartography analyses on repeated-run panels.

## Governance rule

NeoMundi publishes observable profiles, not rankings.
"""


def publication_checklist() -> str:
    return """# Publication review checklist

This checklist must be reviewed manually before publication.

## Identity leakage

- [ ] No provider name is present in any public file.
- [ ] No model name is present in any public file.
- [ ] No private mapping file is present in the public directory.
- [ ] No source path is present in the public manifest.
- [ ] No raw response is present in the public directory.
- [ ] No question-level trace is present in the public directory.
- [ ] No judge rationale is present in the public directory.

## Ranking leakage

- [ ] No rank column is present.
- [ ] No rating column is present.
- [ ] No grade column is present.
- [ ] No composite score is present.
- [ ] No best / worst wording is present.
- [ ] No leaderboard wording is present.

## Re-identification review

- [ ] Profile-level rates have been reviewed for triangulation risk.
- [ ] Rare runtime categories have been suppressed or grouped.
- [ ] Observation volumes are bucketed unless a detailed release was explicitly approved.
- [ ] The public release has been compared against earlier public artifacts for accidental re-identification clues.

## Methodology

- [ ] The README states that pseudonymization is not anonymization.
- [ ] The README states that the judges are presented separately.
- [ ] The README states that runtime signals are not merged into a composite score.
- [ ] The README states that the release is not a universal benchmark.
- [ ] Checksums have been generated.
"""


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build_release(
    input_dir: Path,
    output_dir: Path,
    private_dir: Path,
    mode: str,
    force: bool,
) -> int:
    if mode not in {"conservative", "detailed"}:
        raise ValueError("Mode inconnu. Choisir conservative ou detailed.")

    if output_dir.exists():
        if not force:
            raise FileExistsError(
                f"Le dossier public existe déjà : {output_dir}\n"
                "Relance avec --force uniquement si tu souhaites le reconstruire."
            )
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    private_dir.mkdir(parents=True, exist_ok=True)

    summary_path = input_dir / SUMMARY_FILE
    global_path = input_dir / GLOBAL_FILE
    pairs_path = input_dir / PAIRS_FILE

    for path in [summary_path, global_path, pairs_path]:
        if not path.exists():
            raise FileNotFoundError(f"Fichier interne requis absent : {path}")

    summary_df = read_csv_flexible(summary_path)
    global_df = read_csv_flexible(global_path)
    pairs_df = read_csv_flexible(pairs_path)

    required_summary = {"provider", "n_comparable_pairs"}
    required_pairs = {"provider"}

    if not required_summary.issubset(set(summary_df.columns)):
        raise RuntimeError(
            f"{SUMMARY_FILE} doit contenir : {sorted(required_summary)}"
        )

    if not required_pairs.issubset(set(pairs_df.columns)):
        raise RuntimeError(
            f"{PAIRS_FILE} doit contenir : {sorted(required_pairs)}"
        )

    providers_summary = sorted(summary_df["provider"].dropna().astype(str).unique())
    providers_pairs = sorted(pairs_df["provider"].dropna().astype(str).unique())

    if providers_summary != providers_pairs:
        raise RuntimeError(
            "Les providers du résumé et des paires comparables ne correspondent pas exactement."
        )

    providers = providers_summary
    mapping_df, mapping_path, mapping_changed = load_or_create_mapping(providers, private_dir)

    profile_summary = build_profile_summary(summary_df, mapping_df, mode)
    runtime_summary = build_runtime_summary(pairs_df, mapping_df, mode)

    reject_fully_empty_public_columns(
        profile_summary,
        "public_profile_summary.csv",
    )
    reject_fully_empty_public_columns(
        runtime_summary,
        "public_runtime_profile_summary.csv",
    )

    methodology_validation = build_methodology_validation(global_df, len(providers), mode)
    data_dictionary = build_data_dictionary(mode)

    profile_summary.to_csv(
        output_dir / "public_profile_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    runtime_summary.to_csv(
        output_dir / "public_runtime_profile_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    methodology_validation.to_csv(
        output_dir / "public_methodology_validation.csv",
        index=False,
        encoding="utf-8-sig",
    )

    data_dictionary.to_csv(
        output_dir / "public_data_dictionary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    (output_dir / "README_PUBLIC.md").write_text(
        public_readme(mode),
        encoding="utf-8",
    )

    (output_dir / "PUBLICATION_REVIEW_CHECKLIST.md").write_text(
        publication_checklist(),
        encoding="utf-8",
    )

    # Manifest volontairement sans chemins sources ni noms de providers.
    manifest = {
        "release_name": output_dir.name,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "generator": "export_public_profiles.py",
        "generator_version": VERSION,
        "release_mode": mode,
        "profile_count": int(len(profile_summary)),
        "methodology": "TruthfulQA double-judge factual evaluation with separate runtime behavioral dimensions",
        "publication_principles": [
            "Pseudonymous profiles only",
            "No provider names",
            "No model names",
            "No ranking",
            "No rating",
            "No composite score",
            "No raw responses",
            "No question-level traces",
            "No judge rationales",
            "Judges presented separately",
            "Runtime dimensions kept separate from factual evaluation",
        ],
        "files": [
            "README_PUBLIC.md",
            "public_profile_summary.csv",
            "public_runtime_profile_summary.csv",
            "public_methodology_validation.csv",
            "public_data_dictionary.csv",
            "PUBLICATION_REVIEW_CHECKLIST.md",
            "RELEASE_MANIFEST.json",
            "CHECKSUMS.sha256",
        ],
        "privacy_note": (
            "Pseudonymization is not absolute anonymization. "
            "Manual review remains mandatory before publication."
        ),
    }

    (output_dir / "RELEASE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Checksum après écriture de tous les fichiers publics sauf CHECKSUMS lui-même.
    write_checksums(output_dir)

    # Contrôle anti-fuite après génération.
    leak_findings = scan_public_directory_for_leaks(output_dir, providers)

    if leak_findings:
        leak_report = "\n".join(f"- {item}" for item in leak_findings)
        # On déplace la release en quarantaine plutôt que de la laisser disponible.
        quarantine = output_dir.with_name(output_dir.name + "_QUARANTINE")
        if quarantine.exists():
            shutil.rmtree(quarantine)
        shutil.move(str(output_dir), str(quarantine))

        raise RuntimeError(
            "Release publique refusée : fuite potentielle détectée.\n"
            f"Release déplacée en quarantaine : {quarantine}\n"
            f"{leak_report}"
        )

    # Journal privé.
    private_log = [
        "NEOMUNDI PUBLIC RELEASE BUILD LOG",
        "=" * 72,
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"Generator version: {VERSION}",
        f"Input dir: {input_dir}",
        f"Output dir: {output_dir}",
        f"Private mapping: {mapping_path}",
        f"Mapping created or updated: {mapping_changed}",
        f"Mode: {mode}",
        f"Provider count: {len(providers)}",
        f"Public profile count: {len(profile_summary)}",
        "",
        "PRIVATE PROVIDER ↔ PROFILE MAPPING",
        "-" * 72,
    ]

    for _, row in mapping_df.sort_values("provider", kind="stable").iterrows():
        private_log.append(f"{row['provider']} -> {row['profile_id']}")

    private_log.extend(
        [
            "",
            "PUBLIC FILE CHECKSUMS",
            "-" * 72,
            (output_dir / "CHECKSUMS.sha256").read_text(encoding="utf-8"),
        ]
    )

    (private_dir / BUILD_LOG_FILE).write_text(
        "\n".join(private_log),
        encoding="utf-8",
    )

    print("RELEASE PUBLIQUE GÉNÉRÉE")
    print("=" * 72)
    print(f"Dossier public : {output_dir}")
    print(f"Dossier privé  : {private_dir}")
    print(f"Mode           : {mode}")
    print(f"Profils publics: {len(profile_summary)}")
    print()
    print("CONTRÔLES")
    print("-" * 72)
    print("OK — Aucun nom de provider détecté dans les fichiers publics.")
    print("OK — Aucun champ de classement détecté.")
    print("OK — Aucun score composite détecté.")
    print("OK — Aucun chemin source publié.")
    print("OK — Aucun fichier question-level publié.")
    print()
    print("REVUE HUMAINE OBLIGATOIRE")
    print("-" * 72)
    print("Ouvre PUBLICATION_REVIEW_CHECKLIST.md et coche chaque contrôle avant publication.")
    print()
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Construit une release publique pseudonymisée sans classement."
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help="Dossier interne figé contenant les résultats double-jugés.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Dossier public à créer.",
    )

    parser.add_argument(
        "--private-dir",
        type=Path,
        default=None,
        help="Dossier privé contenant la table de correspondance pseudonymisée.",
    )

    parser.add_argument(
        "--mode",
        choices=["conservative", "detailed"],
        default="conservative",
        help="Niveau de granularité publique. Défaut : conservative.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Reconstruit le dossier public s'il existe déjà.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        input_dir = find_input_dir(args.input_dir)

        if args.output_dir:
            output_dir = args.output_dir.expanduser().resolve()
        else:
            output_dir = (input_dir.parent / DEFAULT_PUBLIC_DIR_NAME).resolve()

        if args.private_dir:
            private_dir = args.private_dir.expanduser().resolve()
        else:
            private_dir = (input_dir.parent / DEFAULT_PRIVATE_DIR_NAME).resolve()

        print(f"Dossier interne figé : {input_dir}")
        print(f"Dossier public cible : {output_dir}")
        print(f"Dossier privé        : {private_dir}")
        print()

        exit_code = build_release(
            input_dir=input_dir,
            output_dir=output_dir,
            private_dir=private_dir,
            mode=args.mode,
            force=args.force,
        )

        sys.exit(exit_code)

    except Exception as exc:  # noqa: BLE001
        print(f"ERREUR : {type(exc).__name__}: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
