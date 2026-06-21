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
    uv run python chapters/chapter_10_reproducibility/ch10_06_metadata_sidecar_json.py

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


FIGURE_ID = "ch10_06_metadata_sidecar_json"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 10.6. Тезис: рядом с рисунком полезно сохранять metadata:
        входной файл, переменные, seed, версии и параметры экспорта.

    EN:
        Subsection 10.6. Thesis: figure metadata should be saved alongside
        the image: input file, variables, seed, versions, and export parameters.
    """
    fig, ax = plt.subplots(figsize=(6.5, 4.2))

    sns.regplot(
        data=df,
        x="bmi_kg_m2",
        y="sbp_mm_hg",
        ci=95,
        scatter_kws={"alpha": 0.45, "s": 24},
        ax=ax,
    )
    ax.set_xlabel("ИМТ, кг/м²")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.set_title("Рисунок с sidecar metadata JSON")
    sns.despine(ax=ax)
    fig.tight_layout()
    return fig


def save_metadata(name: str) -> None:
    """
    RU:
        Сохраняет JSON с описанием рисунка.

    EN:
        Saves JSON describing the figure.
    """
    import json
    import sys
    import numpy as np
    import matplotlib
    import seaborn

    metadata = {
        "figure_id": name,
        "input_dataset": "clinical_cross_sectional.csv",
        "x": "bmi_kg_m2",
        "y": "sbp_mm_hg",
        "seed": None,
        "python": sys.version,
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "matplotlib": matplotlib.__version__,
        "seaborn": seaborn.__version__,
        "export_formats": ["png", "pdf", "tiff"],
    }

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DIR / f"{name}.metadata.json"
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved metadata: {path}")


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    save_metadata(FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
