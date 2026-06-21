# -*- coding: utf-8 -*-
"""
Chapter 07 standalone specialized medical plot script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 7.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 7 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_07_medical_special_plots/ch07_06_decision_curve_analysis_simple.py

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
        Единый академический стиль для специализированных медицинских графиков.

    EN:
        Unified academic style for specialized medical plots.
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


FIGURE_ID = "ch07_06_decision_curve_analysis_simple"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 7.6. Тезис: decision curve analysis иллюстрирует
        клиническую полезность модели при разных порогах вмешательства.

    EN:
        Subsection 7.6. Thesis: decision curve analysis illustrates clinical
        usefulness of a model across intervention thresholds.
    """
    import numpy as np

    y = df["disease_status"].to_numpy()
    p = df["predicted_probability"].to_numpy()
    n = len(y)

    thresholds = np.linspace(0.05, 0.95, 100)
    net_model = []
    net_all = []
    prevalence = y.mean()

    for pt in thresholds:
        predicted_positive = p >= pt
        tp = ((predicted_positive == 1) & (y == 1)).sum()
        fp = ((predicted_positive == 1) & (y == 0)).sum()
        net_benefit = tp / n - fp / n * (pt / (1 - pt))
        net_model.append(net_benefit)

        net_all.append(prevalence - (1 - prevalence) * (pt / (1 - pt)))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(thresholds, net_model, label="Модель")
    ax.plot(thresholds, net_all, linestyle="--", label="Лечить всех")
    ax.axhline(0, linestyle=":", color="0.4", label="Лечить никого")

    ax.set_xlabel("Пороговая вероятность")
    ax.set_ylabel("Net benefit")
    ax.set_title("Decision curve analysis, учебный пример")
    ax.legend()
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("diagnostic_roc.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
