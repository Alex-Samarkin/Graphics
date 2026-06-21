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
    uv run python chapters/chapter_08_axes_legends_captions/ch08_06_panel_labels.py

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


FIGURE_ID = "ch08_06_panel_labels"


def add_panel_label(ax: plt.Axes, label: str) -> None:
    """
    RU: Добавляет буквенную метку панели в левый верхний угол.
    EN: Adds a panel letter to the upper-left corner.
    """
    ax.text(
        -0.12,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="left",
    )


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 8.6. Тезис: многопанельные рисунки должны иметь
        согласованные буквенные метки A, B, C, D.

    EN:
        Subsection 8.6. Thesis: multi-panel figures should have consistent
        panel labels A, B, C, D.
    """
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))

    ax = axes[0, 0]
    sns.histplot(data=df, x="age_years", bins=20, ax=ax)
    ax.set_xlabel("Возраст, годы")
    ax.set_ylabel("Частота")
    ax.set_title("Возраст")
    add_panel_label(ax, "A")
    sns.despine(ax=ax)

    ax = axes[0, 1]
    sns.histplot(data=df, x="bmi_kg_m2", bins=20, ax=ax)
    ax.set_xlabel("ИМТ, кг/м²")
    ax.set_ylabel("Частота")
    ax.set_title("ИМТ")
    add_panel_label(ax, "B")
    sns.despine(ax=ax)

    ax = axes[1, 0]
    sns.boxplot(data=df, x="therapy_group", y="sbp_mm_hg", ax=ax)
    ax.set_xlabel("Группа")
    ax.set_ylabel("АД, мм рт. ст.")
    ax.set_title("АД по группам")
    ax.tick_params(axis="x", rotation=20)
    add_panel_label(ax, "C")
    sns.despine(ax=ax)

    ax = axes[1, 1]
    sns.scatterplot(data=df, x="bmi_kg_m2", y="glucose_mmol_l", alpha=0.6, ax=ax)
    ax.set_xlabel("ИМТ, кг/м²")
    ax.set_ylabel("Глюкоза, ммоль/л")
    ax.set_title("ИМТ и глюкоза")
    add_panel_label(ax, "D")
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
