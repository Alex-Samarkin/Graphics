# -*- coding: utf-8 -*-
"""
Chapter 02 standalone figure/environment script.

RU:
    Один файл = одна иллюстрация одного практического тезиса главы 2.
    Скрипт рассчитан на запуск из корня проекта.

EN:
    One file = one illustration of one practical Chapter 2 thesis.
    The script is intended to be run from the project root.

Run:
    uv run python chapters/chapter_02_environment/ch02_06_dataset_preview_clinical.py

Expected before running figure examples:
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
        Единый научный стиль для рисунков главы:
        белый фон, читаемые шрифты, colorblind-safe палитра,
        сохранение с высоким DPI.

    EN:
        Unified scientific style for chapter figures:
        white background, readable fonts, colorblind-safe palette,
        high-DPI export.
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


FIGURE_ID = "ch02_06_dataset_preview_clinical"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Тезис: перед построением графиков данные нужно осмотреть:
        диапазоны, выбросы, группы и базовые распределения.

    EN:
        Thesis: before plotting, data should be inspected:
        ranges, outliers, groups, and basic distributions.
    """
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))

    sns.histplot(df, x="age_years", bins=20, ax=axes[0])
    axes[0].set_title("Возраст")
    axes[0].set_xlabel("Возраст, годы")
    axes[0].set_ylabel("Частота")

    sns.histplot(df, x="bmi_kg_m2", bins=20, ax=axes[1])
    axes[1].set_title("ИМТ")
    axes[1].set_xlabel("ИМТ, кг/м²")
    axes[1].set_ylabel("Частота")

    sns.countplot(data=df, x="therapy_group", ax=axes[2])
    axes[2].set_title("Группы терапии")
    axes[2].set_xlabel("Группа")
    axes[2].set_ylabel("n")
    axes[2].tick_params(axis="x", rotation=20)

    for ax in axes:
        sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    print(df.head())
    print()
    print(df.describe(include='number').round(2))

    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
