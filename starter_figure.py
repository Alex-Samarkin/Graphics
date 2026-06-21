# starter_figure.py
# Standalone figure script template.
#
# Rule:
#   one Python file = one illustration of one thesis
#
# Run from the project root:
#   uv run python chapters/chapter_XX_topic/starter_figure.py
#
# This file intentionally does NOT generate data.
# Put datasets into data/ and exported figures into figure/.

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
FIGURE_DIR = PROJECT_ROOT / "figure"


# ---------------------------------------------------------------------
# Figure metadata
# ---------------------------------------------------------------------

FIGURE_ID = "fig_000_starter"
FIGURE_TITLE = "Starter figure"
FIGURE_THESIS = "This figure illustrates one clearly formulated scientific thesis."

# Replace this with the actual dataset file when needed.
# Example:
#   DATA_FILE = DATA_DIR / "processed" / "patients.csv"
DATA_FILE = DATA_DIR / "processed" / "example.csv"


# ---------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------

def set_scientific_style() -> None:
    """Apply a clean scientific plotting style."""
    sns.set_theme(
        context="paper",
        style="ticks",
        palette="colorblind",
    )

    plt.rcParams.update(
        {
            # Fonts
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,

            # Lines and axes
            "axes.linewidth": 1.0,
            "lines.linewidth": 1.8,
            "lines.markersize": 6,

            # Spines
            "axes.spines.top": False,
            "axes.spines.right": False,

            # Export defaults
            "figure.dpi": 120,
            "savefig.dpi": 600,
            "savefig.bbox": "tight",
            "savefig.facecolor": "white",

            # Default figure size, inches
            "figure.figsize": (6.0, 4.0),
        }
    )


# ---------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------

def ensure_directories() -> None:
    """Create output directories if they do not exist."""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def load_data(path: Path) -> pd.DataFrame:
    """
    Load a dataset from CSV.

    The starter template expects CSV because it is transparent and
    convenient for teaching. Replace this function if you use XLSX,
    Parquet, JSON, or another format.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Put the required dataset into data/processed/ or update DATA_FILE."
        )

    return pd.read_csv(path, encoding="utf-8-sig")


def save_figure(
    fig: plt.Figure,
    name: str,
    formats: tuple[str, ...] = ("png", "pdf", "tiff"),
) -> None:
    """Save one figure in several publication-friendly formats."""
    ensure_directories()

    for fmt in formats:
        output_path = FIGURE_DIR / f"{name}.{fmt}"
        fig.savefig(
            output_path,
            dpi=600,
            bbox_inches="tight",
            facecolor="white",
        )
        print(f"Saved: {output_path}")


# ---------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------

def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    Build one figure.

    Replace the example content with the actual visual argument
    for the current chapter and thesis.
    """
    fig, ax = plt.subplots()

    # -----------------------------------------------------------------
    # Example placeholder.
    # Replace these columns with real columns from your dataset.
    # -----------------------------------------------------------------
    required_columns = {"x", "y"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "The starter plot expects columns 'x' and 'y'. "
            f"Missing columns: {sorted(missing_columns)}.\n"
            "Replace build_figure() with the actual plotting code "
            "for the current illustration."
        )

    ax.plot(df["x"], df["y"], marker="o")
    ax.set_xlabel("X variable, units")
    ax.set_ylabel("Y variable, units")

    # For articles and theses, the title is often placed in the caption,
    # not inside the plot. Keep this line only for drafts/presentations.
    ax.set_title(FIGURE_TITLE)

    sns.despine(ax=ax)

    return fig


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    print(f"Figure ID: {FIGURE_ID}")
    print(f"Thesis: {FIGURE_THESIS}")

    set_scientific_style()
    ensure_directories()

    df = load_data(DATA_FILE)
    fig = build_figure(df)

    save_figure(fig, FIGURE_ID)
    plt.show()


if __name__ == "__main__":
    main()
