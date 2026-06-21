# Chapter 07 Python files

RU:
Файлы главы 7 сгруппированы по подразделам специализированных медицинских графиков: ROC, Kaplan–Meier, forest plot, CONSORT, Bland–Altman, калибровка/decision curve, лабораторные пороги и индивидуальные траектории.

EN:
Chapter 7 files are grouped by specialized medical plot subsections: ROC, Kaplan-Meier, forest plot, CONSORT, Bland-Altman, calibration/decision curve, laboratory thresholds, and individual trajectories.

## 7.1. ROC, AUC, sensitivity/specificity

- `ch07_01_roc_curve_basic.py`
- `ch07_01_roc_threshold_annotations.py`
- `ch07_01_sensitivity_specificity_threshold.py`

## 7.2. Kaplan–Meier and survival curves

- `ch07_02_kaplan_meier_basic.py`
- `ch07_02_kaplan_meier_censoring.py`
- `ch07_02_kaplan_meier_risk_table_simple.py`
- `ch07_02_logrank_annotation.py`

## 7.3. Forest plot

- `ch07_03_forest_plot_basic.py`
- `ch07_03_forest_plot_weights.py`

## 7.4. CONSORT flow diagram

- `ch07_04_consort_flow_basic.py`
- `ch07_04_consort_flow_table.py`

## 7.5. Agreement: Bland–Altman

- `ch07_05_bland_altman_medical_agreement.py`

## 7.6. Calibration and decision curve

- `ch07_06_calibration_curve_basic.py`
- `ch07_06_decision_curve_analysis_simple.py`

## 7.7. Laboratory thresholds and longitudinal trajectories

- `ch07_07_lab_reference_interval_plot.py`
- `ch07_07_spaghetti_trajectory_plot.py`

## 7.8. Summary panel

- `ch07_08_special_plots_summary_panel.py`

## Usage

Copy files into:

```text
chapters/chapter_07_medical_special_plots/
```

Generate data first:

```powershell
uv run python generate_data.py
```

Run from project root:

```powershell
uv run python chapters/chapter_07_medical_special_plots/ch07_01_roc_curve_basic.py
```
