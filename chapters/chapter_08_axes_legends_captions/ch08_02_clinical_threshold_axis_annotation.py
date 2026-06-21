# -*- coding: utf-8 -*-
"""
Chapter 08 standalone axes/legends/captions script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 8.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 8 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_08_axes_legends_captions/ch08_02_clinical_threshold_axis_annotation.py

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
        Единый академический стиль для оформления осей, легенд и подписей.

    EN:
        Unified academic style for axes, legends, and captions.
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


FIGURE_ID = "ch08_02_clinical_threshold_axis_annotation"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 8.2. Тезис: клинические пороги на оси должны быть явно
        подписаны, иначе читатель не поймёт медицинский смысл масштаба.

    EN:
        Subsection 8.2. Thesis: clinical thresholds on an axis should be
        explicitly labeled, otherwise readers miss their medical meaning.
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    sns.scatterplot(data=df, x="age_years", y="ldl_mmol_l", hue="statin_therapy", alpha=0.7, ax=ax)
    ax.axhline(3.0, linestyle="--", color="black", label="LDL 3.0 ммоль/л")
    ax.text(df["age_years"].min(), 3.08, "Клинический ориентир LDL = 3.0 ммоль/л", va="bottom")

    ax.set_xlabel("Возраст, годы")
    ax.set_ylabel("LDL-холестерин, ммоль/л")
    ax.set_title("Ось и клинический порог должны работать вместе")
    ax.legend(title="Статины", bbox_to_anchor=(1.02, 1), loc="upper left")
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
