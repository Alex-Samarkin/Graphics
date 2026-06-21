# -*- coding: utf-8 -*-
"""
Chapter 07 standalone specialized medical plot script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 7.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 7 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_07_medical_special_plots/ch07_05_bland_altman_medical_agreement.py

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
        Единый академический стиль для специализированных медицинских графиков.

    EN:
        Unified academic style for specialized medical plots.
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


FIGURE_ID = "ch07_05_bland_altman_medical_agreement"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 7.5. Тезис: для сравнения методов измерения корреляции
        недостаточно; нужен анализ согласия, например Bland–Altman.

    EN:
        Subsection 7.5. Thesis: correlation is not enough to compare measurement
        methods; agreement analysis such as Bland-Altman is needed.
    """
    from scipy import stats
    import numpy as np

    x = df["manual_sbp_mm_hg"]
    y = df["automated_sbp_mm_hg"]
    mean_x = df["mean_sbp_mm_hg"]
    diff = df["difference_auto_minus_manual_mm_hg"]

    bias = diff.mean()
    sd = diff.std(ddof=1)
    loa_low = bias - 1.96 * sd
    loa_high = bias + 1.96 * sd
    r, _ = stats.pearsonr(x, y)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    ax = axes[0]
    ax.scatter(x, y, alpha=0.7)
    ax.set_xlabel("Ручной метод, мм рт. ст.")
    ax.set_ylabel("Автоматический метод, мм рт. ст.")
    ax.set_title(f"Корреляция методов: r = {r:.2f}")
    sns.despine(ax=ax)

    ax = axes[1]
    ax.scatter(mean_x, diff, alpha=0.7)
    ax.axhline(bias, linestyle="-", label=f"Bias = {bias:.1f}")
    ax.axhline(loa_low, linestyle="--", label=f"Lower LoA = {loa_low:.1f}")
    ax.axhline(loa_high, linestyle="--", label=f"Upper LoA = {loa_high:.1f}")
    ax.set_xlabel("Среднее двух методов, мм рт. ст.")
    ax.set_ylabel("Автоматический − ручной, мм рт. ст.")
    ax.set_title("Согласие методов: Bland–Altman")
    ax.legend()
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("bland_altman_agreement.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
