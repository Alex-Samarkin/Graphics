# -*- coding: utf-8 -*-
"""
Chapter 10 standalone reproducibility script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 10.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 10 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_10_reproducibility/ch10_04_parameterized_script_cli.py

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
REPORT_DIR = PROJECT_ROOT / "report"


def set_scientific_style() -> None:
    """
    RU:
        Единый академический стиль для воспроизводимых рисунков.

    EN:
        Unified academic style for reproducible figures.
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


FIGURE_ID = "ch10_04_parameterized_script_cli"


def parse_args():
    """
    RU:
        Аргументы командной строки позволяют менять параметры без правки кода.

    EN:
        Command-line arguments allow changing parameters without editing code.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Parameterized figure example.")
    parser.add_argument("--group", default="Препарат A", help="Therapy group to plot.")
    parser.add_argument("--bins", type=int, default=20, help="Number of histogram bins.")
    parser.add_argument("--output-name", default=FIGURE_ID, help="Output figure name.")
    return parser.parse_args()


def build_figure(df: pd.DataFrame, group: str, bins: int) -> plt.Figure:
    """
    RU:
        Подраздел 10.4. Тезис: параметры анализа должны быть явными:
        группа, число бинов, имя файла и т.д.

    EN:
        Subsection 10.4. Thesis: analysis parameters should be explicit:
        group, number of bins, output filename, etc.
    """
    part = df[df["therapy_group"] == group]
    if part.empty:
        raise ValueError(f"Unknown group: {group}")

    fig, ax = plt.subplots(figsize=(6.5, 4))
    sns.histplot(part, x="sbp_mm_hg", bins=bins, ax=ax)

    ax.set_xlabel("Систолическое АД, мм рт. ст.")
    ax.set_ylabel("Частота")
    ax.set_title(f"Распределение АД: {group}, bins={bins}")
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    args = parse_args()
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df, group=args.group, bins=args.bins)
    save_figure(fig, args.output_name)
    plt.show()


if __name__ == "__main__":
    main()
