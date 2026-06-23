# file: boxplot_hides_shape.py
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

# Два РАЗНЫХ распределения с близкими медианой и квартилями
unimodal = rng.normal(100, 20, 400)
bimodal = np.concatenate([rng.normal(70, 8, 200),
                          rng.normal(130, 8, 200)])

data = pd.DataFrame({
    "Показатель": np.concatenate([unimodal, bimodal]),
    "Распределение": ["Унимодальное"] * 400 + ["Бимодальное"] * 400,
})

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# Слева: boxplot — ящики выглядят почти одинаково
sns.boxplot(data=data, x="Распределение", y="Показатель",
            color="#56B4E9", width=0.5, ax=axes[0])
axes[0].set_title("Boxplot: ящики почти неотличимы")

# Справа: гистограммы раскрывают истинную разницу форм
sns.histplot(data=data, x="Показатель", hue="Распределение",
             stat="density", common_norm=False, element="step",
             bins="auto", alpha=0.4, ax=axes[1])
axes[1].set_title("Гистограммы: формы радикально разные")

sns.despine(fig=fig)
fig.tight_layout()
save_figure(fig, "fig_boxplot_hides_shape")