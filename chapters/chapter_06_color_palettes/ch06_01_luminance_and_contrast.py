# -*- coding: utf-8 -*-
"""
Chapter 06 standalone color/palette script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 6.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 6 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_06_color_palettes/ch06_01_luminance_and_contrast.py

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
        Единый академический стиль для иллюстраций по цвету.

    EN:
        Unified academic style for color-related figures.
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


FIGURE_ID = "ch06_01_luminance_and_contrast"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 6.1. Тезис: читаемость графика зависит не только от оттенка,
        но и от светлоты/контраста. Слабый контраст ухудшает восприятие.

    EN:
        Subsection 6.1. Thesis: readability depends not only on hue but also
        on luminance and contrast. Weak contrast impairs perception.
    """
    summary = (
        df.groupby("therapy_group", as_index=False)
        .agg(mean_sbp=("sbp_mm_hg", "mean"))
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    ax = axes[0]
    ax.bar(summary["therapy_group"], summary["mean_sbp"], color=["#d9d9d9", "#cfcfcf", "#c4c4c4"], edgecolor="#bdbdbd")
    ax.set_title("Плохо: слабый контраст")
    ax.set_xlabel("Группа терапии")
    ax.set_ylabel("Среднее систолическое АД, мм рт. ст.")
    ax.tick_params(axis="x", rotation=20)
    sns.despine(ax=ax)

    ax = axes[1]
    ax.bar(
        summary["therapy_group"],
        summary["mean_sbp"],
        # здесь разные оттенки одного цвета
        # color=["#aec6cf", "#7fa8c2", "#4e7ba8"],
        # здесь один цвет, но с разной прозрачностью
        color=["#4e7ba8aa", "#4e7ba8cc", "#4e7ba8ff"],
        edgecolor="black",
        linewidth=0.8,
    )
    ax.set_title("Лучше: различимый контраст")
    ax.set_xlabel("Группа терапии")
    ax.set_ylabel("Среднее систолическое АД, мм рт. ст.")
    ax.tick_params(axis="x", rotation=20)
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
