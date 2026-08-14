"""
Blueprint: recommendation routes.
Provides a standalone recommendations endpoint for a given condition/severity.
"""
import logging

from flask import Blueprint, request

from utils.helper import error_response, handle_exceptions, success_response
from utils.recommendation_generator import get_recommendations, get_crisis_resources

logger = logging.getLogger(__name__)

recommendation_bp = Blueprint("recommendation", __name__, url_prefix="/api")

VALID_CONDITIONS = {"Normal", "Anxiety", "Depression", "Burnout"}
VALID_SEVERITIES  = {"Mild", "Moderate", "Severe"}


@recommendation_bp.route("/recommendations", methods=["GET"])
@handle_exceptions
def recommendations():
    """
    GET /api/recommendations?condition=Anxiety&severity=Moderate
    Returns a list of wellness recommendations.
    """
    condition = request.args.get("condition", "").strip()
    severity  = request.args.get("severity",  "").strip()

    if not condition or not severity:
        return error_response("Query params 'condition' and 'severity' are required.", 400)

    if condition not in VALID_CONDITIONS:
        return error_response(f"Invalid condition '{condition}'.", 400)

    if severity not in VALID_SEVERITIES:
        return error_response(f"Invalid severity '{severity}'.", 400)

    recs      = get_recommendations(condition, severity)
    resources = get_crisis_resources()

    return success_response({
        "condition":       condition,
        "severity":        severity,
        "recommendations": recs,
        "crisis_resources": resources,
    })
