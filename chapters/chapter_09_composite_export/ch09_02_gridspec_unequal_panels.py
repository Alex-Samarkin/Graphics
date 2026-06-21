# -*- coding: utf-8 -*-
"""
Chapter 09 standalone composite/export script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 9.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 9 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_09_composite_export/ch09_02_gridspec_unequal_panels.py

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
        Единый академический стиль для составных рисунков и экспорта.

    EN:
        Unified academic style for composite figures and export.
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


def add_panel_label(ax: plt.Axes, label: str) -> None:
    """
    RU:
        Добавляет буквенную метку панели.

    EN:
        Adds a panel letter.
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


FIGURE_ID = "ch09_02_gridspec_unequal_panels"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 9.2. Тезис: GridSpec позволяет делать неравные панели:
        например, большую основную панель и две вспомогательные.

    EN:
        Subsection 9.2. Thesis: GridSpec allows unequal panels, such as one
        large main panel and two supporting panels.
    """
    import matplotlib.gridspec as gridspec

    fig = plt.figure(figsize=(10, 6.5))
    gs = gridspec.GridSpec(2, 2, width_ratios=[2.2, 1], height_ratios=[1, 1])

    ax_main = fig.add_subplot(gs[:, 0])
    ax_top = fig.add_subplot(gs[0, 1])
    ax_bottom = fig.add_subplot(gs[1, 1])

    sns.scatterplot(data=df, x="bmi_kg_m2", y="sbp_mm_hg", hue="therapy_group", alpha=0.65, ax=ax_main)
    ax_main.set_xlabel("ИМТ, кг/м²")
    ax_main.set_ylabel("Систолическое АД, мм рт. ст.")
    ax_main.set_title("Основная панель: связь ИМТ и АД")
    ax_main.legend(title="Группа", loc="best")
    add_panel_label(ax_main, "A")
    sns.despine(ax=ax_main)

    sns.histplot(data=df, x="bmi_kg_m2", bins=20, ax=ax_top)
    ax_top.set_xlabel("ИМТ, кг/м²")
    ax_top.set_ylabel("Частота")
    ax_top.set_title("Распределение ИМТ")
    add_panel_label(ax_top, "B")
    sns.despine(ax=ax_top)

    sns.histplot(data=df, x="sbp_mm_hg", bins=20, ax=ax_bottom)
    ax_bottom.set_xlabel("АД, мм рт. ст.")
    ax_bottom.set_ylabel("Частота")
    ax_bottom.set_title("Распределение АД")
    add_panel_label(ax_bottom, "C")
    sns.despine(ax=ax_bottom)

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
