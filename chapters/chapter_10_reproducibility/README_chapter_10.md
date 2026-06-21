# Chapter 10 Python files

RU:
Файлы главы 10 сгруппированы по подразделам: структура проекта, разделение данных/анализа/визуализации, seed и bootstrap, параметры запуска, проверка данных, metadata, версии среды, логирование и pipeline.

EN:
Chapter 10 files are grouped by subsections: project structure, separation of data/analysis/visualization, seed and bootstrap, runtime parameters, data validation, metadata, environment versions, logging, and pipeline.

## 10.1. Структура проекта и каталог данных

- `ch10_01_project_structure_audit.py`
- `ch10_01_data_catalog_summary.py`

## 10.2. Разделение данных, расчётов и визуализации

- `ch10_02_separate_data_analysis_visualization.py`
- `ch10_02_intermediate_outputs.py`

## 10.3. Seed, bootstrap and reproducibility

- `ch10_03_reproducible_random_seed.py`
- `ch10_03_bootstrap_ci_reproducible.py`

## 10.4. Параметры запуска и конфигурация

- `ch10_04_parameterized_script_cli.py`
- `ch10_04_config_dict_parameters.py`

## 10.5. Проверка входных данных

- `ch10_05_input_data_validation.py`
- `ch10_05_missing_values_report.py`

## 10.6. Metadata and environment versions

- `ch10_06_metadata_sidecar_json.py`
- `ch10_06_environment_versions_report.py`

## 10.7. Логирование и pipeline

- `ch10_07_logging_pipeline_steps.py`
- `ch10_07_minimal_make_like_pipeline.py`

## 10.8. Чек-лист воспроизводимости

- `ch10_08_reproducibility_checklist_table.py`

## Usage

Copy files into:

```text
chapters/chapter_10_reproducibility/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_10_reproducibility/ch10_07_minimal_make_like_pipeline.py
```
