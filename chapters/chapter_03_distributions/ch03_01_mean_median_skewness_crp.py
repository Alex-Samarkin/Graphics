# -*- coding: utf-8 -*-
"""
Chapter 03 standalone distribution-plot script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 3.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 3 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_03_distributions/ch03_01_mean_median_skewness_crp.py

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
        Задаёт единый академический стиль для графиков распределений.

    EN:
        Applies a unified academic style for distribution plots.
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


FIGURE_ID = "ch03_01_mean_median_skewness_crp"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 3.1. Тезис: у асимметричных лабораторных показателей
        среднее может заметно отличаться от медианы, поэтому распределение
        нужно визуализировать до выбора статистической сводки.

    EN:
        Subsection 3.1. Thesis: for skewed laboratory variables, the mean
        can differ substantially from the median, so the distribution should
        be visualized before choosing a summary statistic.
    """
    fig, ax = plt.subplots(figsize=(7, 4.2))

    sns.histplot(df, x="crp_mg_l", bins=35, kde=True, ax=ax)
    mean_value = df["crp_mg_l"].mean()
    median_value = df["crp_mg_l"].median()

    ax.axvline(mean_value, linestyle="--", linewidth=2, label=f"Среднее = {mean_value:.1f}")
    ax.axvline(median_value, linestyle="-", linewidth=2, label=f"Медиана = {median_value:.1f}")

    ax.set_xlabel("С-реактивный белок, мг/л")
    ax.set_ylabel("Частота")
    ax.set_title("Асимметрия распределения: среднее ≠ медиана")
    ax.legend()
    sns.despine(ax=ax)

    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    print("CRP mean:", round(df["crp_mg_l"].mean(), 2))
    print("CRP median:", round(df["crp_mg_l"].median(), 2))
    print("CRP mode approx:", df["crp_mg_l"].round().mode().iloc[0])
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
