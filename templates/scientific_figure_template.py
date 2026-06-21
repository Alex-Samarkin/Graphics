# -*- coding: utf-8 -*-
"""
Reusable scientific figure template.

RU:
    Замените FIGURE_ID, DATA_FILE и build_figure() под конкретный тезис.

EN:
    Replace FIGURE_ID, DATA_FILE and build_figure() for a specific thesis.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
FIGURE_DIR = PROJECT_ROOT / "figure"

FIGURE_ID = "replace_me"
DATA_FILE = "clinical_cross_sectional.csv"


def set_scientific_style() -> None:
    sns.set_theme(context="paper", style="ticks", palette="colorblind")
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
    })


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / DATA_FILE, encoding="utf-8-sig")


def save_figure(fig: plt.Figure) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf", "tiff"):
        fig.savefig(FIGURE_DIR / f"{FIGURE_ID}.{ext}", dpi=600, bbox_inches="tight", facecolor="white")


def build_figure(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    sns.scatterplot(data=df, x="bmi_kg_m2", y="sbp_mm_hg", ax=ax)
    ax.set_xlabel("ИМТ, кг/м²")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.set_title("Replace title")
    sns.despine(ax=ax)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    df = load_data()
    fig = build_figure(df)
    save_figure(fig)
    plt.show()


if __name__ == "__main__":
    main()
