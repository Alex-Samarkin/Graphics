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

FIGURE_ID = "ch12_01_figure_quality_checklist_table"


def build_checklist() -> pd.DataFrame:
    """
    RU:
        Создаёт универсальный чек-лист качества научного рисунка.

    EN:
        Creates a universal scientific-figure quality checklist.
    """
    return pd.DataFrame({
        "block": [
            "Смысл", "Смысл", "Данные", "Данные", "Оси", "Оси",
            "Цвет", "Цвет", "Статистика", "Экспорт", "Воспроизводимость"
        ],
        "criterion": [
            "Рисунок отвечает на один главный вопрос",
            "Тип графика соответствует типу данных",
            "Показаны индивидуальные наблюдения там, где это важно",
            "Не скрыта вариабельность",
            "Оси подписаны с единицами измерения",
            "Шкалы не искажают вывод",
            "Цвет не является единственным кодом различий",
            "Палитра совместима с дальтонизмом/печатью",
            "Ясно, что означают SD/SEM/CI/p-value",
            "Формат и dpi соответствуют назначению",
            "Данные, код и параметры запуска сохранены",
        ],
        "status": ["check"] * 11,
    })


def build_figure(checklist: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 12.1. Тезис: чек-лист превращает качество рисунка
        из субъективного впечатления в проверяемую процедуру.

    EN:
        Subsection 12.1. Thesis: a checklist turns figure quality from a
        subjective impression into a verifiable procedure.
    """
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.axis("off")
    table = ax.table(
        cellText=checklist.values,
        colLabels=["Блок", "Критерий", "Статус"],
        loc="center",
        cellLoc="left",
        colLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.35)
    ax.set_title("Чек-лист качества научного рисунка", pad=18)
    fig.tight_layout()
    return fig


def main() -> None:
    set_scientific_style()
    checklist = build_checklist()
    save_table(checklist, "ch12_01_figure_quality_checklist.csv")
    fig = build_figure(checklist)
    save_figure(fig, FIGURE_ID, formats=("png", "pdf"))
    plt.show()


if __name__ == "__main__":
    main()
