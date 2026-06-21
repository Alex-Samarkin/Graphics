# Chapter 02 Python files

RU:
Файлы главы 2 выделяют практические блоки из раздела "Подготовка рабочей среды": версии библиотек, стиль, объектно-ориентированный matplotlib, сохранение фигур, структура проекта, предварительный просмотр данных и воспроизводимость через seed.

EN:
Chapter 2 files separate the practical blocks from "Environment setup": library versions, style, object-oriented matplotlib, figure export, project structure, data preview, and seed-based reproducibility.

## Files

1. `ch02_01_check_environment_versions.py`
2. `ch02_02_default_vs_scientific_style.py`
3. `ch02_03_object_oriented_matplotlib.py`
4. `ch02_04_save_figure_formats.py`
5. `ch02_05_project_paths_and_data_loading.py`
6. `ch02_06_dataset_preview_clinical.py`
7. `ch02_07_reproducible_seed_demo.py`

## Usage

Copy files into:

```text
chapters/chapter_02_environment/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_02_environment/ch02_02_default_vs_scientific_style.py
```
