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
    uv run python chapters/chapter_05_relationships_regression/ch05_05_bland_altman_proportional_bias.py

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


FIGURE_ID = "ch05_05_bland_altman_proportional_bias"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 5.5. Тезис: на графике Бланда–Альтмана можно увидеть
        пропорциональное смещение, когда ошибка зависит от уровня измерения.

    EN:
        Subsection 5.5. Thesis: a Bland-Altman plot can reveal proportional
        bias when measurement error depends on the measurement level.
    """
    from scipy import stats

    mean_x = df["mean_sbp_mm_hg"]
    diff = df["difference_auto_minus_manual_mm_hg"]

    slope, intercept, r, p, _ = stats.linregress(mean_x, diff)
    y_hat = intercept + slope * mean_x

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(mean_x, diff, alpha=0.7, s=28)
    ax.plot(mean_x, y_hat, linestyle="--", label=f"Тренд: slope = {slope:.2f}, p = {p:.3g}")
    ax.axhline(diff.mean(), linestyle="-", label=f"Среднее смещение = {diff.mean():.1f}")

    ax.set_xlabel("Среднее двух измерений, мм рт. ст.")
    ax.set_ylabel("Автоматический − ручной метод, мм рт. ст.")
    ax.set_title("Бланд–Альтман: проверка пропорционального смещения")
    ax.legend()
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("bland_altman_agreement.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
