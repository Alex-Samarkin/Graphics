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
    uv run python chapters/chapter_02_environment/ch02_07_reproducible_seed_demo.py

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


FIGURE_ID = "ch02_07_reproducible_seed_demo"


def build_figure() -> plt.Figure:
    """
    RU:
        Тезис: фиксированный seed делает случайные примеры воспроизводимыми.
        Это демонстрационный мини-набор, он не записывает данные в data/.

    EN:
        Thesis: a fixed seed makes random examples reproducible.
        This is a small demonstration dataset; it does not write data to data/.
    """
    import numpy as np

    rng_a = np.random.default_rng(42)
    rng_b = np.random.default_rng(42)
    rng_c = np.random.default_rng(2025)

    x = range(1, 31)
    y_a = rng_a.normal(0, 1, 30).cumsum()
    y_b = rng_b.normal(0, 1, 30).cumsum()
    y_c = rng_c.normal(0, 1, 30).cumsum()

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, y_a, marker="o", label="seed = 42, запуск A")
    ax.plot(x, y_b, linestyle="--", label="seed = 42, запуск B")
    ax.plot(x, y_c, marker="s", linestyle=":", label="seed = 2025")

    ax.set_xlabel("Номер наблюдения")
    ax.set_ylabel("Кумулятивное случайное значение")
    ax.set_title("Одинаковый seed воспроизводит ту же последовательность")
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
