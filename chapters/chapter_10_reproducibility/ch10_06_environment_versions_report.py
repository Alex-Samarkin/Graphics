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
    uv run python chapters/chapter_10_reproducibility/ch10_06_environment_versions_report.py

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


FIGURE_ID = "ch10_06_environment_versions_report"


def main() -> None:
    """
    RU:
        Подраздел 10.6. Тезис: версии Python и библиотек нужно сохранять
        как отдельный отчёт, чтобы рисунки можно было воспроизвести позже.

    EN:
        Subsection 10.6. Thesis: Python and library versions should be saved
        as a separate report so figures can be reproduced later.
    """
    import sys
    import numpy as np
    import scipy
    import matplotlib
    import seaborn
    import sklearn

    versions = {
        "python": sys.version.replace("\n", " "),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": scipy.__version__,
        "matplotlib": matplotlib.__version__,
        "seaborn": seaborn.__version__,
        "scikit_learn": sklearn.__version__,
    }

    try:
        import lifelines
        versions["lifelines"] = lifelines.__version__
    except ImportError:
        versions["lifelines"] = "not installed"

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / "ch10_06_environment_versions.csv"
    pd.DataFrame([versions]).to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Saved environment report: {output_path}")
    for key, value in versions.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
