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
    uv run python chapters/chapter_09_composite_export/ch09_05_transparent_background_export.py

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


FIGURE_ID = "ch09_05_transparent_background_export"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 9.5. Тезис: прозрачный фон полезен для слайдов, но
        для статей чаще нужен белый фон и стабильное воспроизведение.

    EN:
        Subsection 9.5. Thesis: transparent background is useful for slides,
        while articles often require white background and stable reproduction.
    """
    fig, ax = plt.subplots(figsize=(6.5, 4.2))

    summary = df.groupby("therapy_group", as_index=False).agg(mean_sbp=("sbp_mm_hg", "mean"))
    ax.bar(summary["therapy_group"], summary["mean_sbp"], edgecolor="black", alpha=0.85)
    ax.set_xlabel("Группа терапии")
    ax.set_ylabel("Среднее систолическое АД, мм рт. ст.")
    ax.set_title("Экспорт с прозрачным фоном")
    ax.tick_params(axis="x", rotation=20)
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def save_transparent(fig: plt.Figure, name: str) -> None:
    """
    RU:
        Сохраняет отдельную PNG-версию с прозрачным фоном.

    EN:
        Saves a separate PNG version with transparent background.
    """
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    white_path = FIGURE_DIR / f"{name}_white.png"
    transparent_path = FIGURE_DIR / f"{name}_transparent.png"
    fig.savefig(white_path, dpi=600, bbox_inches="tight", facecolor="white")
    fig.savefig(transparent_path, dpi=600, bbox_inches="tight", transparent=True)
    print(f"Saved: {white_path}")
    print(f"Saved: {transparent_path}")


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    save_transparent(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
