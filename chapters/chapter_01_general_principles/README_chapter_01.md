# Chapter 01 Python files

RU:
В исходной первой главе нет исполняемых Python-блоков: она содержит теоретические принципы и ASCII-схему анатомии графика. Поэтому этот комплект является предложенной правкой: ключевые тезисы главы 1 превращены в самостоятельные Python-файлы-иллюстрации.

EN:
The original Chapter 1 contains no executable Python blocks: it contains theoretical principles and an ASCII anatomy diagram. Therefore, this pack is a proposed correction: key Chapter 1 theses are converted into standalone Python figure scripts.

## Files

1. `ch01_01_chartjunk_vs_scientific_graph.py`
   - RU: научный график против декоративного графического мусора.
   - EN: scientific graph versus decorative chartjunk.

2. `ch01_02_anatomy_of_scientific_plot.py`
   - RU: анатомия научного графика: оси, единицы, легенда, SD, подпись.
   - EN: anatomy of a scientific plot: axes, units, legend, SD, caption.

3. `ch01_03_axis_truncation_warning.py`
   - RU: как обрезанная ось Y искажает столбчатую диаграмму.
   - EN: how a truncated Y-axis distorts a bar chart.

4. `ch01_04_variability_must_be_shown.py`
   - RU: почему нужно показывать вариабельность и индивидуальные наблюдения.
   - EN: why variability and individual observations should be shown.

5. `ch01_05_color_is_not_enough.py`
   - RU: цвет не должен быть единственным кодом различий.
   - EN: color should not be the only encoding of differences.

6. `ch01_06_publication_export_example.py`
   - RU: публикационный размер и экспорт PNG/PDF/TIFF.
   - EN: publication size and PNG/PDF/TIFF export.

## Usage

Copy the files into:

```text
chapters/chapter_01_general_principles/
```

Before running, generate datasets:

```powershell
uv run python generate_data.py
```

Run any file from the project root:

```powershell
uv run python chapters/chapter_01_general_principles/ch01_01_chartjunk_vs_scientific_graph.py
```
