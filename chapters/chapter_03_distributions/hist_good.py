# file: hist_good.py
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
bmi = df["bmi"]

fig, ax = plt.subplots(figsize=(6.5, 4.3))

# Гистограмма с автоподбором бинов и наложенной KDE
sns.histplot(
    bmi, bins="auto", kde=True,
    color="#0072B2", edgecolor="white",
    alpha=0.75, ax=ax
)

# Линии среднего и медианы
mean_val = bmi.mean()
median_val = bmi.median()
ax.axvline(mean_val, color="#D55E00", linestyle="--", linewidth=1.6,
           label=f"Среднее = {mean_val:.1f}")
ax.axvline(median_val, color="#009E73", linestyle=":", linewidth=1.8,
           label=f"Медиана = {median_val:.1f}")

ax.set_xlabel("Индекс массы тела, кг/м²")
ax.set_ylabel("Число пациентов")
ax.legend(frameon=False)

sns.despine(ax=ax)
fig.tight_layout()
save_figure(fig, "fig_hist_good")