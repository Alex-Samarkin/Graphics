# -*- coding: utf-8 -*-
"""
Chapter 04 standalone categorical-comparison script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 4.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 4 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_04_category_comparison/ch04_03_normalized_100_percent_bar.py

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
        Единый академический стиль для сравнения категорий.

    EN:
        Unified academic style for categorical comparisons.
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


FIGURE_ID = "ch04_03_normalized_100_percent_bar"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 4.3. Тезис: нормированные 100% столбцы подходят для
        сравнения структуры, но скрывают абсолютные размеры групп.

    EN:
        Subsection 4.3. Thesis: normalized 100% bars are suitable for comparing
        composition, but hide absolute group sizes.
    """
    pivot = df.pivot(index="department", columns="severity", values="percent")
    severity_order = ["Лёгкая", "Средняя", "Тяжёлая"]
    pivot = pivot[severity_order]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bottom = None

    for severity in severity_order:
        ax.bar(
            pivot.index,
            pivot[severity],
            bottom=bottom,
            label=severity,
            edgecolor="black",
            linewidth=0.6,
        )
        bottom = pivot[severity] if bottom is None else bottom + pivot[severity]

    ax.set_ylim(0, 100)
    ax.set_xlabel("Отделение")
    ax.set_ylabel("Доля пациентов, %")
    ax.set_title("Нормированная 100% столбчатая диаграмма")
    ax.legend(title="Тяжесть состояния", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.tick_params(axis="x", rotation=20)
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("categorical_composition.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
