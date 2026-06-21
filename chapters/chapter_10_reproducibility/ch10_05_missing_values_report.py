# -*- coding: utf-8 -*-
"""
Chapter 10 standalone reproducibility script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 10.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 10 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_10_reproducibility/ch10_05_missing_values_report.py

Expected before running:
    uv run python generate_data.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
FIGURE_DIR = PROJECT_ROOT / "figure"
REPORT_DIR = PROJECT_ROOT / "report"


def set_scientific_style() -> None:
    """
    RU:
        Единый академический стиль для воспроизводимых рисунков.

    EN:
        Unified academic style for reproducible figures.
    """
    sns.set_theme(context="paper", style="ticks", palette="colorblind")
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "axes.linewidth": 1.0,
        "lines.linewidth": 1.8,
        "lines.markersize": 6,
        "figure.dpi": 120,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
    })


def load_dataset(filename: str) -> pd.DataFrame:
    """
    RU:
        Загружает CSV из data/processed/.
        Если файла нет, сначала запустите generate_data.py.

    EN:
        Loads a CSV file from data/processed/.
        If the file is missing, run generate_data.py first.
    """
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Run first: uv run python generate_data.py"
        )
    return pd.read_csv(path, encoding="utf-8-sig")


def save_figure(fig: plt.Figure, name: str, formats: tuple[str, ...] = ("png", "pdf", "tiff")) -> None:
    """
    RU:
        Сохраняет рисунок в указанных форматах в папку figure/.

    EN:
        Saves the figure in the requested formats into the figure/ folder.
    """
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    for ext in formats:
        path = FIGURE_DIR / f"{name}.{ext}"
        fig.savefig(path, dpi=600, bbox_inches="tight", facecolor="white")
        print(f"Saved: {path}")


FIGURE_ID = "ch10_05_missing_values_report"


def build_figure(missing: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 10.5. Тезис: отчёт о пропущенных значениях должен быть
        частью воспроизводимого анализа, даже если пропусков нет.

    EN:
        Subsection 10.5. Thesis: a missing-value report should be part of
        reproducible analysis, even if no values are missing.
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    ax.barh(missing["variable"], missing["missing_n"], edgecolor="black")
    ax.set_xlabel("Число пропусков")
    ax.set_ylabel("Переменная")
    ax.set_title("Отчёт о пропущенных значениях")
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")

    variables = ["age_years", "bmi_kg_m2", "sbp_mm_hg", "glucose_mmol_l", "ldl_mmol_l"]
    missing = pd.DataFrame({
        "variable": variables,
        "missing_n": [df[v].isna().sum() for v in variables],
        "missing_percent": [df[v].isna().mean() * 100 for v in variables],
    })

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / "ch10_05_missing_values_report.csv"
    missing.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Saved missing-value report: {output_path}")

    fig = build_figure(missing)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
