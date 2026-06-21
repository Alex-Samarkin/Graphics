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
    uv run python chapters/chapter_07_medical_special_plots/ch07_08_special_plots_summary_panel.py

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


FIGURE_ID = "ch07_08_special_plots_summary_panel"


def build_figure() -> plt.Figure:
    """
    RU:
        Подраздел 7.8. Тезис: специализированные медицинские графики отвечают
        на разные клинические вопросы: диагностика, прогноз, выживаемость,
        мета-анализ и поток участников.

    EN:
        Subsection 7.8. Thesis: specialized medical plots answer different
        clinical questions: diagnosis, prognosis, survival, meta-analysis,
        and participant flow.
    """
    from sklearn.metrics import roc_curve, auc
    from lifelines import KaplanMeierFitter
    import numpy as np

    roc_df = load_dataset("diagnostic_roc.csv")
    surv_df = load_dataset("survival_kaplan_meier.csv")
    forest_df = load_dataset("forest_meta_analysis.csv")

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    # ROC
    ax = axes[0, 0]
    fpr, tpr, _ = roc_curve(roc_df["disease_status"], roc_df["predicted_probability"])
    ax.plot(fpr, tpr, label=f"AUC = {auc(fpr, tpr):.2f}")
    ax.plot([0, 1], [0, 1], linestyle="--", color="0.5")
    ax.set_title("A. ROC")
    ax.set_xlabel("1 − специфичность")
    ax.set_ylabel("Чувствительность")
    ax.legend()
    sns.despine(ax=ax)

    # KM
    ax = axes[0, 1]
    for group, part in surv_df.groupby("therapy_group"):
        kmf = KaplanMeierFitter()
        kmf.fit(part["time_months"], part["event"], label=group)
        kmf.plot_survival_function(ax=ax, ci_show=False)
    ax.set_title("B. Kaplan–Meier")
    ax.set_xlabel("Месяцы")
    ax.set_ylabel("Без события")
    sns.despine(ax=ax)

    # Forest
    ax = axes[1, 0]
    plot_df = forest_df.head(6).sort_values("risk_ratio")
    y = np.arange(len(plot_df))
    ax.errorbar(
        plot_df["risk_ratio"],
        y,
        xerr=[plot_df["risk_ratio"] - plot_df["ci_low"], plot_df["ci_high"] - plot_df["risk_ratio"]],
        fmt="o",
        capsize=3,
    )
    ax.axvline(1, linestyle="--", color="0.5")
    ax.set_yticks(y)
    ax.set_yticklabels(plot_df["study"])
    ax.set_xscale("log")
    ax.set_title("C. Forest plot")
    ax.set_xlabel("Risk ratio")
    sns.despine(ax=ax, left=True)

    # Calibration
    ax = axes[1, 1]
    from sklearn.calibration import calibration_curve
    prob_true, prob_pred = calibration_curve(roc_df["disease_status"], roc_df["predicted_probability"], n_bins=8, strategy="quantile")
    ax.plot(prob_pred, prob_true, marker="o")
    ax.plot([0, 1], [0, 1], linestyle="--", color="0.5")
    ax.set_title("D. Calibration")
    ax.set_xlabel("Предсказанная вероятность")
    ax.set_ylabel("Наблюдаемая частота")
    sns.despine(ax=ax)

    fig.suptitle("Специализированные медицинские графики: что они показывают", y=1.02)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    fig = build_figure()
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
