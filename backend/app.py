"""Flask API for Random Forest mental-health predictions."""
import logging
import sys
from functools import wraps
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config
from models.predict_model import registry as model_registry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

REQUIRED_FIELDS = [
    "age",
    "gender",
    "occupation",
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
VALID_GENDERS = {"Female", "Male", "Non-binary"}
VALID_OCCUPATIONS = {
    "Student",
    "Working Professional",
    "Both (Part-time work + Study)",
}
NUMERIC_RANGES = {
    "age": (1, 120),
    "sleep_hours": (0, 24),
    "sleep_quality": (1, 10),
    "social_media_hours": (0, 24),
    "academic_work_pressure": (0, 10),
    "physical_activity_days": (0, 7),
    "stress_level": (0, 10),
    "anxiety_score": (0, 10),
    "depression_score": (0, 10),
    "work_life_balance": (0, 10),
    "mood_score": (0, 10),
    "concentration_level": (0, 10),
    "social_support": (0, 10),
}


def success_response(data: dict[str, Any], status: int = 200):
    return jsonify({"success": True, "data": data}), status


def error_response(message: str, status: int = 400, details: Any = None):
    body = {"success": False, "error": message}
    if details:
        body["details"] = details
    return jsonify(body), status


def handle_exceptions(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except Exception as exc:
            logger.exception("Unhandled exception in %s", view.__name__)
            return error_response(
                "An unexpected server error occurred.", 500, str(exc)
            )

    return wrapped


def validate_prediction(payload: dict) -> list[str]:
    errors = [
        f"Field '{field}' is required."
        for field in REQUIRED_FIELDS
        if field not in payload or payload[field] is None or payload[field] == ""
    ]
    if errors:
        return errors

    gender = str(payload["gender"])
    occupation = str(payload["occupation"])
    if gender not in VALID_GENDERS:
        errors.append(
            f"Invalid gender '{gender}'. Must be one of {sorted(VALID_GENDERS)}."
        )
    if occupation not in VALID_OCCUPATIONS:
        errors.append(f"Invalid occupation '{occupation}'.")

    for field, (minimum, maximum) in NUMERIC_RANGES.items():
        try:
            value = float(payload[field])
            if not minimum <= value <= maximum:
                errors.append(
                    f"'{field}' must be between {minimum} and {maximum}."
                )
        except (TypeError, ValueError):
            errors.append(f"'{field}' must be a number.")

    return errors


def create_app(cfg: Config = None) -> Flask:
    """Create the API, load model artifacts, and register prediction routes."""
    if cfg is None:
        cfg = Config()

    app = Flask(__name__)
    app.config.from_object(cfg)
    CORS(app, origins=cfg.CORS_ORIGINS, supports_credentials=True)

    try:
        model_registry.load(cfg.MODELS_DIR, cfg)
    except RuntimeError as exc:
        logger.error("%s", exc)
        logger.error("Prediction endpoints will be unavailable until models are trained.")

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "ok",
            "service": "Mental Health Prediction API",
            "models_loaded": model_registry.is_loaded(),
            "version": "1.0.0",
        })

    @app.route("/api/model-info", methods=["GET"])
    @handle_exceptions
    def model_info():
        if not model_registry.metrics:
            return error_response(
                "Model metrics not found. Ensure models have been trained.", 404
            )
        return success_response(model_registry.metrics)

    @app.route("/api/predict", methods=["POST"])
    @handle_exceptions
    def predict():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or not payload:
            return error_response("Request body must be valid JSON.", 400)

        validation_errors = validate_prediction(payload)
        if validation_errors:
            return error_response("Validation failed.", 422, validation_errors)

        logger.info(
            "Prediction request received for age=%s gender=%s",
            payload.get("age"),
            payload.get("gender"),
        )
        result = model_registry.predict(payload)
        return success_response({
            "condition": result["condition"],
            "severity": result["severity"],
            "treatment": result["treatment"],
            "confidence": result["confidence"],
            "prediction_time": f"{result['prediction_ms']} ms",
        })

    @app.errorhandler(404)
    def not_found(_):
        return error_response("Endpoint not found.", 404)

    @app.errorhandler(405)
    def method_not_allowed(_):
        return error_response("Method not allowed.", 405)

    @app.errorhandler(500)
    def internal_error(_):
        return error_response("Internal server error.", 500)

    logger.info("Flask app created successfully.")
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"], debug=app.config["DEBUG"])
