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

FIGURE_ID = "ch12_02_starter_template_generator"

TEMPLATE = '# -*- coding: utf-8 -*-\n"""\nReusable scientific figure template.\n\nRU:\n    Замените FIGURE_ID, DATA_FILE и build_figure() под конкретный тезис.\n\nEN:\n    Replace FIGURE_ID, DATA_FILE and build_figure() for a specific thesis.\n"""\nfrom pathlib import Path\n\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport seaborn as sns\n\n\nPROJECT_ROOT = Path(__file__).resolve().parents[2]\nDATA_DIR = PROJECT_ROOT / "data" / "processed"\nFIGURE_DIR = PROJECT_ROOT / "figure"\n\nFIGURE_ID = "replace_me"\nDATA_FILE = "clinical_cross_sectional.csv"\n\n\ndef set_scientific_style() -> None:\n    sns.set_theme(context="paper", style="ticks", palette="colorblind")\n    plt.rcParams.update({\n        "font.family": "DejaVu Sans",\n        "font.size": 11,\n        "savefig.dpi": 600,\n        "savefig.bbox": "tight",\n        "savefig.facecolor": "white",\n    })\n\n\ndef load_data() -> pd.DataFrame:\n    return pd.read_csv(DATA_DIR / DATA_FILE, encoding="utf-8-sig")\n\n\ndef save_figure(fig: plt.Figure) -> None:\n    FIGURE_DIR.mkdir(parents=True, exist_ok=True)\n    for ext in ("png", "pdf", "tiff"):\n        fig.savefig(FIGURE_DIR / f"{FIGURE_ID}.{ext}", dpi=600, bbox_inches="tight", facecolor="white")\n\n\ndef build_figure(df: pd.DataFrame) -> plt.Figure:\n    fig, ax = plt.subplots(figsize=(6.5, 4.2))\n    sns.scatterplot(data=df, x="bmi_kg_m2", y="sbp_mm_hg", ax=ax)\n    ax.set_xlabel("ИМТ, кг/м²")\n    ax.set_ylabel("Систолическое АД, мм рт. ст.")\n    ax.set_title("Replace title")\n    sns.despine(ax=ax)\n    fig.tight_layout()\n    return fig\n\n\ndef main() -> None:\n    set_scientific_style()\n    df = load_data()\n    fig = build_figure(df)\n    save_figure(fig)\n    plt.show()\n\n\nif __name__ == "__main__":\n    main()\n'


def main() -> None:
    """
    RU:
        Подраздел 12.2. Тезис: шаблон стартового файла ускоряет создание
        новых рисунков и снижает вероятность забыть стиль/экспорт/пути.

    EN:
        Subsection 12.2. Thesis: a starter template speeds up creation of new
        figures and reduces the chance of forgetting style/export/paths.
    """
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = TEMPLATE_DIR / "scientific_figure_template.py"
    output_path.write_text(TEMPLATE, encoding="utf-8")
    print(f"Saved template: {output_path}")


if __name__ == "__main__":
    main()
