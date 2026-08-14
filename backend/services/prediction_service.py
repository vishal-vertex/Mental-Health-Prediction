"""
Prediction service — orchestrates ML inference, recommendations, and Gemini.
Contains no Flask or routing code.
"""
import logging
from typing import Any

from models.predict_model import registry as model_registry
from services import gemini_service
from utils.recommendation_generator import get_recommendations

logger = logging.getLogger(__name__)


def generate_prediction(input_data: dict) -> dict[str, Any]:
    """
    Run the full prediction pipeline for a single input.

    Steps:
        1. Run three ML models → condition, severity, treatment, confidence
        2. Generate rule-based recommendations
        3. Request Gemini personalised suggestion
        4. Return assembled response dict

    Args:
        input_data: validated dict of 15 feature values

    Returns:
        dict with condition, severity, treatment, confidence,
             recommendations, gemini_suggestion, prediction_time
    """
    # ── Step 1: ML inference ───────────────────────────────────────
    result = model_registry.predict(input_data)

    condition      = result["condition"]
    severity       = result["severity"]
    treatment      = result["treatment"]
    confidence     = result["confidence"]
    prediction_ms  = result["prediction_ms"]

    # ── Step 2: Recommendations ────────────────────────────────────
    recommendations = get_recommendations(condition, severity)

    # ── Step 3: Gemini suggestion ──────────────────────────────────
    gemini_suggestion = gemini_service.get_gemini_suggestion(
        condition=condition,
        severity=severity,
        treatment=treatment,
        user_data=input_data,
        fallback_recommendations=recommendations,
    )

    return {
        "condition":        condition,
        "severity":         severity,
        "treatment":        treatment,
        "confidence":       confidence,
        "recommendations":  recommendations,
        "gemini_suggestion": gemini_suggestion,
        "prediction_time":  f"{prediction_ms} ms",
    }


def get_model_metrics() -> dict[str, Any]:
    """Return stored model evaluation metrics."""
    return model_registry.metrics
