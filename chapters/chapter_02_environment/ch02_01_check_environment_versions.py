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
    uv run python chapters/chapter_02_environment/ch02_01_check_environment_versions.py

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


FIGURE_ID = "ch02_01_environment_versions"


def main() -> None:
    """
    RU:
        Тезис: версии библиотек нужно фиксировать для воспроизводимости.
        Этот файл ничего не рисует, а печатает версии ключевых пакетов.

    EN:
        Thesis: library versions should be recorded for reproducibility.
        This file does not draw a figure; it prints key package versions.
    """
    import sys
    import numpy as np
    import scipy
    import matplotlib
    import seaborn
    import sklearn

    print("Python:      ", sys.version.replace("\n", " "))
    print("numpy:       ", np.__version__)
    print("pandas:      ", pd.__version__)
    print("scipy:       ", scipy.__version__)
    print("matplotlib:  ", matplotlib.__version__)
    print("seaborn:     ", seaborn.__version__)
    print("scikit-learn:", sklearn.__version__)

    try:
        import lifelines
        print("lifelines:   ", lifelines.__version__)
    except ImportError:
        print("lifelines:    not installed")

    try:
        import statannotations
        print("statannotations:", statannotations.__version__)
    except ImportError:
        print("statannotations: not installed")


if __name__ == "__main__":
    main()
