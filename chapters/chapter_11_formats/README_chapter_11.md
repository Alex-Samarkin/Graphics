# Chapter 11 Python files

RU:
Файлы главы 11 сгруппированы по контекстам использования научной графики: статья, ВКР/диссертация, презентация, постер, отчёт, веб, печать и матрица выбора формата.

EN:
Chapter 11 files are grouped by scientific-graphics usage contexts: journal article, thesis/dissertation, presentation, poster, report, web, print, and format decision matrix.

## 11.1. Один результат — разные контексты

- `ch11_01_same_data_different_contexts.py`

## 11.2. Научная статья

- `ch11_02_journal_article_one_column.py`
- `ch11_02_journal_article_two_column.py`

## 11.3. ВКР, диссертация, квалификационная работа

- `ch11_03_thesis_figure_with_caption.py`
- `ch11_03_thesis_table_like_figure.py`

## 11.4. Презентация

- `ch11_04_presentation_slide_16x9.py`
- `ch11_04_presentation_before_after_simplification.py`

## 11.5. Постер

- `ch11_05_poster_large_format.py`
- `ch11_05_poster_three_panel_summary.py`

## 11.6. Отчёт / dashboard-style графика

- `ch11_06_report_dashboard_style.py`
- `ch11_06_management_report_horizontal_bars.py`

## 11.7. Веб и карточки

- `ch11_07_web_html_export.py`
- `ch11_07_responsive_square_card.py`

## 11.8. Печать и разрешение

- `ch11_08_print_grayscale_check.py`
- `ch11_08_low_resolution_warning.py`

## 11.9. Матрица выбора формата

- `ch11_09_format_decision_matrix.py`

## Usage

Copy files into:

```text
chapters/chapter_11_formats/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_11_formats/ch11_04_presentation_slide_16x9.py
```
