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
    uv run python chapters/chapter_10_reproducibility/ch10_07_logging_pipeline_steps.py

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


FIGURE_ID = "ch10_07_logging_pipeline_steps"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 10.7. Тезис: логирование фиксирует ход выполнения:
        загрузку данных, расчёты, сохранение таблиц и экспорт рисунка.

    EN:
        Subsection 10.7. Thesis: logging records execution flow:
        data loading, calculations, table saving, and figure export.
    """
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    sns.histplot(df, x="sbp_mm_hg", bins=25, ax=ax)
    ax.set_xlabel("Систолическое АД, мм рт. ст.")
    ax.set_ylabel("Частота")
    ax.set_title("Pipeline с логированием")
    sns.despine(ax=ax)
    fig.tight_layout()
    return fig


def main() -> None:
    import logging

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    log_path = REPORT_DIR / "ch10_07_pipeline.log"

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )

    set_scientific_style()
    logging.info("Style configured")

    df = load_dataset("clinical_cross_sectional.csv")
    logging.info("Loaded dataset with %d rows and %d columns", df.shape[0], df.shape[1])

    fig = build_figure(df)
    logging.info("Figure built")

    save_figure(fig, FIGURE_ID)
    logging.info("Figure exported")

    print(f"Saved log: {log_path}")
    plt.show()


if __name__ == "__main__":
    main()
