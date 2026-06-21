# -*- coding: utf-8 -*-
"""
Chapter 05 standalone relationships/regression script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 5.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 5 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_05_relationships_regression/ch05_03_ci_vs_prediction_interval.py

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
        Единый академический стиль для графиков связи между переменными.

    EN:
        Unified academic style for relationship and regression plots.
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


FIGURE_ID = "ch05_03_ci_vs_prediction_interval"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 5.3. Тезис: доверительный интервал среднего уже, чем
        интервал предсказания индивидуального наблюдения.

    EN:
        Subsection 5.3. Thesis: the confidence interval for the mean is narrower
        than the prediction interval for an individual observation.
    """
    import numpy as np
    import statsmodels.api as sm

    x = df["bmi_kg_m2"].to_numpy()
    y = df["sbp_mm_hg"].to_numpy()

    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()

    x_grid = np.linspace(x.min(), x.max(), 120)
    X_grid = sm.add_constant(x_grid)
    pred = model.get_prediction(X_grid).summary_frame(alpha=0.05)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(x, y, alpha=0.35, s=22)
    ax.plot(x_grid, pred["mean"], label="Средняя линия регрессии")
    ax.fill_between(x_grid, pred["mean_ci_lower"], pred["mean_ci_upper"], alpha=0.25, label="95% CI среднего")
    ax.fill_between(x_grid, pred["obs_ci_lower"], pred["obs_ci_upper"], alpha=0.12, label="95% интервал предсказания")

    ax.set_xlabel("ИМТ, кг/м²")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.set_title("CI среднего vs интервал предсказания")
    ax.legend()
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
