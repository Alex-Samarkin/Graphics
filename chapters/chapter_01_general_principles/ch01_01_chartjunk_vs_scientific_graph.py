# -*- coding: utf-8 -*-
"""
Chapter 01 standalone figure script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 1.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 1 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run from project root:
    uv run python chapters/chapter_01_general_principles/ch01_01_chartjunk_vs_scientific_graph.py

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
        Задаёт спокойный научный стиль: белый фон, читаемые шрифты,
        отсутствие лишних верхней и правой рамок, палитра colorblind.

    EN:
        Applies a clean scientific style: white background, readable fonts,
        removed top/right spines, and a colorblind-safe palette.
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


def ensure_output_dir() -> None:
    """RU: Создаёт папку figure/. EN: Creates the figure/ directory."""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(fig: plt.Figure, name: str) -> None:
    """
    RU:
        Сохраняет рисунок в форматах, полезных для разных задач:
        PNG — просмотр и презентации, PDF — векторный формат,
        TIFF — растровый формат для журналов.

    EN:
        Saves the figure in formats useful for different contexts:
        PNG for previews/slides, PDF as a vector format,
        TIFF as a journal-friendly raster format.
    """
    ensure_output_dir()
    for ext in ("png", "pdf", "tiff"):
        path = FIGURE_DIR / f"{name}.{ext}"
        fig.savefig(path, dpi=600, bbox_inches="tight", facecolor="white")
        print(f"Saved: {path}")


def load_dataset(filename: str) -> pd.DataFrame:
    """
    RU:
        Загружает синтетический учебный датасет из data/processed/.
        Если файла нет, сначала запустите generate_data.py.

    EN:
        Loads a synthetic teaching dataset from data/processed/.
        If the file is missing, run generate_data.py first.
    """
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Run first: uv run python generate_data.py"
        )
    return pd.read_csv(path, encoding="utf-8-sig")


FIGURE_ID = "ch01_01_chartjunk_vs_scientific_graph"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Тезис: научный график должен передавать данные, а не украшать их.
        Левая панель намеренно перегружена декоративными элементами.
        Правая панель показывает те же данные в чистом академическом виде.

    EN:
        Thesis: a scientific figure should communicate data, not decorate it.
        The left panel is deliberately overloaded with decorative elements.
        The right panel shows the same data in a clean academic form.
    """
    summary = (
        df.groupby("therapy_group", as_index=False)
        .agg(
            mean_sbp=("sbp_mm_hg", "mean"),
            sd_sbp=("sbp_mm_hg", "std"),
            n=("sbp_mm_hg", "size"),
        )
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    # RU: Плохой вариант: псевдоэффекты, тяжёлая сетка, заголовок-крик.
    # EN: Bad version: pseudo-effects, heavy grid, over-emphatic title.
    ax = axes[0]
    bars = ax.bar(
        summary["therapy_group"],
        summary["mean_sbp"],
        yerr=summary["sd_sbp"],
        capsize=5,
        edgecolor="black",
        linewidth=1.5,
        hatch="//",
        alpha=0.75,
    )
    ax.set_title("ЭФФЕКТ ЛЕЧЕНИЯ!!!")
    ax.set_ylabel("АД")
    ax.grid(True, axis="both", linewidth=1.2)
    ax.set_facecolor("#f0f0f0")
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            "★",
            ha="center",
            va="bottom",
            fontsize=18,
        )
    ax.tick_params(axis="x", rotation=20)

    # RU: Хороший вариант: подписи, единицы, SD, минимум лишнего.
    # EN: Good version: labels, units, SD, minimal non-data ink.
    ax = axes[1]
    ax.bar(
        summary["therapy_group"],
        summary["mean_sbp"],
        yerr=summary["sd_sbp"],
        capsize=4,
        edgecolor="black",
        linewidth=0.8,
        alpha=0.85,
    )
    ax.set_title("Среднее систолическое АД по группам")
    ax.set_xlabel("Группа терапии")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.text(
        0.02,
        0.96,
        "Планки погрешностей: SD",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=9,
    )
    sns.despine(ax=ax)
    ax.tick_params(axis="x", rotation=20)

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
