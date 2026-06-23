# file: boxplot_anatomy.py
from turtle import color

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

rng = np.random.default_rng(3)
data = rng.normal(70, 10, 200)          # ЧСС, уд/мин
data = np.append(data, [110, 115, 35])  # добавим выбросы

q1, med, q3 = np.percentile(data, [25, 50, 75])
iqr = q3 - q1

fig, ax = plt.subplots(figsize=(7, 4))
sns.boxplot(x=data, color="#56B4E9", width=0.4, ax=ax,
            flierprops=dict(marker="o", markersize=4,
                            markerfacecolor="#D55E00"))

# Поясняющие подписи
ax.annotate("Медиана (Q2)", xy=(med, 0), xytext=(med+iqr, 0.32),
            ha="center", arrowprops=dict(arrowstyle="->", color="black"))
ax.annotate("Q1", xy=(q1, -0.2), xytext=(q1, -0.34), ha="center",
            arrowprops=dict(arrowstyle="->", color="black"))
ax.annotate("Q3", xy=(q3, -0.2), xytext=(q3, -0.34), ha="center",
            arrowprops=dict(arrowstyle="->", color="black"))
ax.annotate("Выброс", xy=(115, 0), xytext=(115, 0.3), ha="center",
            arrowprops=dict(arrowstyle="->", color="black"))
ax.text(med, 0.22, f"IQR = {iqr:.0f}", ha="center", fontsize=9)

ax.set_xlabel("Частота сердечных сокращений, уд/мин")
ax.set_yticks([])
ax.set_ylim(-0.5, 0.5)

sns.despine(ax=ax, left=True)
fig.tight_layout()
save_figure(fig, "fig_boxplot_anatomy")