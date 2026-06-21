# -*- coding: utf-8 -*-
"""
Chapter 11 standalone context/format script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 11.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/.

EN:
    One file = one illustration of one Chapter 11 thesis.
    The script reads data from data/processed/ and saves output to figure/.

Run:
    uv run python chapters/chapter_11_formats/ch11_06_report_dashboard_style.py

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


def set_scientific_style(context: str = "paper") -> None:
    """
    RU:
        Единый стиль с возможностью адаптации под контекст:
        paper, thesis, presentation, poster, web.

    EN:
        Unified style with context adaptation:
        paper, thesis, presentation, poster, web.
    """
    context_settings = {
        "paper": {"font": 10, "title": 11, "label": 10, "tick": 9, "legend": 9},
        "thesis": {"font": 11, "title": 12, "label": 11, "tick": 10, "legend": 10},
        "presentation": {"font": 15, "title": 18, "label": 16, "tick": 13, "legend": 13},
        "poster": {"font": 18, "title": 22, "label": 19, "tick": 16, "legend": 16},
        "web": {"font": 12, "title": 14, "label": 12, "tick": 11, "legend": 11},
    }
    s = context_settings.get(context, context_settings["paper"])

    sns.set_theme(context="paper", style="ticks", palette="colorblind")
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": s["font"],
        "axes.titlesize": s["title"],
        "axes.labelsize": s["label"],
        "xtick.labelsize": s["tick"],
        "ytick.labelsize": s["tick"],
        "legend.fontsize": s["legend"],
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
    RU: Добавляет буквенную метку панели.
    EN: Adds a panel letter.
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


FIGURE_ID = "ch11_06_report_dashboard_style"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 11.6. Тезис: для аналитического отчёта важна не только
        красота графика, но и быстрая управленческая читаемость показателей.

    EN:
        Subsection 11.6. Thesis: for an analytical report, the figure should
        support fast managerial reading of indicators, not just aesthetics.
    """
    import numpy as np

    summary = df.groupby("therapy_group", as_index=False).agg(
        n=("patient_id", "count"),
        mean_sbp=("sbp_mm_hg", "mean"),
        mean_glucose=("glucose_mmol_l", "mean"),
        complication_rate=("complication", "mean"),
    )
    summary["complication_rate"] *= 100

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))

    metrics = [
        ("n", "Пациенты, n", "A"),
        ("mean_sbp", "Среднее АД", "B"),
        ("mean_glucose", "Средняя глюкоза", "C"),
        ("complication_rate", "Осложнения, %", "D"),
    ]

    for ax, (metric, title, label) in zip(axes.ravel(), metrics):
        sns.barplot(data=summary, x="therapy_group", y=metric, edgecolor="black", ax=ax)
        ax.set_title(f"{label}. {title}")
        ax.set_xlabel("Группа")
        ax.set_ylabel(title)
        ax.tick_params(axis="x", rotation=20)
        sns.despine(ax=ax)

    fig.suptitle("Отчётная панель по группам терапии", y=1.02)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style("web")
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID, formats=("png", "pdf"))
    plt.show()


if __name__ == "__main__":
    main()
