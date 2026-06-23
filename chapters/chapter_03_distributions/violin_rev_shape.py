# file: violin_reveals_shape.py
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
rng = np.random.default_rng(0)

unimodal = rng.normal(100, 20, 400)
bimodal = np.concatenate([rng.normal(70, 8, 200),
                          rng.normal(130, 8, 200)])
data = pd.DataFrame({
    "Показатель": np.concatenate([unimodal, bimodal]),
    "Распределение": ["Унимодальное"] * 400 + ["Бимодальное"] * 400,
})

fig, ax = plt.subplots(figsize=(6.5, 4.5))
sns.violinplot(
    data=data, x="Распределение", y="Показатель",
    inner="box",            # внутри — миниатюрный boxplot
    color="#56B4E9", ax=ax
)
ax.set_title("Скрипичный график раскрывает бимодальность")
ax.set_xlabel("")
ax.set_ylabel("Показатель, усл. ед.")

sns.despine(ax=ax)
fig.tight_layout()
save_figure(fig, "fig_violin_reveals_shape")