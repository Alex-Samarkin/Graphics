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
    uv run python chapters/chapter_10_reproducibility/ch10_05_input_data_validation.py

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


FIGURE_ID = "ch10_05_input_data_validation"

REQUIRED_COLUMNS = {
    "patient_id",
    "therapy_group",
    "age_years",
    "bmi_kg_m2",
    "sbp_mm_hg",
    "glucose_mmol_l",
}


def validate_input(df: pd.DataFrame) -> None:
    """
    RU:
        Проверяет наличие обязательных колонок и базовые диапазоны.

    EN:
        Checks required columns and basic value ranges.
    """
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    checks = {
        "age_years": (18, 100),
        "bmi_kg_m2": (10, 70),
        "sbp_mm_hg": (60, 260),
        "glucose_mmol_l": (2, 30),
    }

    for column, (low, high) in checks.items():
        bad = df[~df[column].between(low, high)]
        if len(bad) > 0:
            raise ValueError(f"Column {column} has {len(bad)} values outside {low}..{high}")


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 10.5. Тезис: до построения графика нужно проверить,
        что входные данные имеют ожидаемые колонки и диапазоны.

    EN:
        Subsection 10.5. Thesis: before plotting, verify that input data
        have expected columns and ranges.
    """
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    sns.scatterplot(data=df, x="bmi_kg_m2", y="sbp_mm_hg", hue="therapy_group", alpha=0.65, ax=ax)
    ax.set_xlabel("ИМТ, кг/м²")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.set_title("График после проверки входных данных")
    ax.legend(title="Группа", bbox_to_anchor=(1.02, 1), loc="upper left")
    sns.despine(ax=ax)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    validate_input(df)
    print("Input validation: OK")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
