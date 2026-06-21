# Chapter 06 Python files

RU:
Файлы главы 6 сгруппированы по подразделам: восприятие цвета, типы палитр, проблема rainbow/jet, доступность и дальтонизм, практический выбор палитр, избыточное кодирование и единая цветовая схема.

EN:
Chapter 6 files are grouped by subsections: color perception, palette types, rainbow/jet problem, accessibility and color vision deficiency, practical palette choice, redundant encoding, and unified color schemes.

## 6.1. Восприятие цвета

- `ch06_01_luminance_and_contrast.py`

## 6.2. Типы палитр

- `ch06_02_palette_types_overview.py`
- `ch06_02_sequential_palette_for_magnitude.py`
- `ch06_02_diverging_palette_for_deviation.py`
- `ch06_02_qualitative_palette_for_groups.py`

## 6.3. Проблема rainbow/jet

- `ch06_03_jet_palette_problem.py`

## 6.4. Доступность: дальтонизм и чёрно-белая печать

- `ch06_04_colorblind_safe_vs_red_green.py`
- `ch06_04_double_encoding_lines_markers.py`
- `ch06_04_black_white_print_hatching.py`

## 6.5. Практический выбор палитр

- `ch06_05_practical_palette_selection.py`
- `ch06_05_consistent_palette_mapping.py`

## 6.6. Цвет как избыточное кодирование и единая схема

- `ch06_06_color_redundancy_not_overload.py`
- `ch06_06_unified_color_scheme_summary.py`

## Usage

Copy files into:

```text
chapters/chapter_06_color_palettes/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_06_color_palettes/ch06_03_jet_palette_problem.py
```
