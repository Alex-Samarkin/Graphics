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
    uv run python chapters/chapter_02_environment/ch02_04_save_figure_formats.py

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


FIGURE_ID = "ch02_04_save_figure_formats"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Тезис: один и тот же рисунок полезно сохранять в нескольких форматах:
        PNG для просмотра, PDF как вектор, TIFF для журналов.

    EN:
        Thesis: the same figure should often be saved in several formats:
        PNG for preview, PDF as vector output, TIFF for journals.
    """
    summary = (
        df.groupby("therapy_group", as_index=False)
        .agg(mean_sbp=("sbp_mm_hg", "mean"), sd_sbp=("sbp_mm_hg", "std"))
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(
        summary["therapy_group"],
        summary["mean_sbp"],
        yerr=summary["sd_sbp"],
        fmt="o",
        capsize=5,
        label="Среднее ± SD",
    )

    ax.set_xlabel("Группа терапии")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.set_title("Один рисунок — несколько форматов экспорта")
    ax.legend()
    sns.despine(ax=ax)

    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
