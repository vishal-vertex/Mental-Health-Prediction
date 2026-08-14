"""
Gemini AI service — generates personalized wellness suggestions.
Reads the API key from environment. Gracefully falls back if key is missing
or the API call fails.
"""
import logging
import os

logger = logging.getLogger(__name__)

_gemini_client = None
_gemini_model  = None


def _init_gemini(api_key: str) -> bool:
    """Initialise the Gemini client. Returns True on success."""
    global _gemini_client, _gemini_model
    if not api_key or api_key in ("your_gemini_api_key_here", ""):
        logger.warning("GEMINI_API_KEY not set — AI suggestions disabled.")
        return False
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        _gemini_model  = genai.GenerativeModel("gemini-1.5-flash")
        _gemini_client = genai
        logger.info("Gemini AI initialised successfully.")
        return True
    except Exception as exc:
        logger.warning("Gemini init failed: %s", exc)
        return False


def initialise(api_key: str) -> None:
    _init_gemini(api_key)


def _build_prompt(condition: str, severity: str, treatment: str, user_data: dict) -> str:
    age        = user_data.get("age", "unknown")
    gender     = user_data.get("gender", "unknown")
    occupation = user_data.get("occupation", "unknown")
    sleep_hrs  = user_data.get("sleep_hours", "unknown")
    stress     = user_data.get("stress_level", "unknown")
    activity   = user_data.get("physical_activity_days", "unknown")

    return (
        f"You are a compassionate mental health wellness coach. "
        f"A {age}-year-old {gender} working as a {occupation} has been assessed.\n\n"
        f"Assessment Results:\n"
        f"- Mental Health Condition: {condition}\n"
        f"- Severity: {severity}\n"
        f"- Recommended Treatment: {treatment}\n\n"
        f"Lifestyle Snapshot:\n"
        f"- Sleep: {sleep_hrs} hours/night\n"
        f"- Stress Level: {stress}/10\n"
        f"- Physical Activity: {activity} days/week\n\n"
        f"Please provide 3–4 personalised, empathetic, and actionable wellness suggestions "
        f"tailored specifically to this person's profile. Be warm, non-judgmental, and "
        f"evidence-based. Do NOT use bullet points — write in a conversational, supportive tone. "
        f"Keep the response under 200 words."
    )


def get_gemini_suggestion(
    condition: str,
    severity: str,
    treatment: str,
    user_data: dict,
    fallback_recommendations: list[str] | None = None,
) -> str:
    """
    Call Gemini API for a personalised wellness suggestion.
    Returns the AI text, or a well-formatted fallback if the API is unavailable.
    """
    if _gemini_model is None:
        return _build_fallback(condition, severity, fallback_recommendations)

    try:
        prompt   = _build_prompt(condition, severity, treatment, user_data)
        response = _gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        logger.warning("Gemini API call failed: %s", exc)
        return _build_fallback(condition, severity, fallback_recommendations)


def _build_fallback(
    condition: str,
    severity: str,
    recommendations: list[str] | None,
) -> str:
    if recommendations:
        tips = " ".join(f"({i+1}) {r}" for i, r in enumerate(recommendations[:3]))
        return (
            f"Based on your {severity.lower()} {condition} assessment, here are your "
            f"top personalised suggestions: {tips} "
            f"Remember — small, consistent steps lead to lasting well-being. "
            f"You are not alone on this journey."
        )
    return (
        f"You have been assessed with {severity} {condition}. "
        f"We encourage you to consult a qualified mental health professional "
        f"and take proactive steps towards your well-being every day."
    )
