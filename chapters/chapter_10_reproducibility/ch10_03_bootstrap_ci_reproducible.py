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
    uv run python chapters/chapter_10_reproducibility/ch10_03_bootstrap_ci_reproducible.py

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


FIGURE_ID = "ch10_03_bootstrap_ci_reproducible"


def bootstrap_mean_ci(values, n_boot: int = 2000, seed: int = 42) -> tuple[float, float, float]:
    """
    RU:
        Воспроизводимый bootstrap: seed задаётся явно.

    EN:
        Reproducible bootstrap: the seed is explicit.
    """
    import numpy as np

    rng = np.random.default_rng(seed)
    values = np.asarray(values)
    boot = [rng.choice(values, size=len(values), replace=True).mean() for _ in range(n_boot)]
    return values.mean(), float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 10.3. Тезис: если анализ содержит случайные процедуры
        bootstrap/перестановки, seed должен быть зафиксирован.

    EN:
        Subsection 10.3. Thesis: if analysis contains random procedures such
        as bootstrap/permutation, the seed should be fixed.
    """
    rows = []
    for group, part in df.groupby("therapy_group"):
        mean, low, high = bootstrap_mean_ci(part["sbp_mm_hg"], seed=42)
        rows.append({"therapy_group": group, "mean": mean, "low": low, "high": high})
    summary = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.errorbar(
        summary["therapy_group"],
        summary["mean"],
        yerr=[summary["mean"] - summary["low"], summary["high"] - summary["mean"]],
        fmt="o",
        capsize=5,
    )

    ax.set_xlabel("Группа терапии")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.set_title("Bootstrap 95% CI с фиксированным seed")
    ax.tick_params(axis="x", rotation=20)
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
