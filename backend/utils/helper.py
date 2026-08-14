"""
General helper utilities: request validation, response formatting,
and error handler wrappers.
"""
import logging
from functools import wraps
from typing import Any

from flask import jsonify, request

logger = logging.getLogger(__name__)

REQUIRED_PREDICT_FIELDS = [
    "age", "gender", "occupation", "sleep_hours", "sleep_quality",
    "social_media_hours", "academic_work_pressure", "physical_activity_days",
    "stress_level", "anxiety_score", "depression_score",
    "work_life_balance", "mood_score", "concentration_level", "social_support",
]

VALID_GENDERS     = {"Female", "Male", "Non-binary"}
VALID_OCCUPATIONS = {"Student", "Working Professional", "Both (Part-time work + Study)"}


def success_response(data: dict[str, Any], status: int = 200):
    """Wrap data in a standard success envelope."""
    return jsonify({"success": True, "data": data}), status


def error_response(message: str, status: int = 400, details: Any = None):
    """Wrap error message in a standard error envelope."""
    body = {"success": False, "error": message}
    if details:
        body["details"] = details
    return jsonify(body), status


def validate_predict_payload(payload: dict) -> list[str]:
    """
    Validate the prediction request payload.
    Returns a list of error strings (empty if valid).
    """
    errors = []

    # Check required fields
    for field in REQUIRED_PREDICT_FIELDS:
        if field not in payload or payload[field] is None or payload[field] == "":
            errors.append(f"Field '{field}' is required.")

    if errors:
        return errors  # no point further validating if fields are missing

    # Categorical checks
    gender = str(payload.get("gender", ""))
    if gender not in VALID_GENDERS:
        errors.append(f"Invalid gender '{gender}'. Must be one of {sorted(VALID_GENDERS)}.")

    occupation = str(payload.get("occupation", ""))
    if occupation not in VALID_OCCUPATIONS:
        errors.append(f"Invalid occupation '{occupation}'.")

    # Numeric range checks
    numeric_ranges = {
        "age":                      (1,   120),
        "sleep_hours":              (0,   24),
        "sleep_quality":            (1,   10),
        "social_media_hours":       (0,   24),
        "academic_work_pressure":   (0,   10),
        "physical_activity_days":   (0,   7),
        "stress_level":             (0,   10),
        "anxiety_score":            (0,   10),
        "depression_score":         (0,   10),
        "work_life_balance":        (0,   10),
        "mood_score":               (0,   10),
        "concentration_level":      (0,   10),
        "social_support":           (0,   10),
    }

    for field, (lo, hi) in numeric_ranges.items():
        val = payload.get(field)
        try:
            num = float(val)
            if not (lo <= num <= hi):
                errors.append(f"'{field}' must be between {lo} and {hi}.")
        except (TypeError, ValueError):
            errors.append(f"'{field}' must be a number.")

    return errors


def handle_exceptions(f):
    """Decorator: catch unhandled exceptions and return a 500 response."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as exc:
            logger.exception("Unhandled exception in %s", f.__name__)
            return error_response(
                "An unexpected server error occurred.", 500, str(exc)
            )
    return wrapper
