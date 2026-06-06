#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_judge_disagreement_structure.py

Analyse interne de la structure des désaccords OpenAI ↔ Mistral
sur le corpus TruthfulQA double-jugé NeoMundi.

Le script utilise en priorité :
    comparable_pairs_internal.csv

Il peut aussi lire :
    judge_disagreements.csv

mais les calculs principaux reposent sur comparable_pairs_internal.csv,
car ce fichier contient les paires comparables ET les accords, nécessaires
pour calculer des taux fiables.

Objectif :
- décrire les directions de désaccord ;
- mesurer leur distribution par provider ;
- mesurer leur distribution par décision runtime et régime ;
- repérer les questions générant des divergences récurrentes ;
- produire un résumé interne exploitable pour la documentation ;
- ne générer aucun classement, rating ou score composite.

Le script ne modifie jamais les fichiers sources.

USAGE SIMPLE
------------
Option 1 — placer ce script dans le dossier gelé contenant
comparable_pairs_internal.csv, puis lancer :

    python .\analyze_judge_disagreement_structure.py

Option 2 — lancer depuis un autre dossier en indiquant la source :

    python .\analyze_judge_disagreement_structure.py `
        --input-dir ".\04_analysis_output\double_judge_analysis_v1_2026-06-06"

Option 3 — personnaliser le dossier de sortie :

    python .\analyze_judge_disagreement_structure.py `
        --input-dir ".\04_analysis_output\double_judge_analysis_v1_2026-06-06" `
        --output-dir ".\04_analysis_output\judge_disagreement_structure_v1_2026-06-06"
"""

from __future__ import annotations

import argparse
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

DEFAULT_INPUT_FILE = "comparable_pairs_internal.csv"
OPTIONAL_DISAGREEMENT_FILE = "judge_disagreements.csv"
DEFAULT_OUTPUT_SUBDIR = "judge_disagreement_structure"

RUNTIME_DIMENSIONS = [
    "decision",
    "regime",
    "dg_profile",
    "dg_flagged",
    "flagged",
    "hallucination",
]

NULL_LIKE = {
    "",
    "nan",
    "none",
    "null",
    "n/a",
    "na",
    "missing",
    "<missing>",
}

TRUE_LIKE = {"true", "1", "yes", "y", "correct", "ok", "pass", "passed"}
FALSE_LIKE = {"false", "0", "no", "n", "incorrect", "ko", "fail", "failed"}

EXPECTED_DIRECTIONS = {
    "agreement",
    "openai_incorrect_mistral_correct",
    "openai_correct_mistral_incorrect",
}


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def normalize_column_name(name: object) -> str:
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")


def normalize_scalar(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def normalize_category(value: object) -> str:
    normalized = normalize_scalar(value)
    return normalized if normalized else "<missing>"


def parse_bool(value: object) -> Optional[bool]:
    if pd.isna(value):
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value == 1:
            return True
        if value == 0:
            return False

    normalized = normalize_scalar(value).lower()
    if normalized in TRUE_LIKE:
        return True
    if normalized in FALSE_LIKE:
        return False
    if normalized in NULL_LIKE:
        return None
    return None


def safe_div(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator else float("nan")


def format_metric(value: object, digits: int = 4) -> str:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)

    if math.isnan(numeric):
        return "NA"

    return f"{numeric:.{digits}f}"


def read_csv_flexible(path: Path) -> pd.DataFrame:
    attempts: list[str] = []

    for encoding in ["utf-8-sig", "utf-8", "cp1252", "latin-1"]:
        for separator in [",", ";", "\t"]:
            try:
                df = pd.read_csv(
                    path,
                    encoding=encoding,
                    sep=separator,
                    dtype=object,
                    low_memory=False,
                )
                if len(df.columns) > 1:
                    return df
                attempts.append(f"{encoding}/{repr(separator)}: une seule colonne")
            except Exception as exc:  # noqa: BLE001
                attempts.append(f"{encoding}/{repr(separator)}: {type(exc).__name__}")

    for encoding in ["utf-8-sig", "utf-8", "cp1252", "latin-1"]:
        try:
            return pd.read_csv(
                path,
                encoding=encoding,
                sep=None,
                engine="python",
                dtype=object,
            )
        except Exception as exc:  # noqa: BLE001
            attempts.append(f"{encoding}/auto: {type(exc).__name__}")

    raise RuntimeError("Impossible de lire le CSV : " + " | ".join(attempts))


def find_input_dir(explicit_input_dir: Optional[Path]) -> Path:
    if explicit_input_dir:
        candidate = explicit_input_dir.expanduser().resolve()
        if (candidate / DEFAULT_INPUT_FILE).exists():
            return candidate
        raise FileNotFoundError(
            f"Le dossier indiqué ne contient pas {DEFAULT_INPUT_FILE} : {candidate}"
        )

    cwd = Path.cwd().resolve()

    # Cas 1 : exécution directement dans le dossier gelé.
    if (cwd / DEFAULT_INPUT_FILE).exists():
        return cwd

    # Cas 2 : emplacements probables depuis la racine du corpus.
    preferred_candidates = [
        cwd / "04_analysis_output" / "double_judge_analysis_v1_2026-06-06",
        cwd / "04_analysis_output" / "double_judge_analysis",
        cwd / "double_judge_analysis_v1_2026-06-06",
        cwd / "double_judge_analysis",
    ]

    for candidate in preferred_candidates:
        if (candidate / DEFAULT_INPUT_FILE).exists():
            return candidate.resolve()

    # Cas 3 : recherche récursive prudente.
    candidates = sorted(
        {
            path.parent.resolve()
            for path in cwd.rglob(DEFAULT_INPUT_FILE)
            if path.is_file()
        }
    )

    if not candidates:
        raise FileNotFoundError(
            f"Aucun fichier {DEFAULT_INPUT_FILE} trouvé depuis : {cwd}"
        )

    # Priorité aux dossiers gelés v1 si plusieurs candidats existent.
    frozen_candidates = [
        path for path in candidates if "double_judge_analysis_v1" in path.name.lower()
    ]

    if len(frozen_candidates) == 1:
        return frozen_candidates[0]

    if len(candidates) == 1:
        return candidates[0]

    formatted = "\n".join(f"  - {candidate}" for candidate in candidates)
    raise RuntimeError(
        "Plusieurs dossiers candidats détectés. Relance avec --input-dir.\n"
        + formatted
    )


def validate_required_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized_map = {
        normalize_column_name(column): str(column)
        for column in df.columns
    }

    required = [
        "provider",
        "question_id",
        "agreement",
        "disagreement_direction",
    ]

    missing = [
        column for column in required
        if normalize_column_name(column) not in normalized_map
    ]

    if missing:
        raise ValueError(
            "Colonnes obligatoires absentes : " + ", ".join(missing)
        )

    rename_map = {}
    for required_column in required:
        actual = normalized_map[normalize_column_name(required_column)]
        if actual != required_column:
            rename_map[actual] = required_column

    return df.rename(columns=rename_map)


def ensure_boolean_agreement(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working["agreement"] = working["agreement"].map(parse_bool)

    if working["agreement"].isna().any():
        count = int(working["agreement"].isna().sum())
        raise ValueError(
            f"{count} valeurs de la colonne agreement ne sont pas interprétables."
        )

    working["agreement"] = working["agreement"].astype(bool)
    return working


def clean_direction(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working["disagreement_direction"] = (
        working["disagreement_direction"]
        .map(normalize_scalar)
        .str.lower()
    )

    # Reconstruction défensive si la direction est absente ou incohérente.
    if {
        "openai_is_correct_parsed",
        "mistral_is_correct_parsed",
    }.issubset(set(working.columns)):
        openai_bool = working["openai_is_correct_parsed"].map(parse_bool)
        mistral_bool = working["mistral_is_correct_parsed"].map(parse_bool)

        reconstructed = pd.Series("agreement", index=working.index, dtype=object)

        reconstructed.loc[
            (openai_bool == False) & (mistral_bool == True)  # noqa: E712
        ] = "openai_incorrect_mistral_correct"

        reconstructed.loc[
            (openai_bool == True) & (mistral_bool == False)  # noqa: E712
        ] = "openai_correct_mistral_incorrect"

        invalid = ~working["disagreement_direction"].isin(EXPECTED_DIRECTIONS)
        working.loc[invalid, "disagreement_direction"] = reconstructed.loc[invalid]

    unknown = ~working["disagreement_direction"].isin(EXPECTED_DIRECTIONS)
    if unknown.any():
        values = sorted(set(working.loc[unknown, "disagreement_direction"]))
        raise ValueError(
            "Directions de désaccord non reconnues : " + " | ".join(values)
        )

    return working


def normalize_runtime_dimensions(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    for dimension in RUNTIME_DIMENSIONS:
        if dimension in working.columns:
            working[dimension] = working[dimension].map(normalize_category)
    return working


# ---------------------------------------------------------------------------
# Agrégations
# ---------------------------------------------------------------------------

def build_global_direction_summary(df: pd.DataFrame) -> pd.DataFrame:
    total = len(df)

    grouped = (
        df.groupby("disagreement_direction", dropna=False)
        .size()
        .reset_index(name="pair_count")
    )

    grouped["pair_rate"] = grouped["pair_count"] / total if total else float("nan")

    expected_order = [
        "agreement",
        "openai_incorrect_mistral_correct",
        "openai_correct_mistral_incorrect",
    ]

    grouped["direction_order"] = grouped["disagreement_direction"].map(
        {direction: index for index, direction in enumerate(expected_order)}
    )

    grouped = (
        grouped.sort_values("direction_order", kind="stable")
        .drop(columns=["direction_order"])
        .reset_index(drop=True)
    )

    return grouped


def build_provider_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("provider", dropna=False)
        .agg(
            comparable_pair_count=("agreement", "size"),
            agreement_count=("agreement", "sum"),
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

    grouped["agreement_rate"] = grouped["agreement_count"] / grouped["comparable_pair_count"]
    grouped["disagreement_rate"] = grouped["disagreement_count"] / grouped["comparable_pair_count"]

    grouped["openai_incorrect_mistral_correct_rate"] = (
        grouped["openai_incorrect_mistral_correct_count"]
        / grouped["comparable_pair_count"]
    )

    grouped["openai_correct_mistral_incorrect_rate"] = (
        grouped["openai_correct_mistral_incorrect_count"]
        / grouped["comparable_pair_count"]
    )

    grouped["directional_imbalance_count"] = (
        grouped["openai_incorrect_mistral_correct_count"]
        - grouped["openai_correct_mistral_incorrect_count"]
    )

    grouped["directional_imbalance_rate"] = (
        grouped["directional_imbalance_count"]
        / grouped["comparable_pair_count"]
    )

    # Ordre alphabétique volontaire : aucune logique de classement.
    return grouped.sort_values("provider", kind="stable").reset_index(drop=True)


def build_provider_dimension_summary(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if dimension not in df.columns:
        return pd.DataFrame()

    grouped = (
        df.groupby(["provider", dimension], dropna=False)
        .agg(
            comparable_pair_count=("agreement", "size"),
            agreement_count=("agreement", "sum"),
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

    grouped["agreement_rate"] = grouped["agreement_count"] / grouped["comparable_pair_count"]
    grouped["disagreement_rate"] = grouped["disagreement_count"] / grouped["comparable_pair_count"]

    grouped["directional_imbalance_count"] = (
        grouped["openai_incorrect_mistral_correct_count"]
        - grouped["openai_correct_mistral_incorrect_count"]
    )

    grouped["directional_imbalance_rate"] = (
        grouped["directional_imbalance_count"]
        / grouped["comparable_pair_count"]
    )

    return grouped.sort_values(["provider", dimension], kind="stable").reset_index(drop=True)


def build_global_dimension_summary(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if dimension not in df.columns:
        return pd.DataFrame()

    grouped = (
        df.groupby(dimension, dropna=False)
        .agg(
            comparable_pair_count=("agreement", "size"),
            provider_count=("provider", "nunique"),
            agreement_count=("agreement", "sum"),
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

    grouped["agreement_rate"] = grouped["agreement_count"] / grouped["comparable_pair_count"]
    grouped["disagreement_rate"] = grouped["disagreement_count"] / grouped["comparable_pair_count"]

    grouped["directional_imbalance_count"] = (
        grouped["openai_incorrect_mistral_correct_count"]
        - grouped["openai_correct_mistral_incorrect_count"]
    )

    grouped["directional_imbalance_rate"] = (
        grouped["directional_imbalance_count"]
        / grouped["comparable_pair_count"]
    )

    return grouped.sort_values(dimension, kind="stable").reset_index(drop=True)


def build_question_frequency(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("question_id", dropna=False)
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
        grouped["disagreement_count"]
        / grouped["comparable_pair_count"]
    )

    grouped["directional_imbalance_count"] = (
        grouped["openai_incorrect_mistral_correct_count"]
        - grouped["openai_correct_mistral_incorrect_count"]
    )

    if "question" in df.columns:
        lookup = (
            df[["question_id", "question"]]
            .drop_duplicates(subset=["question_id"], keep="first")
        )
        grouped = grouped.merge(lookup, on="question_id", how="left")

    # Ici, le tri par fréquence sert à repérer les zones de friction des juges.
    # Il ne s'agit pas d'un classement des providers.
    return grouped.sort_values(
        ["disagreement_count", "disagreement_rate", "question_id"],
        ascending=[False, False, True],
        kind="stable",
    ).reset_index(drop=True)


def build_high_disagreement_questions(
    question_frequency: pd.DataFrame,
    min_disagreement_count: int,
    min_disagreement_rate: float,
) -> pd.DataFrame:
    return (
        question_frequency.loc[
            (question_frequency["disagreement_count"] >= min_disagreement_count)
            | (
                (question_frequency["disagreement_count"] >= 2)
                & (question_frequency["disagreement_rate"] >= min_disagreement_rate)
            )
        ]
        .copy()
        .reset_index(drop=True)
    )


def build_disagreement_rows(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "provider",
        "question_id",
        "question",
        "disagreement_direction",
        "openai_verdict_source",
        "mistral_verdict_source",
        "openai_is_correct_parsed",
        "mistral_is_correct_parsed",
        "decision",
        "regime",
        "dg_profile",
        "dg_flagged",
        "flagged",
        "hallucination",
    ]

    available = [column for column in columns if column in df.columns]

    return (
        df.loc[~df["agreement"], available]
        .sort_values(["provider", "question_id"], kind="stable")
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------------
# Résumé texte
# ---------------------------------------------------------------------------

def build_summary_text(
    input_dir: Path,
    output_dir: Path,
    all_pairs: pd.DataFrame,
    direction_summary: pd.DataFrame,
    provider_summary: pd.DataFrame,
    high_questions: pd.DataFrame,
    generated_files: list[str],
    min_disagreement_count: int,
    min_disagreement_rate: float,
) -> str:
    total = len(all_pairs)
    disagreement_count = int((~all_pairs["agreement"]).sum())
    agreement_count = int(all_pairs["agreement"].sum())

    direction_lookup = {
        row["disagreement_direction"]: int(row["pair_count"])
        for _, row in direction_summary.iterrows()
    }

    mistral_more_permissive = direction_lookup.get(
        "openai_incorrect_mistral_correct", 0
    )

    openai_more_permissive = direction_lookup.get(
        "openai_correct_mistral_incorrect", 0
    )

    provider_positive_imbalance_count = int(
        (provider_summary["directional_imbalance_count"] > 0).sum()
    )

    provider_negative_imbalance_count = int(
        (provider_summary["directional_imbalance_count"] < 0).sum()
    )

    provider_neutral_count = int(
        (provider_summary["directional_imbalance_count"] == 0).sum()
    )

    lines = [
        "ANALYSE DE LA STRUCTURE DES DESACCORDS — NEO MUNDI",
        "=" * 88,
        f"Généré le : {datetime.now().isoformat(timespec='seconds')}",
        f"Dossier source : {input_dir}",
        f"Dossier de sortie : {output_dir}",
        "",
        "CORPUS ANALYSE",
        "-" * 88,
        f"Providers analysés : {provider_summary['provider'].nunique()}",
        f"Paires comparables : {total}",
        f"Accords : {agreement_count}",
        f"Désaccords : {disagreement_count}",
        f"Taux de désaccord : {format_metric(safe_div(disagreement_count, total))}",
        "",
        "DIRECTIONS DES DESACCORDS",
        "-" * 88,
        (
            "OpenAI incorrect / Mistral correct : "
            f"{mistral_more_permissive} "
            f"({format_metric(safe_div(mistral_more_permissive, total))})"
        ),
        (
            "OpenAI correct / Mistral incorrect : "
            f"{openai_more_permissive} "
            f"({format_metric(safe_div(openai_more_permissive, total))})"
        ),
        (
            "Solde directionnel Mistral - OpenAI : "
            f"{mistral_more_permissive - openai_more_permissive}"
        ),
        "",
        "TRANSVERSALITE PAR PROVIDER",
        "-" * 88,
        (
            "Providers avec davantage de cas OpenAI incorrect / Mistral correct : "
            f"{provider_positive_imbalance_count}"
        ),
        (
            "Providers avec davantage de cas OpenAI correct / Mistral incorrect : "
            f"{provider_negative_imbalance_count}"
        ),
        f"Providers avec solde directionnel nul : {provider_neutral_count}",
        "",
        "QUESTIONS A FORTE DIVERGENCE",
        "-" * 88,
        (
            f"Seuil utilisé : au moins {min_disagreement_count} désaccords "
            f"OU au moins 2 désaccords avec un taux >= {min_disagreement_rate:.2f}"
        ),
        f"Questions retenues : {len(high_questions)}",
        "",
        "PROVIDERS — ORDRE ALPHABETIQUE, SANS CLASSEMENT",
        "-" * 88,
    ]

    for _, row in provider_summary.iterrows():
        lines.append(
            f"{str(row['provider']):<16} "
            f"N={int(row['comparable_pair_count']):<5} "
            f"desaccords={int(row['disagreement_count']):<4} "
            f"taux={format_metric(row['disagreement_rate'])} "
            f"Mplus={int(row['openai_incorrect_mistral_correct_count']):<4} "
            f"Oplus={int(row['openai_correct_mistral_incorrect_count']):<4} "
            f"solde={int(row['directional_imbalance_count'])}"
        )

    lines.extend(
        [
            "",
            "RAPPORTS GENERES",
            "-" * 88,
            *[f"- {filename}" for filename in generated_files],
            "",
            "INTERPRETATION PRUDENTE",
            "-" * 88,
            (
                "Cette analyse documente la structure des divergences entre deux juges. "
                "Elle ne permet pas, à elle seule, de déterminer lequel constitue "
                "une référence absolue."
            ),
            (
                "Un solde directionnel positif signifie uniquement que Mistral attribue "
                "plus souvent un verdict correct dans les cas de désaccord."
            ),
            (
                "Aucun classement, rating ou score composite des providers n'est produit."
            ),
            "",
        ]
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Analyse principale
# ---------------------------------------------------------------------------

def analyze(
    input_dir: Path,
    output_dir: Path,
    min_disagreement_count: int,
    min_disagreement_rate: float,
) -> int:
    input_file = input_dir / DEFAULT_INPUT_FILE

    if not input_file.exists():
        raise FileNotFoundError(f"Fichier absent : {input_file}")

    output_dir.mkdir(parents=True, exist_ok=True)

    df = read_csv_flexible(input_file)
    df = validate_required_columns(df)
    df = ensure_boolean_agreement(df)
    df = clean_direction(df)
    df = normalize_runtime_dimensions(df)

    # Normalisation légère des identifiants.
    df["provider"] = df["provider"].map(normalize_category)
    df["question_id"] = df["question_id"].map(normalize_category)

    direction_summary = build_global_direction_summary(df)
    provider_summary = build_provider_summary(df)
    question_frequency = build_question_frequency(df)
    high_questions = build_high_disagreement_questions(
        question_frequency,
        min_disagreement_count=min_disagreement_count,
        min_disagreement_rate=min_disagreement_rate,
    )
    disagreements = build_disagreement_rows(df)

    generated_files = [
        "disagreement_direction_summary.csv",
        "disagreement_by_provider.csv",
        "disagreement_by_question_frequency.csv",
        "high_disagreement_questions.csv",
        "disagreement_rows_internal.csv",
    ]

    direction_summary.to_csv(
        output_dir / "disagreement_direction_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    provider_summary.to_csv(
        output_dir / "disagreement_by_provider.csv",
        index=False,
        encoding="utf-8-sig",
    )

    question_frequency.to_csv(
        output_dir / "disagreement_by_question_frequency.csv",
        index=False,
        encoding="utf-8-sig",
    )

    high_questions.to_csv(
        output_dir / "high_disagreement_questions.csv",
        index=False,
        encoding="utf-8-sig",
    )

    disagreements.to_csv(
        output_dir / "disagreement_rows_internal.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Exports par dimensions runtime.
    dimension_files: list[str] = []

    for dimension in RUNTIME_DIMENSIONS:
        if dimension not in df.columns:
            continue

        provider_dimension = build_provider_dimension_summary(df, dimension)
        global_dimension = build_global_dimension_summary(df, dimension)

        provider_filename = f"disagreement_by_provider_and_{dimension}.csv"
        global_filename = f"disagreement_by_{dimension}_global.csv"

        provider_dimension.to_csv(
            output_dir / provider_filename,
            index=False,
            encoding="utf-8-sig",
        )

        global_dimension.to_csv(
            output_dir / global_filename,
            index=False,
            encoding="utf-8-sig",
        )

        dimension_files.extend([provider_filename, global_filename])

    generated_files.extend(dimension_files)

    summary_text = build_summary_text(
        input_dir=input_dir,
        output_dir=output_dir,
        all_pairs=df,
        direction_summary=direction_summary,
        provider_summary=provider_summary,
        high_questions=high_questions,
        generated_files=[
            *generated_files,
            "disagreement_structure_manifest.json",
            "disagreement_structure_summary.txt",
        ],
        min_disagreement_count=min_disagreement_count,
        min_disagreement_rate=min_disagreement_rate,
    )

    (output_dir / "disagreement_structure_summary.txt").write_text(
        summary_text,
        encoding="utf-8",
    )

    total = len(df)
    disagreement_count = int((~df["agreement"]).sum())

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_dir": str(input_dir.resolve()),
        "input_file": str(input_file.resolve()),
        "output_dir": str(output_dir.resolve()),
        "methodology": (
            "Internal descriptive analysis of disagreement structure between "
            "OpenAI historical judge and Mistral level 1 judge."
        ),
        "provider_count": int(provider_summary["provider"].nunique()),
        "comparable_pair_count": int(total),
        "agreement_count": int(df["agreement"].sum()),
        "disagreement_count": disagreement_count,
        "disagreement_rate": safe_div(disagreement_count, total),
        "high_disagreement_question_thresholds": {
            "min_disagreement_count": min_disagreement_count,
            "min_disagreement_rate_with_at_least_two_disagreements": min_disagreement_rate,
        },
        "high_disagreement_question_count": int(len(high_questions)),
        "runtime_dimensions_exported": [
            dimension for dimension in RUNTIME_DIMENSIONS
            if dimension in df.columns
        ],
        "generated_files": [
            *generated_files,
            "disagreement_structure_manifest.json",
            "disagreement_structure_summary.txt",
        ],
        "notes": [
            "No ranking, rating, leaderboard or composite score is produced.",
            "Provider rows are exported in alphabetical order.",
            "Question frequency sorting is used only to locate recurring judge-friction zones.",
            "This analysis cannot determine which judge is absolutely correct.",
        ],
    }

    with (output_dir / "disagreement_structure_manifest.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)

    print(summary_text)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyse de la structure des désaccords OpenAI ↔ Mistral."
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help=(
            "Dossier contenant comparable_pairs_internal.csv. "
            "Si omis, le script tente une détection automatique."
        ),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Dossier de sortie. Par défaut : sous-dossier "
            "'judge_disagreement_structure' dans le dossier source."
        ),
    )

    parser.add_argument(
        "--min-disagreement-count",
        type=int,
        default=4,
        help=(
            "Nombre minimal de désaccords pour retenir automatiquement "
            "une question à forte divergence. Défaut : 4."
        ),
    )

    parser.add_argument(
        "--min-disagreement-rate",
        type=float,
        default=0.50,
        help=(
            "Taux minimal de désaccord pour retenir une question ayant "
            "au moins deux désaccords. Défaut : 0.50."
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        input_dir = find_input_dir(args.input_dir)

        if args.output_dir:
            output_dir = args.output_dir.expanduser().resolve()
        else:
            output_dir = input_dir / DEFAULT_OUTPUT_SUBDIR

        print(f"Dossier source détecté : {input_dir}")
        print(f"Dossier de sortie : {output_dir}")
        print()

        exit_code = analyze(
            input_dir=input_dir,
            output_dir=output_dir,
            min_disagreement_count=args.min_disagreement_count,
            min_disagreement_rate=args.min_disagreement_rate,
        )

        sys.exit(exit_code)

    except Exception as exc:  # noqa: BLE001
        print(f"ERREUR : {type(exc).__name__}: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
