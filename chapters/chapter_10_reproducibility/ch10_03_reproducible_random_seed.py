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
    uv run python chapters/chapter_10_reproducibility/ch10_03_reproducible_random_seed.py

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


FIGURE_ID = "ch10_03_reproducible_random_seed"


def build_figure() -> plt.Figure:
    """
    RU:
        Подраздел 10.3. Тезис: фиксированный seed делает случайную подвыборку
        и рисунок воспроизводимыми.

    EN:
        Subsection 10.3. Thesis: a fixed seed makes random sampling and the
        resulting figure reproducible.
    """
    import numpy as np

    rng_1 = np.random.default_rng(42)
    rng_2 = np.random.default_rng(42)
    rng_3 = np.random.default_rng(2026)

    x = range(1, 41)
    y1 = rng_1.normal(0, 1, 40).cumsum()
    y2 = rng_2.normal(0, 1, 40).cumsum()
    y3 = rng_3.normal(0, 1, 40).cumsum()

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(x, y1, label="seed = 42, запуск 1")
    ax.plot(x, y2, linestyle="--", label="seed = 42, запуск 2")
    ax.plot(x, y3, linestyle=":", label="seed = 2026")

    ax.set_xlabel("Номер наблюдения")
    ax.set_ylabel("Кумулятивное значение")
    ax.set_title("Одинаковый seed → одинаковый результат")
    ax.legend()
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    fig = build_figure()
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
