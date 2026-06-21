# -*- coding: utf-8 -*-
"""
Chapter 12 standalone checklist/template script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 12.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/ или report/.

EN:
    One file = one illustration of one Chapter 12 thesis.
    The script reads data from data/processed/ and saves output to figure/ or report/.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
FIGURE_DIR = PROJECT_ROOT / "figure"
REPORT_DIR = PROJECT_ROOT / "report"
TEMPLATE_DIR = PROJECT_ROOT / "templates"


def set_scientific_style() -> None:
    """
    RU:
        Единый академический стиль для чек-листов и шаблонов.

    EN:
        Unified academic style for checklists and templates.
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


def save_table(df: pd.DataFrame, filename: str) -> Path:
    """
    RU:
        Сохраняет таблицу в report/.

    EN:
        Saves a table into report/.
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / filename
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Saved: {path}")
    return path

FIGURE_ID = "ch12_01_checklist_from_dataset"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 12.1. Тезис: чек-лист можно хранить как данные
        и визуализировать состояние готовности рисунка.

    EN:
        Subsection 12.1. Thesis: a checklist can be stored as data and used
        to visualize figure-readiness status.
    """
    status_map = {"нет": 0, "частично": 0.5, "да": 1}
    plot_df = df.copy()
    # Determine which column to use as the criterion/label
    if "criterion" in plot_df.columns:
        label_col = "criterion"
    elif "check_description" in plot_df.columns:
        label_col = "check_description"
    elif "check_id" in plot_df.columns:
        label_col = "check_id"
    else:
        # Fall back to the first column
        label_col = plot_df.columns[0]

    plot_df["score"] = plot_df.get("status", pd.Series(["частично"] * len(plot_df))).map(status_map).fillna(0.5)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(plot_df[label_col], plot_df["score"], edgecolor="black")
    ax.set_xlim(0, 1)
    ax.set_xlabel("Готовность: 0 = нет, 1 = да")
    ax.set_ylabel("Критерий")
    ax.set_title("Визуализация чек-листа качества")
    sns.despine(ax=ax)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("figure_quality_checklist.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
