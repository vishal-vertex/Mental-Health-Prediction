"""
Preprocessing utilities shared between training and inference.
Defines feature columns, categorical features, numeric features,
and imputation/encoding helpers.
"""
import os
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ------------------------------------------------------------------
# Feature definitions
# ------------------------------------------------------------------
CATEGORICAL_FEATURES = ["gender", "occupation"]
NUMERIC_FEATURES = [
    "age",
    "sleep_hours",
    "sleep_quality",
    "social_media_hours",
    "academic_work_pressure",
    "physical_activity_days",
    "stress_level",
    "anxiety_score",
    "depression_score",
    "work_life_balance",
    "mood_score",
    "concentration_level",
    "social_support",
]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

TARGET_CONDITION = "mental_health_condition"
TARGET_SEVERITY = "severity"
TARGET_TREATMENT = "treatment"

# Shorten long treatment strings to a concise label used internally
TREATMENT_LABEL_MAP = {
    "No treatment needed; maintain healthy lifestyle and regular exercise": "Healthy Lifestyle",
    "Cognitive Behavioral Therapy (CBT), mindfulness, reduce caffeine, sleep hygiene": "CBT & Mindfulness",
    "Psychotherapy, antidepressants (SSRIs), regular exercise, social engagement": "Psychotherapy & SSRIs",
    "Rest, work-life balance improvement, therapy, reduce workload, meditation": "Rest & Therapy",
}

TREATMENT_REVERSE_MAP = {v: k for k, v in TREATMENT_LABEL_MAP.items()}


def load_raw_data(csv_path: str) -> pd.DataFrame:
    """Load the raw CSV file."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")
    return pd.read_csv(csv_path)


def clean_treatment_column(df: pd.DataFrame) -> pd.DataFrame:
    """Map verbose treatment strings to short labels."""
    df = df.copy()
    df[TARGET_TREATMENT] = df[TARGET_TREATMENT].str.strip()
    # Map to short label; unmapped values become NaN and drop
    df[TARGET_TREATMENT] = df[TARGET_TREATMENT].map(
        lambda x: next(
            (v for k, v in TREATMENT_LABEL_MAP.items() if k in str(x)),
            None,
        )
    )
    return df


def drop_target_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows where any target column is null."""
    return df.dropna(
        subset=[TARGET_CONDITION, TARGET_SEVERITY, TARGET_TREATMENT]
    ).reset_index(drop=True)


def fit_imputers(df: pd.DataFrame):
    """Fit and return (numeric_imputer, categorical_imputer)."""
    num_imputer = SimpleImputer(strategy="median")
    cat_imputer = SimpleImputer(strategy="most_frequent")
    num_imputer.fit(df[NUMERIC_FEATURES])
    cat_imputer.fit(df[CATEGORICAL_FEATURES])
    return num_imputer, cat_imputer


def apply_imputers(df: pd.DataFrame, num_imputer, cat_imputer) -> pd.DataFrame:
    """Apply pre-fitted imputers to features."""
    df = df.copy()
    df[NUMERIC_FEATURES] = num_imputer.transform(df[NUMERIC_FEATURES])
    df[CATEGORICAL_FEATURES] = cat_imputer.transform(df[CATEGORICAL_FEATURES])
    return df


def fit_label_encoders(df: pd.DataFrame) -> dict:
    """Fit a LabelEncoder per categorical feature and per target. Returns dict."""
    encoders = {}
    for col in CATEGORICAL_FEATURES + [TARGET_CONDITION, TARGET_SEVERITY, TARGET_TREATMENT]:
        le = LabelEncoder()
        le.fit(df[col].astype(str))
        encoders[col] = le
    return encoders


def encode_features(df: pd.DataFrame, encoders: dict) -> pd.DataFrame:
    """Label-encode categorical feature columns in-place."""
    df = df.copy()
    for col in CATEGORICAL_FEATURES:
        df[col] = encoders[col].transform(df[col].astype(str))
    return df


def fit_scaler(df: pd.DataFrame) -> StandardScaler:
    """Fit a StandardScaler on all feature columns."""
    scaler = StandardScaler()
    scaler.fit(df[ALL_FEATURES].values)
    return scaler


def preprocess_features(df: pd.DataFrame, num_imputer, cat_imputer, encoders: dict, scaler: StandardScaler) -> np.ndarray:
    """Full preprocessing pipeline for feature matrix X."""
    df = apply_imputers(df, num_imputer, cat_imputer)
    df = encode_features(df, encoders)
    return scaler.transform(df[ALL_FEATURES].values)


def preprocess_single_input(input_dict: dict, num_imputer, cat_imputer, encoders: dict, scaler: StandardScaler) -> np.ndarray:
    """
    Preprocess a single prediction request dict into a scaled feature vector.
    Unknown categories are mapped to the closest known value.
    """
    row = {}
    for col in NUMERIC_FEATURES:
        val = input_dict.get(col)
        row[col] = float(val) if val is not None else np.nan

    for col in CATEGORICAL_FEATURES:
        val = str(input_dict.get(col, ""))
        le = encoders[col]
        # Fallback to first known class if unseen
        row[col] = val if val in le.classes_ else le.classes_[0]

    df = pd.DataFrame([row])
    df[NUMERIC_FEATURES] = num_imputer.transform(df[NUMERIC_FEATURES])

    for col in CATEGORICAL_FEATURES:
        df[col] = encoders[col].transform(df[col].astype(str))

    return scaler.transform(df[ALL_FEATURES].values)
