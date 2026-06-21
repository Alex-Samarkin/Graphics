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

FIGURE_ID = "ch12_03_units_audit"


def check_units(labels: dict[str, str]) -> pd.DataFrame:
    """
    RU:
        Проверяет, содержат ли подписи осей единицы измерения.

    EN:
        Checks whether axis labels contain measurement units.
    """
    unit_markers = ["мм", "мг", "мл", "кг", "год", "%", "mm", "mg", "kg", "years"]
    rows = []
    for axis, label in labels.items():
        has_unit = any(marker in label for marker in unit_markers)
        rows.append({"axis": axis, "label": label, "has_unit_marker": has_unit})
    return pd.DataFrame(rows)


def main() -> None:
    """
    RU:
        Подраздел 12.3. Тезис: отсутствие единиц измерения можно выявлять
        простыми автоматическими проверками.

    EN:
        Subsection 12.3. Thesis: missing units can be detected using simple
        automated checks.
    """
    labels = {
        "x": "ИМТ, кг/м²",
        "y": "Систолическое АД, мм рт. ст.",
        "bad_example": "value",
    }
    audit = check_units(labels)
    save_table(audit, "ch12_03_units_audit.csv")
    print(audit.to_string(index=False))


if __name__ == "__main__":
    main()
