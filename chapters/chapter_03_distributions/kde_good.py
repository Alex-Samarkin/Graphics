# file: kde_boundary_problem.py
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


def save_figure(fig, name, outdir="figures", formats=("png", "pdf")):
    os.makedirs(outdir, exist_ok=True)
    for fmt in formats:
        path = os.path.join(outdir, f"{name}.{fmt}")
        fig.savefig(path, dpi=600, bbox_inches="tight", facecolor="white")
        print(f"Сохранено: {path}")
    plt.show()


set_scientific_style()
df = pd.read_csv("data/patients.csv", encoding="utf-8-sig")
crp = df["crp"]   # СРБ не может быть отрицательным!

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# ПЛОХО: обычная KDE заходит в область crp < 0
sns.kdeplot(crp, color="#D55E00", fill=True, alpha=0.3, ax=axes[0])
axes[0].axvline(0, color="black", linewidth=1.0, linestyle=":")
axes[0].set_title("Плохо: плотность «вытекает» в crp < 0")
axes[0].set_xlabel("С-реактивный белок, мг/л")
axes[0].set_ylabel("Плотность")

# ХОРОШО: ограничиваем носитель оценки границей нуля
sns.kdeplot(crp, color="#0072B2", fill=True, alpha=0.3,
            clip=(0, None), cut=0, ax=axes[1])
axes[1].axvline(0, color="black", linewidth=1.0, linestyle=":")
axes[1].set_title("Хорошо: оценка ограничена crp ≥ 0")
axes[1].set_xlabel("С-реактивный белок, мг/л")
axes[1].set_ylabel("Плотность")

sns.despine(fig=fig)
fig.tight_layout()
save_figure(fig, "fig_kde_boundary")