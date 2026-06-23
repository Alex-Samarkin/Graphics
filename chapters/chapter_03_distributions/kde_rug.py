# file: kde_rug.py
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

# Малая выборка: уровень глюкозы у 25 пациентов
rng = np.random.default_rng(11)
glucose = rng.normal(6.2, 1.1, 25).clip(3.5, 12)

fig, ax = plt.subplots(figsize=(6.5, 4.3))

sns.kdeplot(glucose, color="#0072B2", fill=True, alpha=0.25,
            clip=(0, None), ax=ax, label="KDE")
sns.rugplot(glucose, color="#D55E00", height=0.08,
            linewidth=1.4, ax=ax)

ax.set_xlabel("Глюкоза натощак, ммоль/л")
ax.set_ylabel("Плотность")
ax.set_title(f"KDE и rug plot (n = {len(glucose)})")
ax.legend(frameon=False)

sns.despine(ax=ax)
fig.tight_layout()
save_figure(fig, "fig_kde_rug")