"""
Blueprint: prediction routes.
Receives HTTP requests, validates input, delegates to prediction_service,
returns JSON responses. Contains NO ML or business logic.
"""
import logging

from flask import Blueprint, request

from services.prediction_service import generate_prediction, get_model_metrics
from utils.helper import (
    error_response,
    handle_exceptions,
    success_response,
    validate_predict_payload,
)

logger = logging.getLogger(__name__)

prediction_bp = Blueprint("prediction", __name__, url_prefix="/api")


@prediction_bp.route("/model-info", methods=["GET"])
@handle_exceptions
def model_info():
    """Return evaluation metrics for all three trained models."""
    metrics = get_model_metrics()
    if not metrics:
        return error_response("Model metrics not found. Ensure models have been trained.", 404)
    return success_response(metrics)


@prediction_bp.route("/predict", methods=["POST"])
@handle_exceptions
def predict():
    """
    Accept a JSON body with 15 mental-health features.
    Return condition, severity, treatment, confidence,
    recommendations, and Gemini suggestions.
    """
    payload = request.get_json(silent=True)

    if not payload:
        return error_response("Request body must be valid JSON.", 400)

    # Field-level validation
    validation_errors = validate_predict_payload(payload)
    if validation_errors:
        return error_response("Validation failed.", 422, validation_errors)

    logger.info("Prediction request received for age=%s gender=%s", payload.get("age"), payload.get("gender"))

    result = generate_prediction(payload)
    return success_response(result)
