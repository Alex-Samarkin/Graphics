# file: kde_bandwidth_problem.py
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

# Сконструируем заведомо двухвершинное распределение:
# смесь распределений АД двух подгрупп (с гипотонией и гипертонией)
rng = np.random.default_rng(7)
mix = np.concatenate([
    rng.normal(110, 7, 150),   # подгруппа с нормальным/низким АД
    rng.normal(155, 8, 150),   # подгруппа с высоким АД
])

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Слишком малое сглаживание — ложные пики
sns.kdeplot(mix, bw_adjust=0.15, color="#D55E00",
            fill=True, alpha=0.3, ax=axes[0])
axes[0].set_title("Плохо: слишком малое сглаживание (bw_adjust=0.15)")
axes[0].set_xlabel("Систолическое АД, мм рт. ст.")
axes[0].set_ylabel("Плотность")

# Слишком большое сглаживание — теряются обе вершины
sns.kdeplot(mix, bw_adjust=2.5, color="#D55E00",
            fill=True, alpha=0.3, ax=axes[1])
axes[1].set_title("Плохо: слишком большое сглаживание (bw_adjust=2.5)")
axes[1].set_xlabel("Систолическое АД, мм рт. ст.")
axes[1].set_ylabel("Плотность")

sns.despine(fig=fig)
fig.tight_layout()
save_figure(fig, "fig_kde_bandwidth_problem")