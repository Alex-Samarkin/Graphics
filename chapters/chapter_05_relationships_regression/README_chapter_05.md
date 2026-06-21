# Chapter 05 Python files

RU:
Файлы главы 5 сгруппированы по подразделам: диаграммы рассеяния, корреляция и её ловушки, регрессия и доверительные полосы, матрицы связей и графики Бланда–Альтмана.

EN:
Chapter 5 files are grouped by subsections: scatter plots, correlation and its pitfalls, regression and confidence bands, relationship matrices, and Bland-Altman plots.

## 5.1. Диаграмма рассеяния

- `ch05_01_scatter_basic.py`
- `ch05_01_scatter_overlap_alpha_jitter.py`
- `ch05_01_scatter_encoding_extra_variables.py`

## 5.2. Корреляция и её визуализация

- `ch05_02_correlation_pearson_spearman.py`
- `ch05_02_anscombe_quartet.py`
- `ch05_02_confounding_by_group.py`

## 5.3. Регрессия, доверительные полосы, экстраполяция, LOWESS

- `ch05_03_regression_line_ci.py`
- `ch05_03_ci_vs_prediction_interval.py`
- `ch05_03_extrapolation_warning.py`
- `ch05_03_lowess_nonlinear.py`

## 5.4. Матрицы рассеяния и тепловые карты корреляций

- `ch05_04_pairplot_scatter_matrix.py`
- `ch05_04_correlation_heatmap.py`
- `ch05_04_multiple_correlation_pvalues.py`

## 5.5. График Бланда–Альтмана

- `ch05_05_bland_altman_basic.py`
- `ch05_05_bland_altman_proportional_bias.py`

## Usage

Copy files into:

```text
chapters/chapter_05_relationships_regression/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_05_relationships_regression/ch05_03_regression_line_ci.py
```
