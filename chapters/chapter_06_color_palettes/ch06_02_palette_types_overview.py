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
    uv run python chapters/chapter_06_color_palettes/ch06_02_palette_types_overview.py

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


FIGURE_ID = "ch06_02_palette_types_overview"


def build_figure() -> plt.Figure:
    """
    RU:
        Подраздел 6.2. Тезис: тип палитры должен соответствовать типу данных:
        последовательная — для величины, дивергентная — для отклонений,
        качественная — для категорий.

    EN:
        Subsection 6.2. Thesis: palette type should match data type:
        sequential for magnitude, diverging for deviations, qualitative for categories.
    """
    import numpy as np

    palettes = [
        ("Последовательная / Sequential", "viridis"),
        ("Дивергентная / Diverging", "vlag"),
        ("Качественная / Qualitative", "colorblind"),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(8, 4.8))

    for ax, (title, palette_name) in zip(axes, palettes):
        if palette_name == "colorblind":
            colors = sns.color_palette(palette_name, 8)
            values = np.arange(8).reshape(1, -1)
            ax.imshow(values, aspect="auto", cmap=None)
            for i, color in enumerate(colors):
                ax.add_patch(plt.Rectangle((i - 0.5, -0.5), 1, 1, color=color))
        else:
            values = np.linspace(0, 1, 256).reshape(1, -1)
            ax.imshow(values, aspect="auto", cmap=palette_name)

        ax.set_title(title, loc="left")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    fig.suptitle("Три типа палитр и их назначение", y=1.02)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    fig = build_figure()
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
