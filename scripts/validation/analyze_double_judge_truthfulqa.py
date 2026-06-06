#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
analyze_double_judge_truthfulqa.py

Analyse interne du corpus TruthfulQA double-jugé NeoMundi :
OpenAI historique ↔ Mistral niveau 1.

Arborescence attendue :
truthfulqa_12_models/
├── 01_raw_results/
├── 02_openai_judged/
├── 03_mistral_judged/
├── 04_analysis_output/
├── audit_truthfulqa_inventory.py
└── analyze_double_judge_truthfulqa.py

Le script :
- détecte automatiquement les providers ;
- apparie truthfulqa_<provider>_judged.csv avec
  truthfulqa_<provider>_mistral_judged.csv ;
- aligne les lignes par question_id ;
- vérifie que les réponses comparées sont identiques ;
- exclut proprement les lignes non comparables ;
- calcule l'accord observé et Cohen kappa global et par provider ;
- génère les matrices de confusion ;
- extrait les désaccords ligne par ligne ;
- agrège les désaccords par question et par dimensions runtime disponibles ;
- ne modifie aucun fichier source ;
- ne produit aucun classement, rating ou score composite.

Usage PowerShell :
    python .\analyze_double_judge_truthfulqa.py

ou :
    python .\analyze_double_judge_truthfulqa.py --root "C:\chemin\vers\truthfulqa_12_models"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENAI_DIR = "02_openai_judged"
MISTRAL_DIR = "03_mistral_judged"
OUTPUT_DIR = "04_analysis_output"
ANALYSIS_SUBDIR = "double_judge_analysis"

OPENAI_PATTERN = re.compile(r"^truthfulqa_(?P<provider>.+?)_judged\.csv$", re.IGNORECASE)
MISTRAL_PATTERN = re.compile(r"^truthfulqa_(?P<provider>.+?)_mistral_judged\.csv$", re.IGNORECASE)

QUESTION_ID_ALIASES = [
    "question_id",
    "questionid",
    "qid",
    "question_index",
    "question_idx",
    "id",
]

QUESTION_TEXT_ALIASES = [
    "question",
    "question_text",
    "prompt",
    "input",
    "query",
]

ANSWER_ALIASES = [
    "response",
    "answer",
    "model_response",
    "generated_answer",
    "assistant_response",
    "output",
    "completion",
]

OPENAI_CORRECT_ALIASES = [
    "openai_is_correct",
    "is_correct",
    "judge_is_correct",
]

OPENAI_VERDICT_ALIASES = [
    "openai_judge_verdict",
    "openai_verdict",
    "judge_verdict",
    "verdict",
]

MISTRAL_CORRECT_ALIASES = [
    "mistral_is_correct",
    "is_correct",
    "judge_is_correct",
]

MISTRAL_VERDICT_ALIASES = [
    "mistral_judge_verdict",
    "mistral_verdict",
    "judge_verdict",
    "verdict",
]

RUNTIME_DIMENSIONS = [
    "decision",
    "regime",
    "dg_profile",
    "dg_flagged",
    "flagged",
    "hallucination",
]

NULL_LIKE_STRINGS = {
    "",
    "nan",
    "none",
    "null",
    "n/a",
    "na",
    "missing",
    "error",
    "parse_error",
}

TRUE_LIKE_STRINGS = {
    "true",
    "1",
    "yes",
    "y",
    "correct",
    "ok",
    "pass",
    "passed",
    "allow",
}

FALSE_LIKE_STRINGS = {
    "false",
    "0",
    "no",
    "n",
    "incorrect",
    "ko",
    "fail",
    "failed",
    "flag",
}


# ---------------------------------------------------------------------------
# Utilitaires généraux
# ---------------------------------------------------------------------------

def normalize_provider(provider: str) -> str:
    return provider.strip().lower().replace("-", "_").replace(" ", "_")


def normalize_column_name(name: object) -> str:
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")


def normalize_scalar(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def normalize_text_for_comparison(value: object) -> str:
    return normalize_scalar(value)


def find_column(df: pd.DataFrame, aliases: Iterable[str]) -> str:
    normalized_map = {normalize_column_name(col): str(col) for col in df.columns}
    for alias in aliases:
        key = normalize_column_name(alias)
        if key in normalized_map:
            return normalized_map[key]
    return ""


def is_missing(value: object) -> bool:
    if pd.isna(value):
        return True
    return normalize_scalar(value).lower() in NULL_LIKE_STRINGS


def parse_binary(value: object) -> Optional[bool]:
    """
    Convertit un booléen ou verdict en True / False.
    Retourne None lorsque la valeur n'est pas exploitable.
    """
    if is_missing(value):
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value == 1:
            return True
        if value == 0:
            return False

    normalized = normalize_scalar(value).lower()
    if normalized in TRUE_LIKE_STRINGS:
        return True
    if normalized in FALSE_LIKE_STRINGS:
        return False

    return None


def safe_div(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator else float("nan")


def format_metric(value: object, digits: int = 4) -> str:
    if value is None:
        return "NA"
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isnan(numeric):
        return "NA"
    return f"{numeric:.{digits}f}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv_flexible(path: Path) -> tuple[pd.DataFrame, str, str]:
    """
    Lit un CSV avec plusieurs encodages et séparateurs.
    Retourne : dataframe, encodage, séparateur.
    """
    attempts = []
    encodings = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
    separators = [",", ";", "\t"]

    for encoding in encodings:
        for separator in separators:
            try:
                df = pd.read_csv(
                    path,
                    encoding=encoding,
                    sep=separator,
                    dtype=object,
                    keep_default_na=True,
                    na_values=["", "NA", "N/A", "null", "None"],
                    low_memory=False,
                )
                if len(df.columns) > 1:
                    return df, encoding, repr(separator)
                attempts.append(f"{encoding} / {repr(separator)} : une seule colonne")
            except Exception as exc:  # noqa: BLE001
                attempts.append(f"{encoding} / {repr(separator)} : {type(exc).__name__}")

    for encoding in encodings:
        try:
            df = pd.read_csv(
                path,
                encoding=encoding,
                sep=None,
                engine="python",
                dtype=object,
                keep_default_na=True,
                na_values=["", "NA", "N/A", "null", "None"],
            )
            return df, encoding, "auto"
        except Exception as exc:  # noqa: BLE001
            attempts.append(f"{encoding} / auto : {type(exc).__name__}")

    raise RuntimeError("Impossible de lire le CSV. Essais : " + " | ".join(attempts))


def scan_layer(folder: Path, pattern: re.Pattern[str]) -> dict[str, Path]:
    discovered: dict[str, Path] = {}
    if not folder.exists():
        return discovered

    for path in sorted(folder.glob("*.csv")):
        match = pattern.match(path.name)
        if not match:
            continue
        provider = normalize_provider(match.group("provider"))
        discovered[provider] = path

    return discovered


def add_issue(
    issues: list[dict[str, object]],
    provider: str,
    severity: str,
    category: str,
    detail: str,
) -> None:
    issues.append(
        {
            "provider": provider,
            "severity": severity,
            "category": category,
            "detail": detail,
        }
    )


# ---------------------------------------------------------------------------
# Métriques
# ---------------------------------------------------------------------------

def confusion_counts(openai_values: pd.Series, mistral_values: pd.Series) -> dict[str, int]:
    """
    Matrice de confusion, OpenAI en lignes et Mistral en colonnes.
    """
    openai_bool = openai_values.astype(bool)
    mistral_bool = mistral_values.astype(bool)

    return {
        "openai_incorrect_mistral_incorrect": int((~openai_bool & ~mistral_bool).sum()),
        "openai_incorrect_mistral_correct": int((~openai_bool & mistral_bool).sum()),
        "openai_correct_mistral_incorrect": int((openai_bool & ~mistral_bool).sum()),
        "openai_correct_mistral_correct": int((openai_bool & mistral_bool).sum()),
    }


def cohen_kappa_binary(openai_values: pd.Series, mistral_values: pd.Series) -> tuple[float, float, float]:
    """
    Calcule Cohen kappa pour deux séries booléennes.
    Retourne : kappa, accord observé, accord attendu.
    """
    n = len(openai_values)
    if n == 0:
        return float("nan"), float("nan"), float("nan")

    a = openai_values.astype(bool)
    b = mistral_values.astype(bool)

    observed = float((a == b).mean())
    p_openai_true = float(a.mean())
    p_mistral_true = float(b.mean())

    expected = (
        p_openai_true * p_mistral_true
        + (1.0 - p_openai_true) * (1.0 - p_mistral_true)
    )

    if math.isclose(1.0 - expected, 0.0, abs_tol=1e-15):
        return float("nan"), observed, expected

    kappa = (observed - expected) / (1.0 - expected)
    return float(kappa), observed, expected


def kappa_interpretation(kappa: float) -> str:
    """
    Libellé descriptif indicatif uniquement.
    Ne constitue pas une validation scientifique autonome.
    """
    if math.isnan(kappa):
        return "non_calculable"
    if kappa < 0:
        return "accord_inferieur_au_hasard"
    if kappa < 0.21:
        return "accord_faible"
    if kappa < 0.41:
        return "accord_limite"
    if kappa < 0.61:
        return "accord_modere"
    if kappa < 0.81:
        return "accord_substantiel"
    return "accord_tres_eleve"


def build_metrics_row(provider: str, df: pd.DataFrame) -> dict[str, object]:
    n = len(df)
    openai_values = df["openai_is_correct_parsed"].astype(bool)
    mistral_values = df["mistral_is_correct_parsed"].astype(bool)

    counts = confusion_counts(openai_values, mistral_values)
    kappa, observed, expected = cohen_kappa_binary(openai_values, mistral_values)

    agreement_count = (
        counts["openai_incorrect_mistral_incorrect"]
        + counts["openai_correct_mistral_correct"]
    )
    disagreement_count = (
        counts["openai_incorrect_mistral_correct"]
        + counts["openai_correct_mistral_incorrect"]
    )

    openai_correct_count = int(openai_values.sum())
    mistral_correct_count = int(mistral_values.sum())

    return {
        "provider": provider,
        "n_comparable_pairs": n,
        "agreement_count": agreement_count,
        "disagreement_count": disagreement_count,
        "observed_agreement_rate": safe_div(agreement_count, n),
        "disagreement_rate": safe_div(disagreement_count, n),
        "expected_agreement_rate": expected,
        "cohen_kappa": kappa,
        "kappa_interpretation_indicative": kappa_interpretation(kappa),
        "openai_correct_count": openai_correct_count,
        "openai_correct_rate": safe_div(openai_correct_count, n),
        "mistral_correct_count": mistral_correct_count,
        "mistral_correct_rate": safe_div(mistral_correct_count, n),
        "mistral_minus_openai_correct_rate": (
            safe_div(mistral_correct_count, n) - safe_div(openai_correct_count, n)
        ),
        **counts,
    }


# ---------------------------------------------------------------------------
# Préparation et analyse par provider
# ---------------------------------------------------------------------------

def prepare_provider_pairs(
    provider: str,
    openai_path: Path,
    mistral_path: Path,
    issues: list[dict[str, object]],
) -> tuple[Optional[pd.DataFrame], dict[str, object]]:
    """
    Prépare les paires comparables pour un provider.
    """
    quality: dict[str, object] = {
        "provider": provider,
        "openai_file": openai_path.name,
        "mistral_file": mistral_path.name,
        "openai_sha256": sha256_file(openai_path),
        "mistral_sha256": sha256_file(mistral_path),
        "openai_read_ok": False,
        "mistral_read_ok": False,
        "openai_encoding": "",
        "mistral_encoding": "",
        "openai_separator": "",
        "mistral_separator": "",
        "openai_rows": "",
        "mistral_rows": "",
        "openai_unique_question_ids": "",
        "mistral_unique_question_ids": "",
        "intersection_question_ids": "",
        "only_openai_question_ids": "",
        "only_mistral_question_ids": "",
        "duplicate_openai_question_ids": "",
        "duplicate_mistral_question_ids": "",
        "response_mismatch_count": "",
        "missing_or_unparseable_openai_verdicts": "",
        "missing_or_unparseable_mistral_verdicts": "",
        "excluded_pair_count": "",
        "comparable_pair_count": "",
        "eligible_for_analysis": False,
    }

    try:
        openai_df, openai_encoding, openai_separator = read_csv_flexible(openai_path)
        quality["openai_read_ok"] = True
        quality["openai_encoding"] = openai_encoding
        quality["openai_separator"] = openai_separator
        quality["openai_rows"] = len(openai_df)
    except Exception as exc:  # noqa: BLE001
        add_issue(issues, provider, "ERROR", "openai_read_error", f"{type(exc).__name__}: {exc}")
        return None, quality

    try:
        mistral_df, mistral_encoding, mistral_separator = read_csv_flexible(mistral_path)
        quality["mistral_read_ok"] = True
        quality["mistral_encoding"] = mistral_encoding
        quality["mistral_separator"] = mistral_separator
        quality["mistral_rows"] = len(mistral_df)
    except Exception as exc:  # noqa: BLE001
        add_issue(issues, provider, "ERROR", "mistral_read_error", f"{type(exc).__name__}: {exc}")
        return None, quality

    openai_qid_col = find_column(openai_df, QUESTION_ID_ALIASES)
    mistral_qid_col = find_column(mistral_df, QUESTION_ID_ALIASES)
    openai_question_col = find_column(openai_df, QUESTION_TEXT_ALIASES)
    mistral_question_col = find_column(mistral_df, QUESTION_TEXT_ALIASES)
    openai_answer_col = find_column(openai_df, ANSWER_ALIASES)
    mistral_answer_col = find_column(mistral_df, ANSWER_ALIASES)
    openai_correct_col = find_column(openai_df, OPENAI_CORRECT_ALIASES)
    openai_verdict_col = find_column(openai_df, OPENAI_VERDICT_ALIASES)
    mistral_correct_col = find_column(mistral_df, MISTRAL_CORRECT_ALIASES)
    mistral_verdict_col = find_column(mistral_df, MISTRAL_VERDICT_ALIASES)

    required = [
        ("openai_question_id", openai_qid_col),
        ("mistral_question_id", mistral_qid_col),
        ("openai_answer", openai_answer_col),
        ("mistral_answer", mistral_answer_col),
    ]
    missing_required = [name for name, value in required if not value]
    if missing_required:
        add_issue(
            issues,
            provider,
            "ERROR",
            "missing_required_columns",
            "Colonnes requises absentes : " + ", ".join(missing_required),
        )
        return None, quality

    if not (openai_correct_col or openai_verdict_col):
        add_issue(
            issues,
            provider,
            "ERROR",
            "missing_openai_verdict_columns",
            "Aucune colonne OpenAI de verdict exploitable détectée.",
        )
        return None, quality

    if not (mistral_correct_col or mistral_verdict_col):
        add_issue(
            issues,
            provider,
            "ERROR",
            "missing_mistral_verdict_columns",
            "Aucune colonne Mistral de verdict exploitable détectée.",
        )
        return None, quality

    openai_work = openai_df.copy()
    mistral_work = mistral_df.copy()

    openai_work["_question_id_norm"] = openai_work[openai_qid_col].map(normalize_scalar)
    mistral_work["_question_id_norm"] = mistral_work[mistral_qid_col].map(normalize_scalar)

    openai_duplicate_count = int(openai_work["_question_id_norm"].duplicated().sum())
    mistral_duplicate_count = int(mistral_work["_question_id_norm"].duplicated().sum())
    quality["duplicate_openai_question_ids"] = openai_duplicate_count
    quality["duplicate_mistral_question_ids"] = mistral_duplicate_count

    if openai_duplicate_count:
        add_issue(
            issues,
            provider,
            "ERROR",
            "duplicate_openai_question_ids",
            f"{openai_duplicate_count} question_id dupliqués dans le fichier OpenAI.",
        )

    if mistral_duplicate_count:
        add_issue(
            issues,
            provider,
            "ERROR",
            "duplicate_mistral_question_ids",
            f"{mistral_duplicate_count} question_id dupliqués dans le fichier Mistral.",
        )

    # Une seule ligne par question_id pour rendre l'analyse déterministe.
    openai_work = openai_work.drop_duplicates(subset=["_question_id_norm"], keep="first")
    mistral_work = mistral_work.drop_duplicates(subset=["_question_id_norm"], keep="first")

    openai_ids = set(openai_work["_question_id_norm"])
    mistral_ids = set(mistral_work["_question_id_norm"])
    intersection = openai_ids & mistral_ids
    only_openai = openai_ids - mistral_ids
    only_mistral = mistral_ids - openai_ids

    quality["openai_unique_question_ids"] = len(openai_ids)
    quality["mistral_unique_question_ids"] = len(mistral_ids)
    quality["intersection_question_ids"] = len(intersection)
    quality["only_openai_question_ids"] = len(only_openai)
    quality["only_mistral_question_ids"] = len(only_mistral)

    if only_openai or only_mistral:
        add_issue(
            issues,
            provider,
            "WARNING",
            "question_id_subset_mismatch",
            (
                f"{len(only_openai)} question_id uniquement dans OpenAI ; "
                f"{len(only_mistral)} uniquement dans Mistral. "
                "L'analyse utilisera l'intersection."
            ),
        )

    openai_keep = {
        "_question_id_norm": "question_id",
        openai_answer_col: "response_openai_source",
    }
    if openai_question_col:
        openai_keep[openai_question_col] = "question"

    openai_verdict_source = openai_correct_col or openai_verdict_col
    openai_keep[openai_verdict_source] = "openai_verdict_source"

    # Dimensions runtime provenant du fichier OpenAI historique.
    runtime_columns = {}
    for dimension in RUNTIME_DIMENSIONS:
        column = find_column(openai_work, [dimension])
        if column and column not in openai_keep:
            runtime_columns[column] = dimension
    openai_keep.update(runtime_columns)

    mistral_keep = {
        "_question_id_norm": "question_id",
        mistral_answer_col: "response_mistral_source",
    }
    if mistral_question_col and "question" not in openai_keep.values():
        mistral_keep[mistral_question_col] = "question"

    mistral_verdict_source = mistral_correct_col or mistral_verdict_col
    mistral_keep[mistral_verdict_source] = "mistral_verdict_source"

    left = openai_work[list(openai_keep)].rename(columns=openai_keep)
    right = mistral_work[list(mistral_keep)].rename(columns=mistral_keep)

    merged = left.merge(right, on="question_id", how="inner", suffixes=("", "_mistral"))

    merged["response_openai_norm"] = merged["response_openai_source"].map(normalize_text_for_comparison)
    merged["response_mistral_norm"] = merged["response_mistral_source"].map(normalize_text_for_comparison)
    merged["response_identical"] = merged["response_openai_norm"] == merged["response_mistral_norm"]

    merged["openai_is_correct_parsed"] = merged["openai_verdict_source"].map(parse_binary)
    merged["mistral_is_correct_parsed"] = merged["mistral_verdict_source"].map(parse_binary)

    response_mismatch_count = int((~merged["response_identical"]).sum())
    missing_openai_verdicts = int(merged["openai_is_correct_parsed"].isna().sum())
    missing_mistral_verdicts = int(merged["mistral_is_correct_parsed"].isna().sum())

    quality["response_mismatch_count"] = response_mismatch_count
    quality["missing_or_unparseable_openai_verdicts"] = missing_openai_verdicts
    quality["missing_or_unparseable_mistral_verdicts"] = missing_mistral_verdicts

    if response_mismatch_count:
        add_issue(
            issues,
            provider,
            "ERROR",
            "response_mismatch",
            (
                f"{response_mismatch_count} réponses diffèrent entre OpenAI et Mistral "
                "pour un même question_id. Ces lignes seront exclues."
            ),
        )

    if missing_openai_verdicts:
        add_issue(
            issues,
            provider,
            "WARNING",
            "missing_or_unparseable_openai_verdicts",
            f"{missing_openai_verdicts} verdicts OpenAI absents ou non interprétables.",
        )

    if missing_mistral_verdicts:
        add_issue(
            issues,
            provider,
            "WARNING",
            "missing_or_unparseable_mistral_verdicts",
            f"{missing_mistral_verdicts} verdicts Mistral absents ou non interprétables.",
        )

    merged["provider"] = provider
    merged["pair_is_comparable"] = (
        merged["response_identical"]
        & merged["openai_is_correct_parsed"].notna()
        & merged["mistral_is_correct_parsed"].notna()
    )

    comparable = merged.loc[merged["pair_is_comparable"]].copy()
    excluded_count = len(merged) - len(comparable)

    quality["excluded_pair_count"] = excluded_count
    quality["comparable_pair_count"] = len(comparable)
    quality["eligible_for_analysis"] = len(comparable) > 0

    if len(comparable) == 0:
        add_issue(
            issues,
            provider,
            "ERROR",
            "no_comparable_pairs",
            "Aucune paire exploitable après contrôles.",
        )
        return None, quality

    comparable["openai_is_correct_parsed"] = comparable["openai_is_correct_parsed"].astype(bool)
    comparable["mistral_is_correct_parsed"] = comparable["mistral_is_correct_parsed"].astype(bool)
    comparable["agreement"] = (
        comparable["openai_is_correct_parsed"]
        == comparable["mistral_is_correct_parsed"]
    )

    comparable["disagreement_direction"] = "agreement"
    comparable.loc[
        (~comparable["openai_is_correct_parsed"])
        & comparable["mistral_is_correct_parsed"],
        "disagreement_direction",
    ] = "openai_incorrect_mistral_correct"
    comparable.loc[
        comparable["openai_is_correct_parsed"]
        & (~comparable["mistral_is_correct_parsed"]),
        "disagreement_direction",
    ] = "openai_correct_mistral_incorrect"

    return comparable, quality


# ---------------------------------------------------------------------------
# Agrégations secondaires
# ---------------------------------------------------------------------------

def aggregate_disagreement_by_dimension(all_pairs: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if dimension not in all_pairs.columns:
        return pd.DataFrame()

    working = all_pairs.copy()
    working[dimension] = working[dimension].map(normalize_scalar)
    working.loc[working[dimension] == "", dimension] = "<missing>"

    grouped = (
        working.groupby(["provider", dimension], dropna=False)
        .agg(
            n_comparable_pairs=("agreement", "size"),
            agreement_count=("agreement", "sum"),
        )
        .reset_index()
    )

    grouped["disagreement_count"] = grouped["n_comparable_pairs"] - grouped["agreement_count"]
    grouped["agreement_rate"] = grouped["agreement_count"] / grouped["n_comparable_pairs"]
    grouped["disagreement_rate"] = grouped["disagreement_count"] / grouped["n_comparable_pairs"]

    return grouped.sort_values(["provider", dimension], kind="stable")


def build_question_disagreement_frequency(all_pairs: pd.DataFrame) -> pd.DataFrame:
    if all_pairs.empty:
        return pd.DataFrame()

    grouped = (
        all_pairs.groupby("question_id", dropna=False)
        .agg(
            provider_count=("provider", "nunique"),
            comparable_pair_count=("agreement", "size"),
            disagreement_count=("agreement", lambda values: int((~values.astype(bool)).sum())),
            openai_incorrect_mistral_correct_count=(
                "disagreement_direction",
                lambda values: int((values == "openai_incorrect_mistral_correct").sum()),
            ),
            openai_correct_mistral_incorrect_count=(
                "disagreement_direction",
                lambda values: int((values == "openai_correct_mistral_incorrect").sum()),
            ),
        )
        .reset_index()
    )

    grouped["disagreement_rate"] = (
        grouped["disagreement_count"] / grouped["comparable_pair_count"]
    )

    if "question" in all_pairs.columns:
        question_lookup = (
            all_pairs[["question_id", "question"]]
            .drop_duplicates(subset=["question_id"], keep="first")
        )
        grouped = grouped.merge(question_lookup, on="question_id", how="left")

    # Tri descriptif : fréquence des désaccords, et non classement des providers.
    return grouped.sort_values(
        ["disagreement_count", "question_id"],
        ascending=[False, True],
        kind="stable",
    )


def build_confusion_rows(summary_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in summary_df.iterrows():
        provider = row["provider"]
        rows.extend(
            [
                {
                    "provider": provider,
                    "openai_judge": "INCORRECT",
                    "mistral_judge": "INCORRECT",
                    "count": row["openai_incorrect_mistral_incorrect"],
                },
                {
                    "provider": provider,
                    "openai_judge": "INCORRECT",
                    "mistral_judge": "CORRECT",
                    "count": row["openai_incorrect_mistral_correct"],
                },
                {
                    "provider": provider,
                    "openai_judge": "CORRECT",
                    "mistral_judge": "INCORRECT",
                    "count": row["openai_correct_mistral_incorrect"],
                },
                {
                    "provider": provider,
                    "openai_judge": "CORRECT",
                    "mistral_judge": "CORRECT",
                    "count": row["openai_correct_mistral_correct"],
                },
            ]
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Audit statistique principal
# ---------------------------------------------------------------------------

def analyze(root: Path) -> int:
    openai_folder = root / OPENAI_DIR
    mistral_folder = root / MISTRAL_DIR
    output_folder = root / OUTPUT_DIR / ANALYSIS_SUBDIR
    output_folder.mkdir(parents=True, exist_ok=True)

    if not openai_folder.exists():
        print(f"ERREUR : dossier absent : {openai_folder}")
        return 2

    if not mistral_folder.exists():
        print(f"ERREUR : dossier absent : {mistral_folder}")
        return 2

    openai_files = scan_layer(openai_folder, OPENAI_PATTERN)
    mistral_files = scan_layer(mistral_folder, MISTRAL_PATTERN)

    providers = sorted(set(openai_files) | set(mistral_files))
    issues: list[dict[str, object]] = []
    quality_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    all_pairs_parts: list[pd.DataFrame] = []

    for provider in providers:
        openai_path = openai_files.get(provider)
        mistral_path = mistral_files.get(provider)

        if openai_path is None:
            add_issue(
                issues,
                provider,
                "ERROR",
                "missing_openai_file",
                f"Fichier attendu : truthfulqa_{provider}_judged.csv",
            )
            quality_rows.append(
                {
                    "provider": provider,
                    "openai_file": "",
                    "mistral_file": mistral_path.name if mistral_path else "",
                    "eligible_for_analysis": False,
                }
            )
            continue

        if mistral_path is None:
            add_issue(
                issues,
                provider,
                "ERROR",
                "missing_mistral_file",
                f"Fichier attendu : truthfulqa_{provider}_mistral_judged.csv",
            )
            quality_rows.append(
                {
                    "provider": provider,
                    "openai_file": openai_path.name,
                    "mistral_file": "",
                    "eligible_for_analysis": False,
                }
            )
            continue

        pairs, quality = prepare_provider_pairs(provider, openai_path, mistral_path, issues)
        quality_rows.append(quality)

        if pairs is None or pairs.empty:
            continue

        all_pairs_parts.append(pairs)
        summary_rows.append(build_metrics_row(provider, pairs))

    quality_df = pd.DataFrame(quality_rows)
    issues_df = pd.DataFrame(
        issues,
        columns=["provider", "severity", "category", "detail"],
    )
    summary_by_provider_df = pd.DataFrame(summary_rows)

    if all_pairs_parts:
        all_pairs = pd.concat(all_pairs_parts, ignore_index=True)
    else:
        all_pairs = pd.DataFrame()

    if all_pairs.empty:
        issues_df.to_csv(output_folder / "analysis_issues.csv", index=False, encoding="utf-8-sig")
        quality_df.to_csv(output_folder / "analysis_quality_report.csv", index=False, encoding="utf-8-sig")
        print("ERREUR : aucune paire comparable disponible.")
        return 1

    # Analyse globale poolée.
    global_row = build_metrics_row("GLOBAL_POOLED", all_pairs)
    valid_provider_kappas = summary_by_provider_df["cohen_kappa"].dropna()

    global_row["provider_count_analyzed"] = int(summary_by_provider_df["provider"].nunique())
    global_row["macro_mean_provider_kappa"] = (
        float(valid_provider_kappas.mean()) if not valid_provider_kappas.empty else float("nan")
    )

    if not summary_by_provider_df.empty:
        weights = summary_by_provider_df["n_comparable_pairs"].astype(float)
        kappas = summary_by_provider_df["cohen_kappa"].astype(float)
        usable = kappas.notna() & weights.notna() & (weights > 0)
        global_row["weighted_mean_provider_kappa"] = (
            float((kappas[usable] * weights[usable]).sum() / weights[usable].sum())
            if usable.any()
            else float("nan")
        )
    else:
        global_row["weighted_mean_provider_kappa"] = float("nan")

    global_df = pd.DataFrame([global_row])

    # Matrices et désaccords.
    confusion_df = build_confusion_rows(summary_by_provider_df)

    disagreement_columns = [
        "provider",
        "question_id",
        "question",
        "disagreement_direction",
        "openai_verdict_source",
        "mistral_verdict_source",
        "openai_is_correct_parsed",
        "mistral_is_correct_parsed",
        "response_openai_source",
        "decision",
        "regime",
        "dg_profile",
        "dg_flagged",
        "flagged",
        "hallucination",
    ]
    available_disagreement_columns = [
        column for column in disagreement_columns if column in all_pairs.columns
    ]
    disagreements_df = (
        all_pairs.loc[~all_pairs["agreement"], available_disagreement_columns]
        .sort_values(["provider", "question_id"], kind="stable")
        .reset_index(drop=True)
    )

    question_frequency_df = build_question_disagreement_frequency(all_pairs)

    # Exports secondaires par dimensions runtime disponibles.
    dimension_report_files: list[str] = []
    for dimension in RUNTIME_DIMENSIONS:
        report = aggregate_disagreement_by_dimension(all_pairs, dimension)
        if report.empty:
            continue
        filename = f"disagreement_by_{dimension}.csv"
        report.to_csv(output_folder / filename, index=False, encoding="utf-8-sig")
        dimension_report_files.append(filename)

    # Données comparables minimales pour audit interne et reproduction.
    comparable_export_columns = [
        "provider",
        "question_id",
        "question",
        "openai_verdict_source",
        "mistral_verdict_source",
        "openai_is_correct_parsed",
        "mistral_is_correct_parsed",
        "agreement",
        "disagreement_direction",
        "decision",
        "regime",
        "dg_profile",
        "dg_flagged",
        "flagged",
        "hallucination",
    ]
    available_comparable_columns = [
        column for column in comparable_export_columns if column in all_pairs.columns
    ]
    comparable_pairs_df = (
        all_pairs[available_comparable_columns]
        .sort_values(["provider", "question_id"], kind="stable")
        .reset_index(drop=True)
    )

    # Exports principaux.
    summary_by_provider_df = summary_by_provider_df.sort_values("provider", kind="stable")
    quality_df = quality_df.sort_values("provider", kind="stable")
    if not issues_df.empty:
        issues_df = issues_df.sort_values(["provider", "severity", "category"], kind="stable")

    summary_by_provider_df.to_csv(
        output_folder / "double_judge_summary_by_provider.csv",
        index=False,
        encoding="utf-8-sig",
    )
    global_df.to_csv(
        output_folder / "global_double_judge_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )
    confusion_df.to_csv(
        output_folder / "confusion_matrix_by_provider.csv",
        index=False,
        encoding="utf-8-sig",
    )
    disagreements_df.to_csv(
        output_folder / "judge_disagreements.csv",
        index=False,
        encoding="utf-8-sig",
    )
    question_frequency_df.to_csv(
        output_folder / "question_disagreement_frequency.csv",
        index=False,
        encoding="utf-8-sig",
    )
    quality_df.to_csv(
        output_folder / "analysis_quality_report.csv",
        index=False,
        encoding="utf-8-sig",
    )
    issues_df.to_csv(
        output_folder / "analysis_issues.csv",
        index=False,
        encoding="utf-8-sig",
    )
    comparable_pairs_df.to_csv(
        output_folder / "comparable_pairs_internal.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Manifest et synthèse texte.
    generated_reports = [
        "double_judge_summary_by_provider.csv",
        "global_double_judge_summary.csv",
        "confusion_matrix_by_provider.csv",
        "judge_disagreements.csv",
        "question_disagreement_frequency.csv",
        "analysis_quality_report.csv",
        "analysis_issues.csv",
        "comparable_pairs_internal.csv",
        *dimension_report_files,
        "analysis_manifest.json",
        "analysis_console_summary.txt",
    ]

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(root.resolve()),
        "analysis_folder": str(output_folder.resolve()),
        "methodology": "TruthfulQA double judgment: OpenAI historical judge versus Mistral level 1 judge",
        "provider_count_detected": len(providers),
        "provider_count_analyzed": int(summary_by_provider_df["provider"].nunique()),
        "providers_detected": providers,
        "providers_analyzed": summary_by_provider_df["provider"].tolist(),
        "total_comparable_pairs": int(len(all_pairs)),
        "total_disagreements": int((~all_pairs["agreement"]).sum()),
        "global_observed_agreement_rate": global_row["observed_agreement_rate"],
        "global_cohen_kappa": global_row["cohen_kappa"],
        "macro_mean_provider_kappa": global_row["macro_mean_provider_kappa"],
        "weighted_mean_provider_kappa": global_row["weighted_mean_provider_kappa"],
        "error_count": int((issues_df["severity"] == "ERROR").sum()) if not issues_df.empty else 0,
        "warning_count": int((issues_df["severity"] == "WARNING").sum()) if not issues_df.empty else 0,
        "generated_reports": generated_reports,
        "notes": [
            "No ranking, rating, leaderboard or composite score is produced.",
            "Only OpenAI-Mistral pairs sharing a question_id, an identical response and two parseable verdicts are analyzed.",
            "Global pooled kappa and provider-level kappas are reported separately.",
            "Indicative kappa labels are descriptive only and must not be interpreted as standalone scientific validation.",
        ],
    }

    with (output_folder / "analysis_manifest.json").open("w", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)

    summary_lines = [
        "ANALYSE TRUTHFULQA DOUBLE-JUGEE — NEO MUNDI",
        "=" * 84,
        f"Généré le : {manifest['generated_at']}",
        f"Dossier racine : {manifest['root']}",
        "",
        f"Providers détectés : {manifest['provider_count_detected']}",
        f"Providers analysés : {manifest['provider_count_analyzed']}",
        f"Paires comparables : {manifest['total_comparable_pairs']}",
        f"Désaccords OpenAI ↔ Mistral : {manifest['total_disagreements']}",
        "",
        "SYNTHÈSE GLOBALE POOLÉE",
        "-" * 84,
        f"Accord observé : {format_metric(global_row['observed_agreement_rate'])}",
        f"Taux de désaccord : {format_metric(global_row['disagreement_rate'])}",
        f"Cohen kappa poolé : {format_metric(global_row['cohen_kappa'])}",
        f"Interprétation indicative : {global_row['kappa_interpretation_indicative']}",
        f"Moyenne macro des kappas providers : {format_metric(global_row['macro_mean_provider_kappa'])}",
        f"Moyenne pondérée des kappas providers : {format_metric(global_row['weighted_mean_provider_kappa'])}",
        f"Taux correct OpenAI : {format_metric(global_row['openai_correct_rate'])}",
        f"Taux correct Mistral : {format_metric(global_row['mistral_correct_rate'])}",
        f"Écart Mistral - OpenAI : {format_metric(global_row['mistral_minus_openai_correct_rate'])}",
        "",
        "PROVIDERS — ORDRE ALPHABÉTIQUE, SANS CLASSEMENT",
        "-" * 84,
    ]

    for _, row in summary_by_provider_df.iterrows():
        summary_lines.append(
            f"{row['provider']:<16} "
            f"N={int(row['n_comparable_pairs']):<5} "
            f"accord={format_metric(row['observed_agreement_rate'])} "
            f"kappa={format_metric(row['cohen_kappa'])} "
            f"delta_correct_M-O={format_metric(row['mistral_minus_openai_correct_rate'])}"
        )

    summary_lines.extend(
        [
            "",
            "QUALITÉ DE L'ANALYSE",
            "-" * 84,
            f"Erreurs détectées : {manifest['error_count']}",
            f"Avertissements : {manifest['warning_count']}",
            "",
            "RAPPORTS GÉNÉRÉS",
            "-" * 84,
            *[f"- {filename}" for filename in generated_reports],
            "",
            "LECTURE PRIORITAIRE",
            "-" * 84,
            "1. global_double_judge_summary.csv",
            "2. double_judge_summary_by_provider.csv",
            "3. analysis_quality_report.csv",
            "4. judge_disagreements.csv",
            "5. question_disagreement_frequency.csv",
            "",
            "IMPORTANT",
            "-" * 84,
            "Cette analyse décrit l'accord et les divergences entre deux juges.",
            "Elle ne constitue pas un classement des systèmes évalués.",
            "",
        ]
    )

    summary_text = "\n".join(summary_lines)
    (output_folder / "analysis_console_summary.txt").write_text(summary_text, encoding="utf-8")
    print(summary_text)

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyse TruthfulQA double-jugée : OpenAI historique ↔ Mistral niveau 1."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Dossier racine truthfulqa_12_models. Par défaut : dossier courant.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.expanduser().resolve()
    print(f"Analyse du dossier : {root}")
    exit_code = analyze(root)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
