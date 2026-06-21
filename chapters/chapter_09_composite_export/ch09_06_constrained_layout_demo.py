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
    uv run python chapters/chapter_09_composite_export/ch09_06_constrained_layout_demo.py

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


FIGURE_ID = "ch09_06_constrained_layout_demo"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 9.6. Тезис: constrained_layout может быть удобнее
        tight_layout для сложных фигур с colorbar и несколькими панелями.

    EN:
        Subsection 9.6. Thesis: constrained_layout can be more convenient than
        tight_layout for complex figures with colorbars and multiple panels.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), constrained_layout=True, sharey=True)

    vmin = df["risk_score"].min()
    vmax = df["risk_score"].max()

    sc = axes[0].scatter(df["bmi_kg_m2"], df["sbp_mm_hg"], c=df["risk_score"], cmap="viridis", vmin=vmin, vmax=vmax, s=25, alpha=0.7)
    axes[0].set_xlabel("ИМТ, кг/м²")
    axes[0].set_ylabel("Систолическое АД, мм рт. ст.")
    axes[0].set_title("A. ИМТ")
    add_panel_label(axes[0], "A")
    sns.despine(ax=axes[0])

    axes[1].scatter(df["glucose_mmol_l"], df["sbp_mm_hg"], c=df["risk_score"], cmap="viridis", vmin=vmin, vmax=vmax, s=25, alpha=0.7)
    axes[1].set_xlabel("Глюкоза, ммоль/л")
    axes[1].set_ylabel("Систолическое АД, мм рт. ст.")
    axes[1].set_title("B. Глюкоза")
    add_panel_label(axes[1], "B")
    sns.despine(ax=axes[1])

    cbar = fig.colorbar(sc, ax=axes)
    cbar.set_label("Сконструированный риск")

    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
