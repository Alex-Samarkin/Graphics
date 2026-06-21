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
    uv run python chapters/chapter_07_medical_special_plots/ch07_04_consort_flow_basic.py

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


FIGURE_ID = "ch07_04_consort_flow_basic"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 7.4. Тезис: CONSORT-диаграмма показывает поток участников
        через этапы клинического исследования.

    EN:
        Subsection 7.4. Thesis: a CONSORT diagram shows participant flow
        through stages of a clinical trial.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.axis("off")

    boxes = [
        (0.5, 0.92, "Оценены на соответствие\\nn = 820"),
        (0.5, 0.78, "Рандомизированы\\nn = 480"),
        (0.28, 0.62, "Препарат A\\nn = 240"),
        (0.72, 0.62, "Плацебо\\nn = 240"),
        (0.28, 0.45, "Завершили наблюдение\\nn = 218"),
        (0.72, 0.45, "Завершили наблюдение\\nn = 216"),
        (0.28, 0.28, "Включены в анализ\\nn = 236"),
        (0.72, 0.28, "Включены в анализ\\nn = 238"),
    ]

    for x, y, text in boxes:
        ax.text(
            x,
            y,
            text,
            ha="center",
            va="center",
            bbox={"boxstyle": "round,pad=0.45", "fc": "white", "ec": "black"},
            transform=ax.transAxes,
        )

    arrows = [
        ((0.5, 0.88), (0.5, 0.82)),
        ((0.5, 0.74), (0.28, 0.66)),
        ((0.5, 0.74), (0.72, 0.66)),
        ((0.28, 0.58), (0.28, 0.49)),
        ((0.72, 0.58), (0.72, 0.49)),
        ((0.28, 0.41), (0.28, 0.32)),
        ((0.72, 0.41), (0.72, 0.32)),
    ]

    for start, end in arrows:
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            xycoords=ax.transAxes,
            arrowprops={"arrowstyle": "->", "linewidth": 1.2, "color": "blue"},
        )

    ax.text(0.76, 0.84, "Исключены\\nn = 340", transform=ax.transAxes, ha="center",
            bbox={"boxstyle": "round,pad=0.35", "fc": "white", "ec": "0.5"})
    ax.annotate("", xy=(0.66, 0.84), xytext=(0.53, 0.84), xycoords=ax.transAxes,
                arrowprops={"arrowstyle": "->", "linewidth": 1.0, "color": "red"})

    ax.set_title("CONSORT flow diagram", pad=20)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("consort_flow.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
