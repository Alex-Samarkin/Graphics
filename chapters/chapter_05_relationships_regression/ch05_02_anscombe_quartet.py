# -*- coding: utf-8 -*-
"""
Chapter 05 standalone relationships/regression script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 5.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 5 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_05_relationships_regression/ch05_02_anscombe_quartet.py

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
        Единый академический стиль для графиков связи между переменными.

    EN:
        Unified academic style for relationship and regression plots.
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


FIGURE_ID = "ch05_02_anscombe_quartet"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 5.2. Тезис: одинаковые сводные статистики могут скрывать
        радикально разные структуры данных. Поэтому корреляцию нужно рисовать.

    EN:
        Subsection 5.2. Thesis: identical summary statistics can hide radically
        different data structures. Correlations should therefore be plotted.
    """
    from scipy import stats

    fig, axes = plt.subplots(2, 2, figsize=(8, 7), sharex=True, sharey=True)
    axes = axes.ravel()

    for ax, (name, part) in zip(axes, df.groupby("dataset", sort=True)):
        sns.regplot(data=part, x="x", y="y", ci=None, ax=ax, scatter_kws={"s": 35})
        r, _ = stats.pearsonr(part["x"], part["y"])
        ax.set_title(f"{name}: r = {r:.2f}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        sns.despine(ax=ax)

    fig.suptitle("Квартет Энскомба: сводная статистика не заменяет график", y=1.02)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("anscombe_quartet.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
