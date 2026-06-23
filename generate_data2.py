import numpy as np
import pandas as pd

def generate_clinical_dataset(n=300, seed=42):
    """
    Генерирует реалистичный учебный клинический набор данных.

    Возвращает pandas.DataFrame со столбцами:
        age        — возраст, годы
        sex        — пол ('Мужской' / 'Женский')
        group      — группа терапии ('Препарат A' / 'Препарат B' / 'Плацебо')
        bmi        — индекс массы тела, кг/м^2
        sbp        — систолическое АД, мм рт. ст.
        glucose    — глюкоза крови натощак, ммоль/л
        crp        — С-реактивный белок, мг/л (асимметричное распределение)
        complication — наличие осложнения (0/1)
    """
    rng = np.random.default_rng(seed)

    # Возраст: нормальное распределение, ограниченное разумным диапазоном
    age = rng.normal(58, 12, n).clip(25, 90)

    # Пол
    sex = rng.choice(["Мужской", "Женский"], size=n, p=[0.48, 0.52])

    # Группа терапии (рандомизация примерно поровну)
    group = rng.choice(
        ["Препарат A", "Препарат B", "Плацебо"],
        size=n, p=[1/3, 1/3, 1/3]
    )

    # ИМТ: нормальное распределение
    bmi = rng.normal(27, 4, n).clip(16, 45)

    # Систолическое АД зависит от возраста и ИМТ + влияние группы терапии
    group_effect = np.select(
        [group == "Препарат A", group == "Препарат B", group == "Плацебо"],
        [-12, -7, 0]   # снижение АД относительно плацебо
    )
    sbp = (
        90
        + 0.45 * age           # вклад возраста
        + 0.8 * bmi            # вклад ИМТ
        + group_effect         # эффект терапии
        + rng.normal(0, 8, n)  # индивидуальная вариабельность
    ).clip(95, 200)

    # Глюкоза натощак: связана с ИМТ
    glucose = (4.0 + 0.07 * bmi + rng.normal(0, 0.6, n)).clip(3.5, 12)

    # С-реактивный белок: логнормальное (правосторонняя асимметрия)
    crp = rng.lognormal(mean=1.0, sigma=0.8, size=n).clip(0.1, 80)

    # Осложнение: вероятность растёт с возрастом и СРБ
    logit = -6 + 0.05 * age + 0.04 * crp
    p_compl = 1 / (1 + np.exp(-logit))
    complication = rng.binomial(1, p_compl)

    df = pd.DataFrame({
        "age": age.round(0).astype(int),
        "sex": sex,
        "group": group,
        "bmi": bmi.round(1),
        "sbp": sbp.round(0).astype(int),
        "glucose": glucose.round(1),
        "crp": crp.round(1),
        "complication": complication,
    })
    return df


# Создаём и осматриваем набор данных
df = generate_clinical_dataset()
print(df.head())
print("\nРазмер выборки:", len(df))
print(df.describe(include=[np.number]).round(1))

df.to_csv("data/processed/patients.csv", index=False, encoding="utf-8-sig")