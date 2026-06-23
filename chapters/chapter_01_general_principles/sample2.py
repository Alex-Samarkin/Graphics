# file: hist_bins_problem.py
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
df = pd.read_csv("data/processed/patients.csv", encoding="utf-8-sig")
bmi = df["bmi"]

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Слишком мало бинов — теряется форма
axes[0].hist(bmi, bins=3, color="#D55E00", edgecolor="white")
axes[0].set_title("Плохо: слишком мало бинов (3)")
axes[0].set_xlabel("ИМТ, кг/м²")
axes[0].set_ylabel("Число пациентов")

# Слишком много бинов — гистограмма «рассыпается»
axes[1].hist(bmi, bins=80, color="#D55E00", edgecolor="white")
axes[1].set_title("Плохо: слишком много бинов (80)")
axes[1].set_xlabel("ИМТ, кг/м²")
axes[1].set_ylabel("Число пациентов")

sns.despine(fig=fig)
fig.tight_layout()
save_figure(fig, "fig_hist_bins_problem")