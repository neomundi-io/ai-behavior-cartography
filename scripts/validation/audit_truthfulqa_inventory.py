#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_truthfulqa_inventory.py

Audit technique du corpus TruthfulQA double-jugé NeoMundi.

Arborescence attendue :
truthfulqa_12_models/
├── 01_raw_results/
├── 02_openai_judged/
├── 03_mistral_judged/
├── 04_analysis_output/
└── audit_truthfulqa_inventory.py

Le script :
- détecte automatiquement les providers ;
- apparie RAW / OpenAI / Mistral niveau 1 ;
- vérifie les volumes, doublons, question_id et schémas ;
- contrôle l'alignement des réponses ;
- détecte les verdicts manquants ;
- produit des rapports CSV et un résumé texte ;
- ne modifie jamais les fichiers sources.

Usage PowerShell :
    python .\audit_truthfulqa_inventory.py
ou :
    python .\audit_truthfulqa_inventory.py --root "C:\chemin\vers\truthfulqa_12_models"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_DIR = "01_raw_results"
OPENAI_DIR = "02_openai_judged"
MISTRAL_DIR = "03_mistral_judged"
OUTPUT_DIR = "04_analysis_output"

RAW_PATTERN = re.compile(r"^truthfulqa_(?P<provider>.+?)_dg_results\.csv$", re.IGNORECASE)
OPENAI_PATTERN = re.compile(r"^truthfulqa_(?P<provider>.+?)_judged\.csv$", re.IGNORECASE)
MISTRAL_PATTERN = re.compile(r"^truthfulqa_(?P<provider>.+?)_mistral_judged\.csv$", re.IGNORECASE)

QUESTION_ID_ALIASES = [
    "question_id",
    "questionid",
    "id",
    "qid",
    "question_index",
    "question_idx",
]

QUESTION_TEXT_ALIASES = [
    "question",
    "prompt",
    "question_text",
    "input",
    "query",
]

ANSWER_ALIASES = [
    "answer",
    "response",
    "model_response",
    "generated_answer",
    "assistant_response",
    "output",
    "completion",
]

OPENAI_VERDICT_ALIASES = [
    "judge_verdict",
    "openai_judge_verdict",
    "openai_verdict",
    "verdict",
]

OPENAI_CORRECT_ALIASES = [
    "is_correct",
    "openai_is_correct",
    "judge_is_correct",
]

MISTRAL_VERDICT_ALIASES = [
    "mistral_judge_verdict",
    "mistral_verdict",
    "judge_verdict",
    "verdict",
]

MISTRAL_CORRECT_ALIASES = [
    "mistral_is_correct",
    "is_correct",
    "judge_is_correct",
]

NULL_LIKE_STRINGS = {
    "",
    "nan",
    "none",
    "null",
    "n/a",
    "na",
    "missing",
}


# ---------------------------------------------------------------------------
# Structures
# ---------------------------------------------------------------------------

@dataclass
class FileRecord:
    provider: str
    layer: str
    file_name: str
    file_path: str
    exists: bool
    read_ok: bool = False
    encoding: str = ""
    separator: str = ""
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    question_id_column: str = ""
    question_text_column: str = ""
    answer_column: str = ""
    verdict_column: str = ""
    correct_column: str = ""
    unique_question_ids: Optional[int] = None
    duplicate_question_ids: Optional[int] = None
    missing_question_ids: Optional[int] = None
    missing_verdicts: Optional[int] = None
    read_error: str = ""


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def normalize_provider(provider: str) -> str:
    """Normalise légèrement un identifiant provider sans écraser son sens."""
    return provider.strip().lower().replace("-", "_").replace(" ", "_")


def normalize_column_name(name: object) -> str:
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")


def normalize_scalar(value: object) -> str:
    """Normalise une valeur pour comparer les contenus entre fichiers."""
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def is_missing_value(value: object) -> bool:
    if pd.isna(value):
        return True
    return normalize_scalar(value).lower() in NULL_LIKE_STRINGS


def find_column(df: pd.DataFrame, aliases: Iterable[str]) -> str:
    normalized_map = {normalize_column_name(col): str(col) for col in df.columns}
    for alias in aliases:
        normalized_alias = normalize_column_name(alias)
        if normalized_alias in normalized_map:
            return normalized_map[normalized_alias]
    return ""


def safe_int(value: Optional[int]) -> object:
    return "" if value is None else value


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

    # Dernier essai : détection automatique du séparateur.
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
    """
    Retourne {provider_normalisé: chemin_csv}.
    Ignore volontairement les fichiers qui ne correspondent pas exactement
    au format attendu, par exemple *_independent_judged.csv.
    """
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
    category: str,
    severity: str,
    detail: str,
    layer: str = "",
) -> None:
    issues.append(
        {
            "provider": provider,
            "layer": layer,
            "category": category,
            "severity": severity,
            "detail": detail,
        }
    )


def build_file_record(provider: str, layer: str, path: Optional[Path]) -> tuple[FileRecord, Optional[pd.DataFrame]]:
    if path is None:
        return (
            FileRecord(
                provider=provider,
                layer=layer,
                file_name="",
                file_path="",
                exists=False,
            ),
            None,
        )

    record = FileRecord(
        provider=provider,
        layer=layer,
        file_name=path.name,
        file_path=str(path.resolve()),
        exists=True,
    )

    try:
        df, encoding, separator = read_csv_flexible(path)
        record.read_ok = True
        record.encoding = encoding
        record.separator = separator
        record.row_count = len(df)
        record.column_count = len(df.columns)

        record.question_id_column = find_column(df, QUESTION_ID_ALIASES)
        record.question_text_column = find_column(df, QUESTION_TEXT_ALIASES)
        record.answer_column = find_column(df, ANSWER_ALIASES)

        if layer == "openai":
            record.verdict_column = find_column(df, OPENAI_VERDICT_ALIASES)
            record.correct_column = find_column(df, OPENAI_CORRECT_ALIASES)
        elif layer == "mistral":
            record.verdict_column = find_column(df, MISTRAL_VERDICT_ALIASES)
            record.correct_column = find_column(df, MISTRAL_CORRECT_ALIASES)

        if record.question_id_column:
            qids = df[record.question_id_column]
            record.missing_question_ids = int(qids.isna().sum())
            non_null_qids = qids.dropna().map(normalize_scalar)
            record.unique_question_ids = int(non_null_qids.nunique())
            record.duplicate_question_ids = int(non_null_qids.duplicated().sum())

        verdict_source = record.correct_column or record.verdict_column
        if verdict_source:
            record.missing_verdicts = int(df[verdict_source].map(is_missing_value).sum())

        return record, df

    except Exception as exc:  # noqa: BLE001
        record.read_error = f"{type(exc).__name__}: {exc}"
        return record, None


def compare_question_ids(
    provider: str,
    records: dict[str, FileRecord],
    frames: dict[str, Optional[pd.DataFrame]],
    issues: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    sets: dict[str, set[str]] = {}
    for layer in ["raw", "openai", "mistral"]:
        record = records[layer]
        df = frames[layer]
        if df is None or not record.question_id_column:
            sets[layer] = set()
            continue
        sets[layer] = set(df[record.question_id_column].dropna().map(normalize_scalar))

    comparisons = [
        ("raw", "openai"),
        ("raw", "mistral"),
        ("openai", "mistral"),
    ]

    for left, right in comparisons:
        left_set = sets[left]
        right_set = sets[right]
        only_left = sorted(left_set - right_set)
        only_right = sorted(right_set - left_set)
        overlap = left_set & right_set

        rows.append(
            {
                "provider": provider,
                "comparison": f"{left}_vs_{right}",
                "left_unique_question_ids": len(left_set),
                "right_unique_question_ids": len(right_set),
                "intersection_count": len(overlap),
                "only_left_count": len(only_left),
                "only_right_count": len(only_right),
                "aligned": bool(left_set and right_set and not only_left and not only_right),
                "sample_only_left": " | ".join(only_left[:10]),
                "sample_only_right": " | ".join(only_right[:10]),
            }
        )

        if left_set and right_set and (only_left or only_right):
            add_issue(
                issues,
                provider,
                category="question_id_mismatch",
                severity="ERROR",
                layer=f"{left}_vs_{right}",
                detail=(
                    f"{len(only_left)} question_id uniquement dans {left}; "
                    f"{len(only_right)} uniquement dans {right}."
                ),
            )

    return rows


def compare_answers(
    provider: str,
    records: dict[str, FileRecord],
    frames: dict[str, Optional[pd.DataFrame]],
    issues: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    comparisons = [
        ("raw", "openai"),
        ("raw", "mistral"),
        ("openai", "mistral"),
    ]

    for left, right in comparisons:
        left_record = records[left]
        right_record = records[right]
        left_df = frames[left]
        right_df = frames[right]

        base_row: dict[str, object] = {
            "provider": provider,
            "comparison": f"{left}_vs_{right}",
            "comparison_possible": False,
            "matched_question_ids": 0,
            "identical_answers": 0,
            "different_answers": 0,
            "missing_answer_values": 0,
            "sample_different_question_ids": "",
            "note": "",
        }

        if left_df is None or right_df is None:
            base_row["note"] = "Comparaison impossible : fichier absent ou illisible."
            rows.append(base_row)
            continue

        if not left_record.question_id_column or not right_record.question_id_column:
            base_row["note"] = "Comparaison impossible : colonne question_id non détectée."
            rows.append(base_row)
            continue

        if not left_record.answer_column or not right_record.answer_column:
            base_row["note"] = "Comparaison impossible : colonne réponse non détectée."
            rows.append(base_row)
            continue

        left_view = left_df[[left_record.question_id_column, left_record.answer_column]].copy()
        right_view = right_df[[right_record.question_id_column, right_record.answer_column]].copy()

        left_view.columns = ["question_id", "answer_left"]
        right_view.columns = ["question_id", "answer_right"]

        left_view["question_id"] = left_view["question_id"].map(normalize_scalar)
        right_view["question_id"] = right_view["question_id"].map(normalize_scalar)

        # Les doublons ont déjà été signalés. On conserve la première occurrence
        # afin de produire une comparaison lisible.
        left_view = left_view.drop_duplicates(subset=["question_id"], keep="first")
        right_view = right_view.drop_duplicates(subset=["question_id"], keep="first")

        merged = left_view.merge(right_view, on="question_id", how="inner")
        merged["answer_left_norm"] = merged["answer_left"].map(normalize_scalar)
        merged["answer_right_norm"] = merged["answer_right"].map(normalize_scalar)

        missing_mask = (merged["answer_left_norm"] == "") | (merged["answer_right_norm"] == "")
        equal_mask = merged["answer_left_norm"] == merged["answer_right_norm"]
        different = merged.loc[~equal_mask & ~missing_mask, "question_id"].tolist()

        base_row.update(
            {
                "comparison_possible": True,
                "matched_question_ids": len(merged),
                "identical_answers": int(equal_mask.sum()),
                "different_answers": int((~equal_mask & ~missing_mask).sum()),
                "missing_answer_values": int(missing_mask.sum()),
                "sample_different_question_ids": " | ".join(different[:10]),
                "note": "",
            }
        )

        if different:
            add_issue(
                issues,
                provider,
                category="answer_mismatch",
                severity="ERROR",
                layer=f"{left}_vs_{right}",
                detail=f"{len(different)} réponses diffèrent malgré un question_id identique.",
            )

        rows.append(base_row)

    return rows


def schema_rows(provider: str, layer: str, record: FileRecord, df: Optional[pd.DataFrame]) -> list[dict[str, object]]:
    if df is None:
        return [
            {
                "provider": provider,
                "layer": layer,
                "column_position": "",
                "column_name": "",
                "normalized_column_name": "",
                "detected_role": "",
                "dtype": "",
                "non_null_count": "",
            }
        ]

    role_by_column = {
        record.question_id_column: "question_id",
        record.question_text_column: "question_text",
        record.answer_column: "answer",
        record.verdict_column: "verdict",
        record.correct_column: "is_correct",
    }

    rows = []
    for position, column in enumerate(df.columns, start=1):
        rows.append(
            {
                "provider": provider,
                "layer": layer,
                "column_position": position,
                "column_name": str(column),
                "normalized_column_name": normalize_column_name(column),
                "detected_role": role_by_column.get(str(column), ""),
                "dtype": str(df[column].dtype),
                "non_null_count": int(df[column].notna().sum()),
            }
        )
    return rows


def verdict_missing_rows(provider: str, layer: str, record: FileRecord, df: Optional[pd.DataFrame]) -> list[dict[str, object]]:
    if df is None:
        return []

    verdict_source = record.correct_column or record.verdict_column
    if not verdict_source:
        return []

    qid_col = record.question_id_column
    rows = []
    missing_mask = df[verdict_source].map(is_missing_value)

    for index, (_, row) in enumerate(df.loc[missing_mask].iterrows(), start=1):
        rows.append(
            {
                "provider": provider,
                "layer": layer,
                "verdict_source_column": verdict_source,
                "row_number_in_file": int(row.name) + 2 if isinstance(row.name, int) else "",
                "question_id": normalize_scalar(row[qid_col]) if qid_col else "",
                "missing_index": index,
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Audit principal
# ---------------------------------------------------------------------------

def audit(root: Path) -> int:
    raw_folder = root / RAW_DIR
    openai_folder = root / OPENAI_DIR
    mistral_folder = root / MISTRAL_DIR
    output_folder = root / OUTPUT_DIR
    output_folder.mkdir(parents=True, exist_ok=True)

    raw_files = scan_layer(raw_folder, RAW_PATTERN)
    openai_files = scan_layer(openai_folder, OPENAI_PATTERN)
    mistral_files = scan_layer(mistral_folder, MISTRAL_PATTERN)

    providers = sorted(set(raw_files) | set(openai_files) | set(mistral_files))

    issues: list[dict[str, object]] = []
    file_records: list[FileRecord] = []
    alignment_rows: list[dict[str, object]] = []
    answer_rows: list[dict[str, object]] = []
    schema_report_rows: list[dict[str, object]] = []
    missing_verdict_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    required_dirs = [raw_folder, openai_folder, mistral_folder]
    missing_dirs = [str(path) for path in required_dirs if not path.exists()]
    if missing_dirs:
        print("ERREUR : dossiers requis absents :")
        for path in missing_dirs:
            print(f"  - {path}")
        return 2

    if not providers:
        print("ERREUR : aucun provider détecté.")
        return 2

    for provider in providers:
        records: dict[str, FileRecord] = {}
        frames: dict[str, Optional[pd.DataFrame]] = {}

        for layer, path in [
            ("raw", raw_files.get(provider)),
            ("openai", openai_files.get(provider)),
            ("mistral", mistral_files.get(provider)),
        ]:
            record, df = build_file_record(provider, layer, path)
            records[layer] = record
            frames[layer] = df
            file_records.append(record)

            if not record.exists:
                add_issue(
                    issues,
                    provider,
                    category="missing_file",
                    severity="ERROR",
                    layer=layer,
                    detail=f"Fichier {layer} absent.",
                )
                continue

            if not record.read_ok:
                add_issue(
                    issues,
                    provider,
                    category="unreadable_csv",
                    severity="ERROR",
                    layer=layer,
                    detail=record.read_error,
                )
                continue

            if not record.question_id_column:
                add_issue(
                    issues,
                    provider,
                    category="missing_question_id_column",
                    severity="ERROR",
                    layer=layer,
                    detail="Aucune colonne question_id reconnue.",
                )

            if record.question_id_column and record.duplicate_question_ids:
                add_issue(
                    issues,
                    provider,
                    category="duplicate_question_ids",
                    severity="ERROR",
                    layer=layer,
                    detail=f"{record.duplicate_question_ids} question_id dupliqués.",
                )

            if record.question_id_column and record.missing_question_ids:
                add_issue(
                    issues,
                    provider,
                    category="missing_question_ids",
                    severity="ERROR",
                    layer=layer,
                    detail=f"{record.missing_question_ids} question_id manquants.",
                )

            if layer in {"openai", "mistral"}:
                if not (record.correct_column or record.verdict_column):
                    add_issue(
                        issues,
                        provider,
                        category="missing_verdict_column",
                        severity="ERROR",
                        layer=layer,
                        detail="Aucune colonne de verdict reconnue.",
                    )
                elif record.missing_verdicts:
                    add_issue(
                        issues,
                        provider,
                        category="missing_verdicts",
                        severity="WARNING",
                        layer=layer,
                        detail=f"{record.missing_verdicts} verdicts manquants.",
                    )

            if not record.answer_column:
                add_issue(
                    issues,
                    provider,
                    category="missing_answer_column",
                    severity="WARNING",
                    layer=layer,
                    detail="Aucune colonne de réponse reconnue : comparaison des réponses impossible.",
                )

            schema_report_rows.extend(schema_rows(provider, layer, record, df))
            if layer in {"openai", "mistral"}:
                missing_verdict_rows.extend(verdict_missing_rows(provider, layer, record, df))

        alignment_rows.extend(compare_question_ids(provider, records, frames, issues))
        answer_rows.extend(compare_answers(provider, records, frames, issues))

        provider_issues = [issue for issue in issues if issue["provider"] == provider]
        provider_errors = sum(issue["severity"] == "ERROR" for issue in provider_issues)
        provider_warnings = sum(issue["severity"] == "WARNING" for issue in provider_issues)

        complete_triplet = all(records[layer].exists and records[layer].read_ok for layer in ["raw", "openai", "mistral"])
        qid_alignment_ok = all(
            row["aligned"]
            for row in alignment_rows
            if row["provider"] == provider
        ) if complete_triplet else False

        answer_comparisons_for_provider = [
            row for row in answer_rows if row["provider"] == provider and row["comparison_possible"]
        ]
        answers_aligned_ok = (
            bool(answer_comparisons_for_provider)
            and all(row["different_answers"] == 0 for row in answer_comparisons_for_provider)
        )

        summary_rows.append(
            {
                "provider": provider,
                "complete_triplet": complete_triplet,
                "raw_rows": safe_int(records["raw"].row_count),
                "openai_rows": safe_int(records["openai"].row_count),
                "mistral_rows": safe_int(records["mistral"].row_count),
                "raw_unique_question_ids": safe_int(records["raw"].unique_question_ids),
                "openai_unique_question_ids": safe_int(records["openai"].unique_question_ids),
                "mistral_unique_question_ids": safe_int(records["mistral"].unique_question_ids),
                "qid_alignment_ok": qid_alignment_ok,
                "answers_aligned_ok": answers_aligned_ok,
                "openai_missing_verdicts": safe_int(records["openai"].missing_verdicts),
                "mistral_missing_verdicts": safe_int(records["mistral"].missing_verdicts),
                "error_count": provider_errors,
                "warning_count": provider_warnings,
                "ready_for_double_judge_analysis": bool(
                    complete_triplet
                    and qid_alignment_ok
                    and answers_aligned_ok
                    and provider_errors == 0
                ),
            }
        )

    # -----------------------------------------------------------------------
    # Exports
    # -----------------------------------------------------------------------

    inventory_df = pd.DataFrame([asdict(record) for record in file_records])
    issues_df = pd.DataFrame(
        issues,
        columns=["provider", "layer", "category", "severity", "detail"],
    )
    summary_df = pd.DataFrame(summary_rows)
    alignment_df = pd.DataFrame(alignment_rows)
    answers_df = pd.DataFrame(answer_rows)
    schema_df = pd.DataFrame(schema_report_rows)
    missing_verdicts_df = pd.DataFrame(
        missing_verdict_rows,
        columns=[
            "provider",
            "layer",
            "verdict_source_column",
            "row_number_in_file",
            "question_id",
            "missing_index",
        ],
    )

    inventory_df.to_csv(output_folder / "row_counts_by_provider.csv", index=False, encoding="utf-8-sig")
    issues_df.to_csv(output_folder / "missing_or_mismatched_files.csv", index=False, encoding="utf-8-sig")
    summary_df.to_csv(output_folder / "inventory_audit_summary.csv", index=False, encoding="utf-8-sig")
    alignment_df.to_csv(output_folder / "question_id_alignment_report.csv", index=False, encoding="utf-8-sig")
    answers_df.to_csv(output_folder / "response_alignment_report.csv", index=False, encoding="utf-8-sig")
    schema_df.to_csv(output_folder / "schema_comparison_report.csv", index=False, encoding="utf-8-sig")
    missing_verdicts_df.to_csv(output_folder / "missing_verdicts_report.csv", index=False, encoding="utf-8-sig")

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(root.resolve()),
        "provider_count": len(providers),
        "providers": providers,
        "detected_files": {
            "raw": len(raw_files),
            "openai": len(openai_files),
            "mistral": len(mistral_files),
        },
        "ready_provider_count": int(summary_df["ready_for_double_judge_analysis"].sum()) if not summary_df.empty else 0,
        "error_count": int((issues_df["severity"] == "ERROR").sum()) if not issues_df.empty else 0,
        "warning_count": int((issues_df["severity"] == "WARNING").sum()) if not issues_df.empty else 0,
        "reports": [
            "inventory_audit_summary.csv",
            "missing_or_mismatched_files.csv",
            "row_counts_by_provider.csv",
            "question_id_alignment_report.csv",
            "response_alignment_report.csv",
            "schema_comparison_report.csv",
            "missing_verdicts_report.csv",
        ],
    }

    with (output_folder / "audit_manifest.json").open("w", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)

    summary_lines = [
        "AUDIT TRUTHFULQA — NEO MUNDI",
        "=" * 70,
        f"Généré le : {manifest['generated_at']}",
        f"Dossier racine : {manifest['root']}",
        "",
        f"Providers détectés : {manifest['provider_count']}",
        f"Fichiers RAW détectés : {manifest['detected_files']['raw']}",
        f"Fichiers OpenAI détectés : {manifest['detected_files']['openai']}",
        f"Fichiers Mistral niveau 1 détectés : {manifest['detected_files']['mistral']}",
        "",
        f"Providers prêts pour l'analyse double-jugée : {manifest['ready_provider_count']} / {manifest['provider_count']}",
        f"Erreurs bloquantes : {manifest['error_count']}",
        f"Avertissements : {manifest['warning_count']}",
        "",
        "PROVIDERS",
        "-" * 70,
    ]

    for row in summary_rows:
        status = "OK" if row["ready_for_double_judge_analysis"] else "A VERIFIER"
        summary_lines.append(
            f"{row['provider']:<16} {status:<12} "
            f"RAW={row['raw_rows']} OPENAI={row['openai_rows']} MISTRAL={row['mistral_rows']} "
            f"ERRORS={row['error_count']} WARNINGS={row['warning_count']}"
        )

    summary_lines.extend(
        [
            "",
            "RAPPORTS GENERES",
            "-" * 70,
            *[f"- {report}" for report in manifest["reports"]],
            "- audit_manifest.json",
            "- audit_console_summary.txt",
            "",
            "ETAPE SUIVANTE",
            "-" * 70,
            "Si les 12 providers sont marqués OK : lancer l'analyse OpenAI ↔ Mistral",
            "avec le futur script analyze_double_judge_truthfulqa.py.",
            "",
        ]
    )

    summary_text = "\n".join(summary_lines)
    (output_folder / "audit_console_summary.txt").write_text(summary_text, encoding="utf-8")
    print(summary_text)

    return 0 if manifest["error_count"] == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit du corpus TruthfulQA double-jugé NeoMundi."
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

    print(f"Audit du dossier : {root}")
    exit_code = audit(root)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
