# file: boxplot_small_n_problem.py
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

# Малые группы: эффект препарата у 5 и 6 пациентов
rng = np.random.default_rng(42)
small = pd.DataFrame({
    "Группа": ["Плацебо"] * 5 + ["Препарат"] * 6,
    "Снижение АД, мм рт. ст.":
        list(rng.normal(5, 4, 5)) + list(rng.normal(12, 5, 6)),
})

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# ПЛОХО: голый boxplot скрывает, что в группах всего 5–6 точек
sns.boxplot(data=small, x="Группа", y="Снижение АД, мм рт. ст.",
            color="#56B4E9", width=0.5, ax=axes[0])
axes[0].set_title("Плохо: boxplot скрывает крошечный размер групп")

# ХОРОШО: показываем сами наблюдения поверх лёгкого boxplot
sns.boxplot(data=small, x="Группа", y="Снижение АД, мм рт. ст.",
            color="white", width=0.5, fliersize=0,
            linewidth=1.2, ax=axes[1])
sns.stripplot(data=small, x="Группа", y="Снижение АД, мм рт. ст.",
              color="#D55E00", size=7, jitter=0.08,
              alpha=0.9, ax=axes[1])
axes[1].set_title("Хорошо: видны все наблюдения")

sns.despine(fig=fig)
fig.tight_layout()
save_figure(fig, "fig_boxplot_small_n")