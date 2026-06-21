# -*- coding: utf-8 -*-
"""
Chapter 04 standalone categorical-comparison script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 4.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 4 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_04_category_comparison/ch04_05_pie_chart_problem.py

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


def set_scientific_style() -> None:
    """
    RU:
        Единый академический стиль для сравнения категорий.

    EN:
        Unified academic style for categorical comparisons.
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


def save_figure(fig: plt.Figure, name: str) -> None:
    """
    RU:
        Сохраняет рисунок в PNG, PDF и TIFF в папку figure/.

    EN:
        Saves the figure as PNG, PDF and TIFF into the figure/ folder.
    """
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf", "tiff"):
        path = FIGURE_DIR / f"{name}.{ext}"
        fig.savefig(path, dpi=600, bbox_inches="tight", facecolor="white")
        print(f"Saved: {path}")


FIGURE_ID = "ch04_05_pie_chart_problem"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 4.5. Тезис: круговые диаграммы плохо подходят для точного
        сравнения близких долей, особенно при нескольких категориях.

    EN:
        Subsection 4.5. Thesis: pie charts are poor for precise comparison
        of similar proportions, especially with several categories.
    """
    part = df[df["department"] == "Кардиология"].copy()

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(
        part["n"],
        labels=part["severity"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.set_title("Круговая диаграмма: сравнивать доли трудно")
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("categorical_composition.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
