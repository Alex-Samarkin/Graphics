# -*- coding: utf-8 -*-
"""
Chapter 09 standalone composite/export script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 9.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 9 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_09_composite_export/ch09_02_nested_gridspec_risk_table.py

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
        Единый академический стиль для составных рисунков и экспорта.

    EN:
        Unified academic style for composite figures and export.
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


def add_panel_label(ax: plt.Axes, label: str) -> None:
    """
    RU:
        Добавляет буквенную метку панели.

    EN:
        Adds a panel letter.
    """
    ax.text(
        -0.12,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top",
        ha="left",
    )


FIGURE_ID = "ch09_02_nested_gridspec_risk_table"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 9.2. Тезис: составной рисунок может включать график и
        таблицу, например Kaplan–Meier и таблицу числа под риском.

    EN:
        Subsection 9.2. Thesis: a composite figure can include both a plot
        and a table, such as Kaplan-Meier and a number-at-risk table.
    """
    from lifelines import KaplanMeierFitter
    import matplotlib.gridspec as gridspec

    times = [0, 6, 12, 18, 24, 30, 36]
    groups = list(df["therapy_group"].unique())

    fig = plt.figure(figsize=(7.5, 6))
    gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1], hspace=0.08)
    ax = fig.add_subplot(gs[0])
    ax_table = fig.add_subplot(gs[1])

    for group, part in df.groupby("therapy_group"):
        kmf = KaplanMeierFitter()
        kmf.fit(part["time_months"], event_observed=part["event"], label=group)
        kmf.plot_survival_function(ax=ax, ci_show=False)

    ax.set_xlabel("")
    ax.set_ylabel("Вероятность без события")
    ax.set_title("Kaplan–Meier + таблица числа под риском")
    ax.set_ylim(0, 1.02)
    add_panel_label(ax, "A")
    sns.despine(ax=ax)

    cell_text = []
    for group in groups:
        part = df[df["therapy_group"] == group]
        cell_text.append([(part["time_months"] >= t).sum() for t in times])

    ax_table.axis("off")
    table = ax_table.table(
        cellText=cell_text,
        rowLabels=groups,
        colLabels=[str(t) for t in times],
        loc="center",
        cellLoc="center",
        rowLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.2)
    ax_table.set_title("B. Число под риском, мес.", fontsize=10)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset("survival_kaplan_meier.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
