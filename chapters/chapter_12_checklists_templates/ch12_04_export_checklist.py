# -*- coding: utf-8 -*-
"""
Chapter 12 standalone checklist/template script.

RU:
    Один файл = одна иллюстрация одного тезиса главы 12.
    Скрипт читает данные из data/processed/ и сохраняет результат в figure/ или report/.

EN:
    One file = one illustration of one Chapter 12 thesis.
    The script reads data from data/processed/ and saves output to figure/ or report/.
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
TEMPLATE_DIR = PROJECT_ROOT / "templates"


def set_scientific_style() -> None:
    """
    RU:
        Единый академический стиль для чек-листов и шаблонов.

    EN:
        Unified academic style for checklists and templates.
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


def save_table(df: pd.DataFrame, filename: str) -> Path:
    """
    RU:
        Сохраняет таблицу в report/.

    EN:
        Saves a table into report/.
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / filename
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Saved: {path}")
    return path

FIGURE_ID = "ch12_04_export_checklist"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 12.4. Тезис: экспорт рисунка должен быть проверяемым:
        нужные форматы созданы, размер файла не равен нулю.

    EN:
        Subsection 12.4. Thesis: figure export should be verifiable:
        required formats are created and file size is non-zero.
    """
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    sns.histplot(df, x="sbp_mm_hg", bins=25, ax=ax)
    ax.set_xlabel("Систолическое АД, мм рт. ст.")
    ax.set_ylabel("Частота")
    ax.set_title("Экспортный чек-лист")
    sns.despine(ax=ax)
    fig.tight_layout()
    return fig


def export_and_check(fig: plt.Figure, name: str, formats: tuple[str, ...]) -> pd.DataFrame:
    """
    RU:
        Экспортирует рисунок и возвращает таблицу проверки файлов.

    EN:
        Exports the figure and returns a file-check table.
    """
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for ext in formats:
        path = FIGURE_DIR / f"{name}.{ext}"
        fig.savefig(path, dpi=600, bbox_inches="tight", facecolor="white")
        rows.append({
            "file": path.name,
            "exists": path.exists(),
            "size_kb": round(path.stat().st_size / 1024, 1),
            "status": "OK" if path.exists() and path.stat().st_size > 0 else "ERROR",
        })
    return pd.DataFrame(rows)


def main() -> None:
    set_scientific_style()
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    check = export_and_check(fig, FIGURE_ID, formats=("png", "pdf", "tiff", "svg"))
    save_table(check, "ch12_04_export_checklist.csv")
    print(check.to_string(index=False))
    plt.show()


if __name__ == "__main__":
    main()
