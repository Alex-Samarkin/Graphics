# Chapter 09 Python files

RU:
Файлы главы 9 сгруппированы по подразделам: составные рисунки, GridSpec, общие оси/легенды/colorbar, размеры под статью и презентацию, форматы экспорта, подписи и layout.

EN:
Chapter 9 files are grouped by subsections: composite figures, GridSpec, shared axes/legends/colorbar, publication and presentation sizes, export formats, captions, and layout.

## 9.1. Составные рисунки и панели

- `ch09_01_basic_subplots_panel_figure.py`
- `ch09_01_panel_labels_consistency.py`

## 9.2. GridSpec и неравные панели

- `ch09_02_gridspec_unequal_panels.py`
- `ch09_02_nested_gridspec_risk_table.py`

## 9.3. Общие оси, легенды и colorbar

- `ch09_03_shared_axes_and_limits.py`
- `ch09_03_common_legend.py`
- `ch09_03_common_colorbar.py`

## 9.4. Размеры под статью и презентацию

- `ch09_04_publication_size_one_column.py`
- `ch09_04_publication_size_two_column.py`
- `ch09_04_presentation_16x9_export.py`

## 9.5. Экспорт и проверка файлов

- `ch09_05_export_formats_png_pdf_tiff_svg.py`
- `ch09_05_transparent_background_export.py`
- `ch09_05_export_file_size_check.py`

## 9.6. Layout, подписи и constrained_layout

- `ch09_06_layout_caption_space.py`
- `ch09_06_constrained_layout_demo.py`

## Usage

Copy files into:

```text
chapters/chapter_09_composite_export/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_09_composite_export/ch09_01_basic_subplots_panel_figure.py
```
