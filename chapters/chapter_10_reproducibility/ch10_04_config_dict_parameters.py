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
    uv run python chapters/chapter_10_reproducibility/ch10_04_config_dict_parameters.py

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


FIGURE_ID = "ch10_04_config_dict_parameters"

CONFIG = {
    "dataset": "clinical_cross_sectional.csv",
    "x": "bmi_kg_m2",
    "y": "sbp_mm_hg",
    "hue": "therapy_group",
    "alpha": 0.65,
    "figure_size": (7, 4.5),
}


def build_figure(df: pd.DataFrame, config: dict) -> plt.Figure:
    """
    RU:
        Подраздел 10.4. Тезис: конфигурация в одном месте делает скрипт
        понятнее и снижает риск случайных правок в логике анализа.

    EN:
        Subsection 10.4. Thesis: keeping configuration in one place makes
        the script clearer and reduces accidental edits to analysis logic.
    """
    fig, ax = plt.subplots(figsize=config["figure_size"])

    sns.scatterplot(
        data=df,
        x=config["x"],
        y=config["y"],
        hue=config["hue"],
        alpha=config["alpha"],
        ax=ax,
    )

    ax.set_xlabel("ИМТ, кг/м²")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.set_title("Параметры фигуры вынесены в CONFIG")
    ax.legend(title="Группа", bbox_to_anchor=(1.02, 1), loc="upper left")
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_dataset(CONFIG["dataset"])
    print("Configuration:")
    for key, value in CONFIG.items():
        print(f"  {key}: {value}")

    fig = build_figure(df, CONFIG)
    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
