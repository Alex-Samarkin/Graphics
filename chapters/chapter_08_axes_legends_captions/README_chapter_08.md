# Chapter 08 Python files

RU:
Файлы главы 8 сгруппированы по подразделам: подписи осей и единицы, шкалы и клинические пороги, легенды, подписи к рисункам, аннотации, многопанельные рисунки и шаблон подписи/экспорта.

EN:
Chapter 8 files are grouped by subsections: axis labels and units, scales and clinical thresholds, legends, captions, annotations, multi-panel figures, and caption/export template.

## 8.1. Оси, единицы, деления

- `ch08_01_axis_labels_units_bad_good.py`
- `ch08_01_tick_formatting_readability.py`

## 8.2. Шкалы и клинические пороги

- `ch08_02_linear_vs_log_axis.py`
- `ch08_02_clinical_threshold_axis_annotation.py`

## 8.3. Легенды и прямые подписи

- `ch08_03_legend_inside_outside.py`
- `ch08_03_direct_labeling_vs_legend.py`

## 8.4. Заголовок и подпись к рисунку

- `ch08_04_title_vs_caption.py`
- `ch08_04_caption_self_contained.py`

## 8.5. Аннотации и статистические подписи

- `ch08_05_annotation_overload.py`
- `ch08_05_statistical_annotation.py`

## 8.6. Многопанельные рисунки

- `ch08_06_panel_labels.py`
- `ch08_06_aligned_axes_multi_panel.py`

## 8.7. Шаблон подписи и экспорта

- `ch08_07_export_caption_template.py`

## Usage

Copy files into:

```text
chapters/chapter_08_axes_legends_captions/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_08_axes_legends_captions/ch08_01_axis_labels_units_bad_good.py
```
