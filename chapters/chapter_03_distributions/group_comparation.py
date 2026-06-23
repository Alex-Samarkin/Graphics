# file: boxplot_groups.py
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

# Упорядочим стадии по клинической логике (а не по алфавиту)
# add stage column to the DataFrame with ordered categorical type and calculate fake stage column first

stage_order = ["I", "II", "III", "IV"]
if "stage" not in df.columns:
    # Derive a stage value from the available clinical variables.
    # Use quantiles so each stage contains roughly the same number of observations.
    score = (
        df["crp"].fillna(0) +
        0.02 * df["age"].fillna(0) +
        0.05 * df["bmi"].fillna(0)
    )
    df["stage"] = pd.qcut(
        score.rank(method="first"),
        q=len(stage_order),
        labels=stage_order,
        duplicates="drop"
    )
else:
    df["stage"] = df["stage"].astype(str)

# Ensure stage ordering is preserved for plotting
df["stage"] = pd.Categorical(df["stage"], categories=stage_order, ordered=True)



fig, ax = plt.subplots(figsize=(6.5, 4.5))
sns.boxplot(
    data=df, x="stage", y="crp",
    order=stage_order, color="#56B4E9",
    width=0.55, fliersize=3, ax=ax
)

ax.set_xlabel("Стадия заболевания")
ax.set_ylabel("С-реактивный белок, мг/л")

# Подпись числа наблюдений над осью x
counts = df.groupby("stage", observed=False).size().reindex(stage_order, fill_value=0)
for i, st in enumerate(stage_order):
    n = counts.loc[st]
    ax.text(
        i, 0.01, f"n={n}",
        ha="center", va="bottom", fontsize=9, color="gray",
        transform=ax.get_xaxis_transform()
    )

sns.despine(ax=ax)
fig.tight_layout()
save_figure(fig, "fig_boxplot_groups")