# file: hist_grouped.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def set_scientific_style():
    sns.set_theme(context="paper", style="ticks", palette="colorblind")
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.titlesize": 12, "axes.labelsize": 11,
        "xtick.labelsize": 10, "ytick.labelsize": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "savefig.dpi": 600, "savefig.bbox": "tight",
    })


def save_figure(fig, name, outdir="figure/samples", formats=("png", "pdf")):
    os.makedirs(outdir, exist_ok=True)
    for fmt in formats:
        path = os.path.join(outdir, f"{name}.{fmt}")
        fig.savefig(path, dpi=600, bbox_inches="tight", facecolor="white")
        print(f"Сохранено: {path}")
    plt.show()


set_scientific_style()
df = pd.read_csv("data/processed/patients.csv", encoding="utf-8-sig")

# Текстовая метка исхода для легенды
df["Исход"] = df["complication"].map({0: "Без осложнения",
                                       1: "Осложнение"})

fig, ax = plt.subplots(figsize=(6.5, 4.3))

# stat="density" — корректное сравнение групп РАЗНОГО размера
sns.histplot(
    data=df, x="crp", hue="Исход",
    stat="density",          # нормировка: сравниваем форму, а не объём
    common_norm=False,       # каждую группу нормируем отдельно
    bins="auto", element="step",
    alpha=0.4, ax=ax
)

ax.set_xlabel("С-реактивный белок, мг/л")
ax.set_ylabel("Плотность")

sns.despine(ax=ax)
fig.tight_layout()
save_figure(fig, "fig_hist_grouped")