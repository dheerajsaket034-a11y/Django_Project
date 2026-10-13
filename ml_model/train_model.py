"""
Train the term-deposit model.

Usage:
    python ml_model/train_model.py                      # synthetic demo data
    python ml_model/train_model.py path/to/bank-full.csv  # real UCI Bank Marketing data (sep=';')
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

OUT = Path(__file__).resolve().parent / "term_deposit_model.joblib"
NUM = ["age", "balance", "campaign", "pdays", "previous"]
CAT = ["job", "education", "housing", "loan", "contact", "poutcome"]
JOBS = ["admin.", "blue-collar", "entrepreneur", "housemaid", "management", "retired",
        "self-employed", "services", "student", "technician", "unemployed", "unknown"]


def synthetic(n=6000, seed=42):
    r = np.random.default_rng(seed)
    df = pd.DataFrame({
        "age": r.integers(18, 85, n),
        "job": r.choice(JOBS, n),
        "education": r.choice(["primary", "secondary", "tertiary", "unknown"], n, p=[.15, .5, .3, .05]),
        "balance": r.normal(1400, 2500, n).astype(int),
        "housing": r.choice(["yes", "no"], n),
        "loan": r.choice(["yes", "no"], n, p=[.2, .8]),
        "contact": r.choice(["cellular", "telephone", "unknown"], n, p=[.65, .1, .25]),
        "campaign": r.integers(1, 12, n),
        "pdays": np.where(r.random(n) < .75, -1, r.integers(1, 400, n)),
        "previous": r.integers(0, 6, n),
        "poutcome": r.choice(["success", "failure", "other", "unknown"], n, p=[.08, .12, .05, .75]),
    })
    z = (-2.2 + 0.0004 * df.balance + 0.015 * (df.age > 60) * (df.age - 60) / 10
         + 0.9 * df.job.isin(["student", "retired"]) + 0.4 * (df.education == "tertiary")
         - 0.6 * (df.housing == "yes") - 0.7 * (df.loan == "yes")
         + 0.5 * (df.contact == "cellular") - 0.8 * (df.contact == "unknown")
         + 2.3 * (df.poutcome == "success") - 0.08 * df.campaign)
    df["y"] = np.where(r.random(n) < 1 / (1 + np.exp(-z)), "yes", "no")
    return df


def main():
    if len(sys.argv) > 1:
        df = pd.read_csv(sys.argv[1], sep=";")
        print("Loaded real dataset:", df.shape)
    else:
        df = synthetic()
        print("No CSV given -> using synthetic demo data:", df.shape)

    X, y = df[NUM + CAT], (df["y"] == "yes").astype(int)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, stratify=y, random_state=42)

    pre = ColumnTransformer([
        ("num", StandardScaler(), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
    ])
    model = Pipeline([("pre", pre), ("clf", RandomForestClassifier(
        n_estimators=300, min_samples_leaf=3, class_weight="balanced", random_state=42, n_jobs=-1))])
    model.fit(Xtr, ytr)

    pred = model.predict(Xte)
    acc = accuracy_score(yte, pred)
    print(f"Accuracy: {acc:.3f}\n", classification_report(yte, pred, target_names=["No", "Yes"]))
    joblib.dump({"model": model, "accuracy": round(float(acc), 3)}, OUT)
    print("Saved ->", OUT)


if __name__ == "__main__":
    main()
