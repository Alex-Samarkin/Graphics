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
    uv run python chapters/chapter_03_distributions/ch03_04_boxplot_hides_shape.py

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


FIGURE_ID = "ch03_04_boxplot_hides_shape"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 3.4. Тезис: boxplot может скрывать форму распределения.
        Violin plot рядом помогает увидеть асимметрию и различия формы.

    EN:
        Subsection 3.4. Thesis: a boxplot can hide the distribution shape.
        A neighboring violin plot reveals skewness and shape differences.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    order = ["Контроль", "Умеренное воспаление", "Выраженное воспаление"]

    ax = axes[0]
    sns.boxplot(data=df, x="disease_group", y="crp_mg_l", order=order, ax=ax)
    ax.set_yscale("log")
    ax.set_title("Boxplot: компактно, но форма скрыта")
    ax.set_xlabel("Группа")
    ax.set_ylabel("СРБ, мг/л, log scale")
    ax.tick_params(axis="x", rotation=20)
    sns.despine(ax=ax)

    ax = axes[1]
    sns.violinplot(data=df, x="disease_group", y="crp_mg_l", order=order, inner="quartile", cut=0, ax=ax)
    ax.set_yscale("log")
    ax.set_title("Violin: видна форма распределения")
    ax.set_xlabel("Группа")
    ax.set_ylabel("СРБ, мг/л, log scale")
    ax.tick_params(axis="x", rotation=20)
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("lab_values_logscale.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
