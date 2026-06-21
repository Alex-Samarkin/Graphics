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
    uv run python chapters/chapter_07_medical_special_plots/ch07_01_roc_threshold_annotations.py

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


FIGURE_ID = "ch07_01_roc_threshold_annotations"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 7.1. Тезис: клинический выбор порога — это не только AUC,
        но и баланс чувствительности и специфичности.

    EN:
        Subsection 7.1. Thesis: clinical threshold selection is not only AUC,
        but a balance between sensitivity and specificity.
    """
    from sklearn.metrics import roc_curve, auc
    import numpy as np

    y_true = df["disease_status"]
    y_score = df["predicted_probability"]

    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    youden_index = tpr - fpr
    best_idx = int(np.argmax(youden_index))

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--", color="0.5")

    ax.scatter(fpr[best_idx], tpr[best_idx], s=70, zorder=3)
    ax.annotate(
        f"Порог ≈ {thresholds[best_idx]:.2f}\\nSensitivity = {tpr[best_idx]:.2f}\\nSpecificity = {1 - fpr[best_idx]:.2f}",
        xy=(fpr[best_idx], tpr[best_idx]),
        xytext=(fpr[best_idx] + 0.08, tpr[best_idx] - 0.18),
        arrowprops={"arrowstyle": "->"},
    )

    ax.set_xlabel("1 − специфичность")
    ax.set_ylabel("Чувствительность")
    ax.set_title("ROC-кривая и пример выбора порога")
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="lower right")
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
