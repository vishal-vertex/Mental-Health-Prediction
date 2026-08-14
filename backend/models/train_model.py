"""
Model training script — run once before starting Flask.

Usage:
    python models/train_model.py

Trains three independent Random Forest classifiers:
    1. Mental Health Condition
    2. Severity
    3. Treatment

Saves all artifacts to backend/models/:
    condition_model.pkl
    severity_model.pkl
    treatment_model.pkl
    scaler.pkl
    label_encoders.pkl
    model_metrics.json
"""
import json
import logging
import os
import sys

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from models.preprocess import (
    ALL_FEATURES,
    TARGET_CONDITION,
    TARGET_SEVERITY,
    TARGET_TREATMENT,
    apply_imputers,
    clean_treatment_column,
    drop_target_nulls,
    encode_features,
    fit_imputers,
    fit_label_encoders,
    fit_scaler,
    load_raw_data,
    preprocess_features,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
TEST_SIZE = 0.2


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray, label_names: list) -> dict:
    """Return a dict of evaluation metrics for a fitted model."""
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=label_names, output_dict=True)
    cm = confusion_matrix(y_test, y_pred).tolist()

    return {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred, average="weighted", zero_division=0) * 100, 2),
        "recall": round(recall_score(y_test, y_pred, average="weighted", zero_division=0) * 100, 2),
        "f1_score": round(f1_score(y_test, y_pred, average="weighted", zero_division=0) * 100, 2),
        "confusion_matrix": cm,
        "labels": label_names,
        "classification_report": report,
    }


def train_rf_model(X_train, y_train) -> RandomForestClassifier:
    """Train a Random Forest classifier with sensible defaults."""
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)
    return model


def main():
    cfg = Config()
    models_dir = cfg.MODELS_DIR
    os.makedirs(models_dir, exist_ok=True)

    # ── 1. Load raw data ──────────────────────────────────────────
    logger.info("Loading dataset from: %s", cfg.DATASET_PATH)
    df = load_raw_data(cfg.DATASET_PATH)
    logger.info("Raw shape: %s", df.shape)

    # ── 2. Clean treatment column ──────────────────────────────────
    df = clean_treatment_column(df)
    df = drop_target_nulls(df)
    logger.info("After cleaning shape: %s", df.shape)

    # ── 3. Fit imputers on feature columns ─────────────────────────
    num_imputer, cat_imputer = fit_imputers(df)

    # ── 4. Apply imputation ────────────────────────────────────────
    df_imputed = apply_imputers(df, num_imputer, cat_imputer)

    # ── 5. Fit label encoders (features + targets) ─────────────────
    label_encoders = fit_label_encoders(df_imputed)

    # ── 6. Encode features ─────────────────────────────────────────
    df_encoded = encode_features(df_imputed, label_encoders)

    # ── 7. Fit scaler ──────────────────────────────────────────────
    scaler = fit_scaler(df_encoded)

    # ── 8. Build feature matrix ────────────────────────────────────
    X = preprocess_features(df_imputed, num_imputer, cat_imputer, label_encoders, scaler)

    # ── 9. Encode target vectors ───────────────────────────────────
    y_condition = label_encoders[TARGET_CONDITION].transform(df_imputed[TARGET_CONDITION].astype(str))
    y_severity  = label_encoders[TARGET_SEVERITY].transform(df_imputed[TARGET_SEVERITY].astype(str))
    y_treatment = label_encoders[TARGET_TREATMENT].transform(df_imputed[TARGET_TREATMENT].astype(str))

    # ── 10. Train / test split ─────────────────────────────────────
    X_tr, X_te, yc_tr, yc_te, ys_tr, ys_te, yt_tr, yt_te = train_test_split(
        X, y_condition, y_severity, y_treatment,
        test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_condition,
    )
    logger.info("Train: %d | Test: %d", len(X_tr), len(X_te))

    # ── 11. Model 1 – Condition ────────────────────────────────────
    logger.info("Training Model 1: Mental Health Condition …")
    condition_model = train_rf_model(X_tr, yc_tr)
    condition_labels = list(label_encoders[TARGET_CONDITION].classes_)
    condition_metrics = evaluate_model(condition_model, X_te, yc_te, condition_labels)
    logger.info("Condition Accuracy: %.2f%%", condition_metrics["accuracy"])

    # ── 12. Model 2 – Severity ─────────────────────────────────────
    logger.info("Training Model 2: Severity …")
    severity_model = train_rf_model(X_tr, ys_tr)
    severity_labels = list(label_encoders[TARGET_SEVERITY].classes_)
    severity_metrics = evaluate_model(severity_model, X_te, ys_te, severity_labels)
    logger.info("Severity Accuracy: %.2f%%", severity_metrics["accuracy"])

    # ── 13. Model 3 – Treatment ────────────────────────────────────
    logger.info("Training Model 3: Treatment …")
    treatment_model = train_rf_model(X_tr, yt_tr)
    treatment_labels = list(label_encoders[TARGET_TREATMENT].classes_)
    treatment_metrics = evaluate_model(treatment_model, X_te, yt_te, treatment_labels)
    logger.info("Treatment Accuracy: %.2f%%", treatment_metrics["accuracy"])

    # ── 14. Save artifacts ─────────────────────────────────────────
    # Attach imputers to the label_encoders dict so one file stores all
    artifacts = {
        "num_imputer": num_imputer,
        "cat_imputer": cat_imputer,
        **label_encoders,
    }

    joblib.dump(condition_model, os.path.join(models_dir, cfg.CONDITION_MODEL_FILE))
    joblib.dump(severity_model,  os.path.join(models_dir, cfg.SEVERITY_MODEL_FILE))
    joblib.dump(treatment_model, os.path.join(models_dir, cfg.TREATMENT_MODEL_FILE))
    joblib.dump(scaler,          os.path.join(models_dir, cfg.SCALER_FILE))
    joblib.dump(artifacts,       os.path.join(models_dir, cfg.LABEL_ENCODERS_FILE))

    metrics = {
        "condition": condition_metrics,
        "severity":  severity_metrics,
        "treatment": treatment_metrics,
    }
    with open(os.path.join(models_dir, cfg.METRICS_FILE), "w") as f:
        json.dump(metrics, f, indent=2)

    logger.info("All artifacts saved to: %s", models_dir)
    logger.info("=" * 50)
    logger.info("SUMMARY")
    logger.info("  Condition  — Accuracy: %.2f%% | F1: %.2f%%", condition_metrics["accuracy"], condition_metrics["f1_score"])
    logger.info("  Severity   — Accuracy: %.2f%% | F1: %.2f%%", severity_metrics["accuracy"],  severity_metrics["f1_score"])
    logger.info("  Treatment  — Accuracy: %.2f%% | F1: %.2f%%", treatment_metrics["accuracy"],  treatment_metrics["f1_score"])
    logger.info("=" * 50)
    logger.info("Training complete ✓")


if __name__ == "__main__":
    main()
