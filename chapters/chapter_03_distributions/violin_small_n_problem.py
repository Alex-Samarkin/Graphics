# file: violin_small_n_problem.py
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
rng = np.random.default_rng(42)
small = pd.DataFrame({
    "Группа": ["Плацебо"] * 6 + ["Препарат"] * 7,
    "Снижение АД, мм рт. ст.":
        list(rng.normal(5, 4, 6)) + list(rng.normal(12, 5, 7)),
})

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# ПЛОХО: violin по 6–7 точкам рисует «гладкое» распределение из ничего
sns.violinplot(data=small, x="Группа", y="Снижение АД, мм рт. ст.",
               color="#56B4E9", inner=None, ax=axes[0])
axes[0].set_title("Плохо: violin придумывает форму по 6–7 точкам")

# ХОРОШО: для малых групп показываем сами точки
sns.stripplot(data=small, x="Группа", y="Снижение АД, мм рт. ст.",
              color="#D55E00", size=8, jitter=0.1, alpha=0.9,
              ax=axes[1])
# добавим маркер медианы
sns.boxplot(data=small, x="Группа", y="Снижение АД, мм рт. ст.",
            color="white", width=0.4, fliersize=0,
            showcaps=False, boxprops=dict(alpha=0),
            whiskerprops=dict(alpha=0),
            medianprops=dict(color="black", linewidth=2),
            ax=axes[1])
axes[1].set_title("Хорошо: все точки + медиана")

sns.despine(fig=fig)
fig.tight_layout()
save_figure(fig, "fig_violin_small_n")