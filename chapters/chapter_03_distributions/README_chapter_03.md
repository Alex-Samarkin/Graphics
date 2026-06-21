# Chapter 03 Python files

RU:
Файлы главы 3 сгруппированы по подразделам: распределения, гистограммы, KDE/rug, boxplot, violin/strip/swarm и сводные фигуры.

EN:
Chapter 3 files are grouped by subsections: distributions, histograms, KDE/rug, boxplots, violin/strip/swarm plots, and summary figures.

## 3.1. Зачем визуализировать распределение

- `ch03_01_mean_median_skewness_crp.py`

## 3.2. Гистограмма

- `ch03_02_histogram_bins_problem.py`
- `ch03_02_histogram_good_practice.py`
- `ch03_02_grouped_histogram_overlay.py`

## 3.3. KDE и rug plot

- `ch03_03_kde_bandwidth_problem.py`
- `ch03_03_kde_good_with_rug.py`
- `ch03_03_kde_boundary_logscale.py`

## 3.4. Boxplot

- `ch03_04_boxplot_anatomy.py`
- `ch03_04_boxplot_group_comparison.py`
- `ch03_04_boxplot_hides_shape.py`

## 3.5. Violin, strip и swarm

- `ch03_05_violin_reveals_shape.py`
- `ch03_05_violin_small_n_problem.py`
- `ch03_05_box_strip_combo.py`
- `ch03_05_strip_vs_swarm.py`

## 3.6. Сводные примеры

- `ch03_06_summary_before_after.py`
- `ch03_06_publication_distribution_panel.py`

## Usage

Copy files into:

```text
chapters/chapter_03_distributions/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_03_distributions/ch03_02_histogram_good_practice.py
```
