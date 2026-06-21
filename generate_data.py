# generate_data.py
# Synthetic medical data generator for the scientific graphics handbook.
#
# Run from the project root:
#   uv run python generate_data.py
#
# The script creates all datasets needed for the handbook examples.
# It does not create figures and does not create chapter plotting scripts.
#
# Output:
#   data/processed/*.csv
#   data/processed/dataset_catalog.csv
#   data/processed/README_DATA.md

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ENCODING = "utf-8-sig"


@dataclass(frozen=True)
class DatasetInfo:
    filename: str
    title: str
    rows: int
    purpose: str
    main_columns: str


def sigmoid(x: np.ndarray | float) -> np.ndarray | float:
    return 1 / (1 + np.exp(-x))


def save_csv(df: pd.DataFrame, filename: str) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / filename
    df.to_csv(path, index=False, encoding=ENCODING)
    return path


def normal_clip(rng: np.random.Generator, mean: float, sd: float, size: int, low: float, high: float) -> np.ndarray:
    return rng.normal(mean, sd, size).clip(low, high)


def as_int(x: np.ndarray) -> np.ndarray:
    return np.rint(x).astype(int)


# ---------------------------------------------------------------------
# 1. Core cross-sectional clinical dataset
# ---------------------------------------------------------------------

def generate_clinical_cross_sectional(n: int = 450, seed: int = SEED) -> pd.DataFrame:
    """
    Main synthetic clinical dataset.

    Scenario: adults with elevated cardiovascular/metabolic risk randomized to
    Drug A, Drug B, or placebo. Values are plausible for teaching graphics,
    not for clinical inference.
    """
    rng = np.random.default_rng(seed)
    patient_id = np.arange(1, n + 1)

    age = normal_clip(rng, 58, 12, n, 25, 88)
    sex = rng.choice(["Мужской", "Женский"], size=n, p=[0.48, 0.52])
    group = rng.choice(["Препарат A", "Препарат B", "Плацебо"], size=n, p=[1 / 3, 1 / 3, 1 / 3])

    bmi = normal_clip(rng, 28.2, 4.6, n, 17.5, 44.5)
    waist = (44 + 1.65 * bmi + np.where(sex == "Мужской", 7, -1) + rng.normal(0, 6, n)).clip(62, 145)

    smoker = rng.binomial(1, np.where(sex == "Мужской", 0.29, 0.17))
    diabetes = rng.binomial(1, sigmoid(-5.6 + 0.045 * age + 0.10 * bmi))
    statin = rng.binomial(1, sigmoid(-2.3 + 0.025 * age + 0.75 * diabetes))

    group_effect_sbp = np.select(
        [group == "Препарат A", group == "Препарат B", group == "Плацебо"],
        [-13.0, -7.0, 0.0],
    )

    sbp = (91 + 0.47 * age + 0.78 * bmi + 5.0 * diabetes + 2.0 * smoker + group_effect_sbp + rng.normal(0, 9.0, n)).clip(95, 198)
    dbp = (52 + 0.16 * age + 0.48 * bmi + 1.8 * smoker + 0.28 * group_effect_sbp + rng.normal(0, 6.5, n)).clip(58, 118)
    heart_rate = (68 + 0.06 * age + 2.4 * smoker + 1.5 * diabetes + rng.normal(0, 8, n)).clip(48, 118)

    glucose = (4.25 + 0.075 * bmi + 1.15 * diabetes + rng.normal(0, 0.55, n)).clip(3.5, 13.5)
    hba1c = (4.9 + 0.06 * bmi + 1.35 * diabetes + rng.normal(0, 0.35, n)).clip(4.5, 11.5)
    ldl = (3.55 + 0.012 * age + 0.020 * bmi - 0.75 * statin + rng.normal(0, 0.65, n)).clip(1.0, 7.5)
    hdl = (1.35 - 0.012 * bmi + np.where(sex == "Женский", 0.18, 0.0) - 0.10 * smoker + rng.normal(0, 0.18, n)).clip(0.55, 2.25)

    triglycerides = rng.lognormal(
        mean=np.log(1.35 + 0.035 * (bmi - 25) + 0.25 * diabetes),
        sigma=0.42,
        size=n,
    ).clip(0.45, 7.8)

    creatinine = (np.where(sex == "Мужской", 84, 70) + 0.23 * age + 3.5 * diabetes + rng.normal(0, 12, n)).clip(42, 180)
    egfr = (112 - 0.82 * age - 0.32 * bmi - 5.5 * diabetes + rng.normal(0, 9, n)).clip(25, 125)
    crp = rng.lognormal(mean=1.0 + 0.018 * (bmi - 28) + 0.18 * smoker, sigma=0.78, size=n).clip(0.1, 85)

    risk_score = sigmoid(-8.0 + 0.055 * age + 0.018 * sbp + 0.33 * diabetes + 0.23 * smoker + 0.12 * ldl - 0.16 * hdl)
    complication_prob = sigmoid(-7.1 + 0.047 * age + 0.014 * sbp + 0.40 * diabetes + 0.030 * crp + 0.20 * smoker)
    complication = rng.binomial(1, complication_prob)

    disease_status = rng.binomial(1, sigmoid(-5.2 + 0.045 * age + 0.060 * crp + 0.55 * diabetes))
    diagnostic_marker = (18 + 8.2 * disease_status + 0.10 * age + 0.28 * crp + rng.normal(0, 6.5, n)).clip(3, 85)

    hypertension_stage = pd.cut(
        sbp,
        bins=[0, 129, 139, 159, 300],
        labels=["Нет/контроль", "Высокое нормальное", "АГ 1 степени", "АГ 2–3 степени"],
        right=True,
    ).astype(str)

    return pd.DataFrame(
        {
            "patient_id": patient_id,
            "age_years": as_int(age),
            "sex": sex,
            "therapy_group": group,
            "bmi_kg_m2": np.round(bmi, 1),
            "waist_cm": np.round(waist, 1),
            "smoker": smoker,
            "diabetes": diabetes,
            "statin_therapy": statin,
            "sbp_mm_hg": as_int(sbp),
            "dbp_mm_hg": as_int(dbp),
            "heart_rate_bpm": as_int(heart_rate),
            "glucose_mmol_l": np.round(glucose, 1),
            "hba1c_percent": np.round(hba1c, 1),
            "ldl_mmol_l": np.round(ldl, 2),
            "hdl_mmol_l": np.round(hdl, 2),
            "triglycerides_mmol_l": np.round(triglycerides, 2),
            "creatinine_umol_l": as_int(creatinine),
            "egfr_ml_min_1_73m2": as_int(egfr),
            "crp_mg_l": np.round(crp, 1),
            "risk_score": np.round(risk_score, 3),
            "complication": complication,
            "complication_probability": np.round(complication_prob, 3),
            "disease_status": disease_status,
            "diagnostic_marker": np.round(diagnostic_marker, 1),
            "hypertension_stage": hypertension_stage,
        }
    )


def generate_small_sample_dataset(df_main: pd.DataFrame, seed: int = SEED + 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parts = []
    for group, group_df in df_main.groupby("therapy_group", sort=False):
        sample = group_df.sample(n=12, random_state=int(rng.integers(1, 1_000_000)))
        parts.append(sample)
    return pd.concat(parts, ignore_index=True).sort_values(["therapy_group", "patient_id"]).reset_index(drop=True)


# ---------------------------------------------------------------------
# 2. Longitudinal data
# ---------------------------------------------------------------------

def generate_longitudinal_bp(n_patients: int = 180, seed: int = SEED + 2) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    patient_id = np.arange(1, n_patients + 1)
    group = rng.choice(["Препарат A", "Препарат B", "Плацебо"], size=n_patients, p=[1/3, 1/3, 1/3])
    age = normal_clip(rng, 59, 11, n_patients, 30, 86)
    bmi = normal_clip(rng, 28.5, 4.5, n_patients, 18, 43)
    baseline = (130 + 0.30 * age + 0.55 * bmi + rng.normal(0, 9, n_patients)).clip(125, 190)
    weeks = np.array([0, 2, 4, 8, 12, 16, 20, 24])

    rows = []
    for i in range(n_patients):
        random_intercept = rng.normal(0, 5)
        for week in weeks:
            if group[i] == "Препарат A":
                expected_change = -17 * (1 - math.exp(-week / 7.5))
            elif group[i] == "Препарат B":
                expected_change = -10 * (1 - math.exp(-week / 8.5))
            else:
                expected_change = -3.5 * (1 - math.exp(-week / 10.0))
            sbp = baseline[i] + expected_change + random_intercept + rng.normal(0, 5.5)
            rows.append(
                {
                    "patient_id": int(patient_id[i]),
                    "therapy_group": group[i],
                    "week": int(week),
                    "age_years": int(round(age[i])),
                    "bmi_kg_m2": round(float(bmi[i]), 1),
                    "sbp_mm_hg": int(round(np.clip(sbp, 95, 200))),
                    "adherence": rng.choice(["Высокая", "Средняя", "Низкая"], p=[0.64, 0.26, 0.10]),
                }
            )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------
# 3. Survival / Kaplan-Meier data
# ---------------------------------------------------------------------

def generate_survival_dataset(n: int = 420, seed: int = SEED + 3) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    patient_id = np.arange(1, n + 1)
    group = rng.choice(["Стандартная терапия", "Интенсивная терапия"], size=n, p=[0.5, 0.5])
    age = normal_clip(rng, 62, 10, n, 35, 88)
    diabetes = rng.binomial(1, sigmoid(-4.4 + 0.04 * age))
    egfr = (105 - 0.75 * age - 7.5 * diabetes + rng.normal(0, 10, n)).clip(25, 120)

    shape = 1.35
    baseline_scale = 32.0
    risk_multiplier = np.exp(0.030 * (age - 62) + 0.38 * diabetes - 0.010 * (egfr - 70) + np.where(group == "Интенсивная терапия", -0.36, 0.0))
    u = rng.uniform(size=n)
    event_time = baseline_scale * (-np.log(u) / risk_multiplier) ** (1 / shape)
    censor_time = rng.uniform(18, 36, size=n)
    observed_time = np.minimum(event_time, censor_time)
    event = (event_time <= censor_time).astype(int)

    return pd.DataFrame(
        {
            "patient_id": patient_id,
            "therapy_group": group,
            "age_years": as_int(age),
            "diabetes": diabetes,
            "egfr_ml_min_1_73m2": as_int(egfr),
            "time_months": np.round(observed_time, 1),
            "event": event,
            "censored": 1 - event,
        }
    )


# ---------------------------------------------------------------------
# 4. Diagnostic ROC data
# ---------------------------------------------------------------------

def generate_diagnostic_roc_dataset(n: int = 520, seed: int = SEED + 4) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    patient_id = np.arange(1, n + 1)
    age = normal_clip(rng, 55, 16, n, 18, 90)
    sex = rng.choice(["Мужской", "Женский"], size=n, p=[0.47, 0.53])
    disease = rng.binomial(1, sigmoid(-3.9 + 0.035 * age))

    crp = rng.lognormal(mean=np.where(disease == 1, 2.55, 1.15), sigma=np.where(disease == 1, 0.65, 0.75), size=n).clip(0.1, 160)
    neutrophils = (3.4 + 2.2 * disease + 0.025 * crp + rng.normal(0, 1.05, n)).clip(1.0, 18)
    biomarker_score = -2.4 + 0.045 * age + 0.030 * crp + 0.35 * neutrophils + rng.normal(0, 1.15, n)
    predicted_probability = sigmoid(biomarker_score)

    return pd.DataFrame(
        {
            "patient_id": patient_id,
            "age_years": as_int(age),
            "sex": sex,
            "disease_status": disease,
            "crp_mg_l": np.round(crp, 1),
            "neutrophils_10e9_l": np.round(neutrophils, 1),
            "biomarker_score": np.round(biomarker_score, 3),
            "predicted_probability": np.round(predicted_probability, 3),
        }
    )


# ---------------------------------------------------------------------
# 5. Bland-Altman agreement data
# ---------------------------------------------------------------------

def generate_bland_altman_dataset(n: int = 140, seed: int = SEED + 5) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    patient_id = np.arange(1, n + 1)
    true_sbp = normal_clip(rng, 136, 18, n, 95, 190)
    manual = true_sbp + rng.normal(0, 3.5, n)
    automated = true_sbp + 2.8 + 0.035 * (true_sbp - 135) + rng.normal(0, 6.0, n)
    mean_measurement = (manual + automated) / 2
    difference = automated - manual
    return pd.DataFrame(
        {
            "patient_id": patient_id,
            "manual_sbp_mm_hg": np.round(manual, 1),
            "automated_sbp_mm_hg": np.round(automated, 1),
            "mean_sbp_mm_hg": np.round(mean_measurement, 1),
            "difference_auto_minus_manual_mm_hg": np.round(difference, 1),
        }
    )


# ---------------------------------------------------------------------
# 6. Forest plot meta-analysis data
# ---------------------------------------------------------------------

def generate_forest_meta_dataset(seed: int = SEED + 6) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    studies = [
        "Ivanov 2017", "Petrova 2018", "Sokolov 2019", "Mikhailova 2020", "Kim 2020",
        "Garcia 2021", "Chen 2021", "Smith 2022", "Rahman 2023", "Novak 2024",
    ]
    rows = []
    for study in studies:
        n_treat = int(rng.integers(95, 420))
        n_control = int(rng.integers(95, 420))
        baseline_risk = rng.uniform(0.10, 0.28)
        true_rr = rng.lognormal(mean=np.log(0.78), sigma=0.18)
        events_control = int(rng.binomial(n_control, baseline_risk))
        events_treat = int(rng.binomial(n_treat, np.clip(baseline_risk * true_rr, 0.03, 0.45)))

        a = events_treat + 0.5
        b = n_treat - events_treat + 0.5
        c = events_control + 0.5
        d = n_control - events_control + 0.5
        rr = (a / (a + b)) / (c / (c + d))
        log_rr = math.log(rr)
        se = math.sqrt((1 / a) - (1 / (a + b)) + (1 / c) - (1 / (c + d)))
        ci_low = math.exp(log_rr - 1.96 * se)
        ci_high = math.exp(log_rr + 1.96 * se)
        weight_raw = 1 / (se**2)
        rows.append(
            {
                "study": study,
                "n_treatment": n_treat,
                "events_treatment": events_treat,
                "n_control": n_control,
                "events_control": events_control,
                "risk_ratio": round(rr, 3),
                "ci_low": round(ci_low, 3),
                "ci_high": round(ci_high, 3),
                "log_risk_ratio": round(log_rr, 4),
                "se_log_risk_ratio": round(se, 4),
                "weight_raw": round(weight_raw, 3),
            }
        )
    df = pd.DataFrame(rows)
    df["weight_percent"] = np.round(100 * df["weight_raw"] / df["weight_raw"].sum(), 1)
    return df.drop(columns=["weight_raw"])


# ---------------------------------------------------------------------
# 7. CONSORT flow data
# ---------------------------------------------------------------------

def generate_consort_flow_dataset() -> pd.DataFrame:
    rows = [
        {"stage": "Оценены на соответствие", "group": "Все участники", "n": 820, "reason": ""},
        {"stage": "Исключены", "group": "Все участники", "n": 340, "reason": "Не соответствовали критериям — 210; отказались — 88; другие причины — 42"},
        {"stage": "Рандомизированы", "group": "Все участники", "n": 480, "reason": ""},
        {"stage": "Назначены на Препарат A", "group": "Препарат A", "n": 240, "reason": ""},
        {"stage": "Назначены на Плацебо", "group": "Плацебо", "n": 240, "reason": ""},
        {"stage": "Получили вмешательство", "group": "Препарат A", "n": 232, "reason": "Не начали лечение — 8"},
        {"stage": "Получили вмешательство", "group": "Плацебо", "n": 235, "reason": "Не начали лечение — 5"},
        {"stage": "Потеряны для наблюдения", "group": "Препарат A", "n": 14, "reason": "Переезд — 5; отзыв согласия — 6; иное — 3"},
        {"stage": "Потеряны для наблюдения", "group": "Плацебо", "n": 19, "reason": "Переезд — 8; отзыв согласия — 7; иное — 4"},
        {"stage": "Завершили наблюдение", "group": "Препарат A", "n": 218, "reason": ""},
        {"stage": "Завершили наблюдение", "group": "Плацебо", "n": 216, "reason": ""},
        {"stage": "Включены в анализ", "group": "Препарат A", "n": 236, "reason": "Анализ intention-to-treat"},
        {"stage": "Включены в анализ", "group": "Плацебо", "n": 238, "reason": "Анализ intention-to-treat"},
    ]
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------
# 8. Anscombe quartet
# ---------------------------------------------------------------------

def generate_anscombe_dataset() -> pd.DataFrame:
    data = {
        "x1": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
        "y1": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68],
        "x2": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
        "y2": [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
        "x3": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
        "y3": [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73],
        "x4": [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
        "y4": [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89],
    }
    wide = pd.DataFrame(data)
    rows = []
    for i in range(1, 5):
        for obs_id, (x, y) in enumerate(zip(wide[f"x{i}"], wide[f"y{i}"]), start=1):
            rows.append({"dataset": f"Набор {i}", "observation_id": obs_id, "x": x, "y": y})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------
# 9. Categorical composition and log-scale laboratory data
# ---------------------------------------------------------------------

def generate_categorical_composition_dataset(seed: int = SEED + 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    departments = ["Кардиология", "Эндокринология", "Терапия", "Неврология"]
    severity = ["Лёгкая", "Средняя", "Тяжёлая"]
    base_probs = {
        "Кардиология": [0.28, 0.50, 0.22],
        "Эндокринология": [0.35, 0.47, 0.18],
        "Терапия": [0.43, 0.42, 0.15],
        "Неврология": [0.31, 0.46, 0.23],
    }
    for dep in departments:
        total = int(rng.integers(120, 260))
        counts = rng.multinomial(total, base_probs[dep])
        for sev, count in zip(severity, counts):
            rows.append({"department": dep, "severity": sev, "n": int(count), "total_department": total, "percent": round(100 * count / total, 1)})
    return pd.DataFrame(rows)


def generate_lab_logscale_dataset(seed: int = SEED + 8) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = 360
    patient_id = np.arange(1, n + 1)
    disease_group = rng.choice(["Контроль", "Умеренное воспаление", "Выраженное воспаление"], size=n, p=[0.35, 0.40, 0.25])
    crp = np.empty(n)
    ferritin = np.empty(n)
    d_dimer = np.empty(n)
    for i, group in enumerate(disease_group):
        if group == "Контроль":
            crp[i] = rng.lognormal(np.log(1.6), 0.55)
            ferritin[i] = rng.lognormal(np.log(95), 0.45)
            d_dimer[i] = rng.lognormal(np.log(230), 0.38)
        elif group == "Умеренное воспаление":
            crp[i] = rng.lognormal(np.log(12), 0.70)
            ferritin[i] = rng.lognormal(np.log(230), 0.55)
            d_dimer[i] = rng.lognormal(np.log(480), 0.45)
        else:
            crp[i] = rng.lognormal(np.log(55), 0.75)
            ferritin[i] = rng.lognormal(np.log(650), 0.70)
            d_dimer[i] = rng.lognormal(np.log(1100), 0.60)
    return pd.DataFrame(
        {
            "patient_id": patient_id,
            "disease_group": disease_group,
            "crp_mg_l": np.round(crp.clip(0.1, 250), 1),
            "ferritin_ng_ml": np.round(ferritin.clip(15, 4000), 0).astype(int),
            "d_dimer_ng_ml": np.round(d_dimer.clip(80, 8000), 0).astype(int),
        }
    )


# ---------------------------------------------------------------------
# 10. Controlled correlated multivariate data
# ---------------------------------------------------------------------

def generate_correlated_multivariate_dataset(seed: int = SEED + 9) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = 300
    means = np.array([58, 28, 136, 5.9, 3.7])
    sds = np.array([12, 4.5, 17, 1.2, 0.9])
    corr = np.array(
        [
            [1.00, 0.22, 0.45, 0.20, 0.24],
            [0.22, 1.00, 0.42, 0.48, 0.28],
            [0.45, 0.42, 1.00, 0.30, 0.22],
            [0.20, 0.48, 0.30, 1.00, 0.18],
            [0.24, 0.28, 0.22, 0.18, 1.00],
        ]
    )
    cov = corr * np.outer(sds, sds)
    x = rng.multivariate_normal(means, cov, size=n)
    df = pd.DataFrame(x, columns=["age_years", "bmi_kg_m2", "sbp_mm_hg", "glucose_mmol_l", "ldl_mmol_l"])
    df["patient_id"] = np.arange(1, n + 1)
    df["age_years"] = df["age_years"].clip(25, 88).round().astype(int)
    df["bmi_kg_m2"] = df["bmi_kg_m2"].clip(17.5, 44).round(1)
    df["sbp_mm_hg"] = df["sbp_mm_hg"].clip(95, 190).round().astype(int)
    df["glucose_mmol_l"] = df["glucose_mmol_l"].clip(3.5, 12.5).round(1)
    df["ldl_mmol_l"] = df["ldl_mmol_l"].clip(1.0, 7.5).round(2)
    return df[["patient_id", "age_years", "bmi_kg_m2", "sbp_mm_hg", "glucose_mmol_l", "ldl_mmol_l"]]


# ---------------------------------------------------------------------
# 11. Figure quality checklist data
# ---------------------------------------------------------------------

def generate_figure_checklist_dataset() -> pd.DataFrame:
    checks = [
        ("axis_labels_present", "Есть подписи обеих осей", "readability", 1),
        ("units_present", "Указаны единицы измерения", "scientific_validity", 1),
        ("sample_size_visible", "Указан объём выборки", "scientific_validity", 1),
        ("uncertainty_shown", "Показана неопределённость/вариабельность", "scientific_validity", 1),
        ("legend_not_overlapping", "Легенда не перекрывает данные", "readability", 1),
        ("colorblind_safe", "Палитра безопасна для нарушений цветовосприятия", "accessibility", 1),
        ("not_3d", "Нет декоративной 3D-графики", "integrity", 1),
        ("bar_axis_starts_zero", "Ось столбчатой диаграммы начинается с нуля", "integrity", 1),
        ("caption_self_contained", "Подпись к рисунку самодостаточна", "reporting", 1),
        ("high_resolution_export", "Файл сохранён в публикационном качестве", "technical", 1),
    ]
    return pd.DataFrame(checks, columns=["check_id", "check_description", "domain", "required"])


# ---------------------------------------------------------------------
# Catalog and docs
# ---------------------------------------------------------------------

def build_catalog(infos: list[DatasetInfo]) -> pd.DataFrame:
    return pd.DataFrame([info.__dict__ for info in infos])


def write_readme(catalog: pd.DataFrame) -> None:
    lines = [
        "# Synthetic datasets",
        "",
        "These files are synthetic educational datasets for the scientific graphics handbook.",
        "They are not real patient data and must not be used for clinical inference.",
        "",
        "Generated by:",
        "",
        "```powershell",
        "uv run python generate_data.py",
        "```",
        "",
        "## Files",
        "",
    ]
    for _, row in catalog.iterrows():
        lines.extend(
            [
                f"### `{row['filename']}`",
                "",
                f"- **Purpose:** {row['purpose']}",
                f"- **Rows:** {row['rows']}",
                f"- **Main columns:** {row['main_columns']}",
                "",
            ]
        )
    (PROCESSED_DIR / "README_DATA.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating synthetic medical datasets...")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Output directory: {PROCESSED_DIR}")
    print(f"Seed: {SEED}\n")

    infos: list[DatasetInfo] = []

    clinical = generate_clinical_cross_sectional()
    save_csv(clinical, "clinical_cross_sectional.csv")
    infos.append(DatasetInfo("clinical_cross_sectional.csv", "Core cross-sectional clinical dataset", len(clinical), "Main dataset for distributions, boxplots, grouped comparisons, correlations, regression, and basic ROC examples.", ", ".join(clinical.columns[:10]) + ", ..."))

    small = generate_small_sample_dataset(clinical)
    save_csv(small, "small_sample_individual_points.csv")
    infos.append(DatasetInfo("small_sample_individual_points.csv", "Small-sample clinical dataset", len(small), "Small-n examples where individual observations should be shown with strip/swarm plots.", ", ".join(small.columns[:10]) + ", ..."))

    longitudinal = generate_longitudinal_bp()
    save_csv(longitudinal, "longitudinal_blood_pressure.csv")
    infos.append(DatasetInfo("longitudinal_blood_pressure.csv", "Longitudinal blood pressure follow-up", len(longitudinal), "Time series and repeated-measures figures; treatment response trajectories.", ", ".join(longitudinal.columns)))

    survival = generate_survival_dataset()
    save_csv(survival, "survival_kaplan_meier.csv")
    infos.append(DatasetInfo("survival_kaplan_meier.csv", "Survival / time-to-event dataset", len(survival), "Kaplan-Meier curves, censoring marks, risk tables, and log-rank-style examples.", ", ".join(survival.columns)))

    roc = generate_diagnostic_roc_dataset()
    save_csv(roc, "diagnostic_roc.csv")
    infos.append(DatasetInfo("diagnostic_roc.csv", "Diagnostic ROC dataset", len(roc), "ROC curves, AUC, thresholds, sensitivity and specificity examples.", ", ".join(roc.columns)))

    bland = generate_bland_altman_dataset()
    save_csv(bland, "bland_altman_agreement.csv")
    infos.append(DatasetInfo("bland_altman_agreement.csv", "Bland-Altman agreement dataset", len(bland), "Agreement between two measurement methods.", ", ".join(bland.columns)))

    forest = generate_forest_meta_dataset()
    save_csv(forest, "forest_meta_analysis.csv")
    infos.append(DatasetInfo("forest_meta_analysis.csv", "Forest plot meta-analysis dataset", len(forest), "Study-level relative risks, confidence intervals and weights for forest plots.", ", ".join(forest.columns)))

    consort = generate_consort_flow_dataset()
    save_csv(consort, "consort_flow.csv")
    infos.append(DatasetInfo("consort_flow.csv", "CONSORT participant flow dataset", len(consort), "CONSORT flow diagrams and consistency checks for randomized trials.", ", ".join(consort.columns)))

    anscombe = generate_anscombe_dataset()
    save_csv(anscombe, "anscombe_quartet.csv")
    infos.append(DatasetInfo("anscombe_quartet.csv", "Anscombe quartet", len(anscombe), "Demonstrating why summary statistics do not replace visualization.", ", ".join(anscombe.columns)))

    categorical = generate_categorical_composition_dataset()
    save_csv(categorical, "categorical_composition.csv")
    infos.append(DatasetInfo("categorical_composition.csv", "Categorical composition dataset", len(categorical), "Grouped and normalized bar charts; categorical proportions by department.", ", ".join(categorical.columns)))

    logscale = generate_lab_logscale_dataset()
    save_csv(logscale, "lab_values_logscale.csv")
    infos.append(DatasetInfo("lab_values_logscale.csv", "Right-skewed laboratory values", len(logscale), "Histograms, KDE, violin/box plots, and logarithmic axis examples.", ", ".join(logscale.columns)))

    correlated = generate_correlated_multivariate_dataset()
    save_csv(correlated, "correlated_multivariate.csv")
    infos.append(DatasetInfo("correlated_multivariate.csv", "Controlled correlated multivariate dataset", len(correlated), "Scatter matrices and correlation heatmaps with a known correlation structure.", ", ".join(correlated.columns)))

    checklist = generate_figure_checklist_dataset()
    save_csv(checklist, "figure_quality_checklist.csv")
    infos.append(DatasetInfo("figure_quality_checklist.csv", "Figure quality checklist dataset", len(checklist), "Chapter 12 automated/checklist-style figure-quality examples.", ", ".join(checklist.columns)))

    catalog = build_catalog(infos)
    save_csv(catalog, "dataset_catalog.csv")
    write_readme(catalog)

    metadata = {"seed": SEED, "generator": "generate_data.py", "synthetic": True, "datasets": [info.__dict__ for info in infos]}
    (PROCESSED_DIR / "dataset_catalog.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Done.\n")
    print("Created datasets:")
    for info in infos:
        print(f"  - data/processed/{info.filename} ({info.rows} rows)")
    print("\nCatalog:")
    print("  - data/processed/dataset_catalog.csv")
    print("  - data/processed/dataset_catalog.json")
    print("  - data/processed/README_DATA.md")


if __name__ == "__main__":
    main()
