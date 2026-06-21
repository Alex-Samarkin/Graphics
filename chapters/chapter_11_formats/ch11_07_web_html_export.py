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
    uv run python chapters/chapter_11_formats/ch11_07_web_html_export.py

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


FIGURE_ID = "ch11_07_web_html_export"


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """
    RU:
        Подраздел 11.7. Тезис: для веб-публикации можно сохранить
        статический PNG и простой HTML-контейнер с подписью.

    EN:
        Subsection 11.7. Thesis: for web publishing, a static PNG and a simple
        HTML container with caption can be exported.
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    sns.regplot(
        data=df,
        x="bmi_kg_m2",
        y="sbp_mm_hg",
        ci=95,
        scatter_kws={"alpha": 0.45, "s": 24},
        ax=ax,
    )
    ax.set_xlabel("ИМТ, кг/м²")
    ax.set_ylabel("Систолическое АД, мм рт. ст.")
    ax.set_title("Веб-версия статического научного графика")
    sns.despine(ax=ax)

    fig.tight_layout()
    return fig


def write_html_page(name: str, caption: str) -> None:
    """
    RU:
        Создаёт простой HTML-файл, который вставляет экспортированный PNG.

    EN:
        Creates a simple HTML file embedding the exported PNG.
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    html = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{name}</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; line-height: 1.5; }}
    figure {{ margin: 0; }}
    img {{ max-width: 100%; height: auto; border: 1px solid #ddd; }}
    figcaption {{ margin-top: 12px; color: #333; }}
  </style>
</head>
<body>
  <figure>
    <img src="../figure/{name}.png" alt="{name}">
    <figcaption>{caption}</figcaption>
  </figure>
</body>
</html>
"""
    path = REPORT_DIR / f"{name}.html"
    path.write_text(html, encoding="utf-8")
    print(f"Saved HTML: {path}")


def main() -> None:
    set_scientific_style("web")
    df = load_dataset("clinical_cross_sectional.csv")
    fig = build_figure(df)
    save_figure(fig, FIGURE_ID, formats=("png", "svg"))
    write_html_page(
        FIGURE_ID,
        "Связь ИМТ и систолического АД; линия показывает линейную регрессию, полоса — 95% CI.",
    )
    plt.show()


if __name__ == "__main__":
    main()
