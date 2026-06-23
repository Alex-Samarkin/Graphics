import matplotlib.pyplot as plt
import seaborn as sns

def set_scientific_style():
    """Единый научный стиль оформления для всех графиков пособия."""
    sns.set_theme(
        context="paper",      # масштаб элементов под печать
        style="ticks",        # белый фон с засечками на осях
        palette="colorblind"  # палитра, безопасная для дальтоников
    )
    plt.rcParams.update({
        # --- Шрифты ---
        "font.family": "DejaVu Sans",  # поддерживает кириллицу
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,

        # --- Линии и элементы ---
        "axes.linewidth": 1.0,
        "lines.linewidth": 1.8,
        "lines.markersize": 6,

        # --- Оформление осей ---
        "axes.spines.top": False,    # убрать верхнюю рамку
        "axes.spines.right": False,  # убрать правую рамку
        "axes.grid": False,

        # --- Качество вывода ---
        "figure.dpi": 110,           # для экрана
        "savefig.dpi": 600,          # для сохранения файлов
        "savefig.bbox": "tight",     # обрезать поля
        "figure.figsize": (6, 4),    # размер по умолчанию, дюймы
    })

# Применяем стиль один раз в начале работы
set_scientific_style()

import numpy as np

x = np.linspace(0, 12, 100)
y = 120 - 15 * np.exp(-x / 3)

fig, ax = plt.subplots()
ax.plot(x, y, color="#0072B2")
ax.set_xlabel("Время терапии, нед.")
ax.set_ylabel("Систолическое АД, мм рт. ст.")
sns.despine(ax=ax)   # дополнительно убирает верхнюю/правую рамки
plt.show()