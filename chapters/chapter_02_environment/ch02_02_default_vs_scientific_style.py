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
    uv run python chapters/chapter_02_environment/ch02_02_default_vs_scientific_style.py

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


FIGURE_ID = "ch02_02_default_vs_scientific_style"


def build_figure() -> plt.Figure:
    """
    RU:
        Тезис: стиль по умолчанию часто недостаточен для научной работы.
        Скрипт сравнивает быстрый черновой график и настроенный научный стиль.

    EN:
        Thesis: the default style is often insufficient for scientific work.
        The script compares a quick draft plot with a configured scientific style.
    """
    import numpy as np

    x = np.linspace(0, 12, 100)
    y = 145 - 16 * (1 - np.exp(-x / 3.2))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    # RU: Намеренно простой вариант без научных подписей.
    # EN: Intentionally simple version without scientific labeling.
    ax = axes[0]
    ax.plot(x, y)
    ax.set_title("Было: стиль по умолчанию")
    ax.set_xlabel("time")
    ax.set_ylabel("value")

    # RU: Настроенный вариант с осмысленными подписями.
    # EN: Configured version with meaningful labels.
    ax = axes[1]
    ax.plot(x, y)
    ax.set_title("Стало: научный стиль")
    ax.set_xlabel("Время терапии, нед.")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
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
