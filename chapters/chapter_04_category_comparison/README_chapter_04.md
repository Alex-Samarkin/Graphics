# Chapter 04 Python files

RU:
Файлы главы 4 сгруппированы по подразделам: столбчатые диаграммы категорий, проблема средних столбцов, сгруппированные/составные/100% столбцы, усечённая ось и альтернативы круговым диаграммам.

EN:
Chapter 4 files are grouped by subsections: categorical bar charts, the problem of bars of means, grouped/stacked/100% bars, truncated axes, and alternatives to pie charts.

## 4.1. Столбчатая диаграмма и отличие от гистограммы

- `ch04_01_countplot_category_frequencies.py`
- `ch04_01_bar_chart_vs_histogram.py`

## 4.2. Bar chart of means, SD/SEM/CI, pointplot

- `ch04_02_bar_of_means_problem.py`
- `ch04_02_sd_sem_ci_comparison.py`
- `ch04_02_pointplot_ci_alternative.py`

## 4.3. Сгруппированные, составные и нормированные столбцы

- `ch04_03_grouped_bar_chart.py`
- `ch04_03_stacked_bar_chart.py`
- `ch04_03_normalized_100_percent_bar.py`

## 4.4. Обрезанная ось и корректный показ малых различий

- `ch04_04_truncated_axis_bar_distortion.py`
- `ch04_04_dotplot_for_small_differences.py`
- `ch04_04_difference_plot.py`

## 4.5. Круговые диаграммы и альтернативы

- `ch04_05_pie_chart_problem.py`
- `ch04_05_bar_alternative_to_pie.py`
- `ch04_05_when_pie_is_acceptable.py`

## Usage

Copy files into:

```text
chapters/chapter_04_category_comparison/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_04_category_comparison/ch04_02_pointplot_ci_alternative.py
```
