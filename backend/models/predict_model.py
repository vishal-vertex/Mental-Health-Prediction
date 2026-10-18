"""
Inference utilities — load saved models once and run predictions.
This module is imported by app.py.
Models are never re-trained here.
"""
import json
import logging
import os
import time
from typing import Any

import joblib
import numpy as np

from models.preprocess import (
    TARGET_CONDITION,
    TARGET_SEVERITY,
    TARGET_TREATMENT,
    TREATMENT_REVERSE_MAP,
    preprocess_single_input,
)

logger = logging.getLogger(__name__)


class ModelRegistry:
    """Holds all loaded model artifacts. Loaded once at Flask startup."""

    def __init__(self):
        self.condition_model = None
        self.severity_model  = None
        self.treatment_model = None
        self.scaler          = None
        self.label_encoders  = {}  # includes num/cat imputers
        self.metrics         = {}
        self._loaded         = False

    def load(self, models_dir: str, cfg) -> None:
        """Load all artifacts from disk. Call once at application startup."""
        if self._loaded:
            return

        try:
            self.condition_model = joblib.load(os.path.join(models_dir, cfg.CONDITION_MODEL_FILE))
            self.severity_model  = joblib.load(os.path.join(models_dir, cfg.SEVERITY_MODEL_FILE))
            self.treatment_model = joblib.load(os.path.join(models_dir, cfg.TREATMENT_MODEL_FILE))
            self.scaler          = joblib.load(os.path.join(models_dir, cfg.SCALER_FILE))
            self.label_encoders  = joblib.load(os.path.join(models_dir, cfg.LABEL_ENCODERS_FILE))

            metrics_path = os.path.join(models_dir, cfg.METRICS_FILE)
            if os.path.exists(metrics_path):
                with open(metrics_path) as f:
                    self.metrics = json.load(f)

            self._loaded = True
            logger.info("All models loaded successfully from %s", models_dir)
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"Required saved model artifacts were not found in {models_dir}.\n{exc}"
            ) from exc

    def is_loaded(self) -> bool:
        return self._loaded

    def predict(self, input_dict: dict) -> dict[str, Any]:
        """
        Run all three models on a single input dict.
        Returns:
            condition, severity, treatment, confidence, prediction_time
        """
        start = time.perf_counter()

        num_imputer = self.label_encoders["num_imputer"]
        cat_imputer = self.label_encoders["cat_imputer"]

        X = preprocess_single_input(
            input_dict, num_imputer, cat_imputer, self.label_encoders, self.scaler
        )

        # Condition
        condition_idx  = self.condition_model.predict(X)[0]
        condition_proba = self.condition_model.predict_proba(X)[0]
        condition       = self.label_encoders[TARGET_CONDITION].inverse_transform([condition_idx])[0]
        confidence      = round(float(np.max(condition_proba)) * 100, 1)

        # Severity
        severity_idx = self.severity_model.predict(X)[0]
        severity     = self.label_encoders[TARGET_SEVERITY].inverse_transform([severity_idx])[0]

        # Treatment (short label → verbose string)
        treatment_idx   = self.treatment_model.predict(X)[0]
        treatment_label = self.label_encoders[TARGET_TREATMENT].inverse_transform([treatment_idx])[0]
        treatment_full  = TREATMENT_REVERSE_MAP.get(treatment_label, treatment_label)

        elapsed = round((time.perf_counter() - start) * 1000, 1)

        return {
            "condition":       condition,
            "severity":        severity,
            "treatment":       treatment_full,
            "treatment_label": treatment_label,
            "confidence":      confidence,
            "prediction_ms":   elapsed,
        }


# Singleton — shared by the API app.
registry = ModelRegistry()
