"""
Recommendation generator — converts predicted condition/severity into
a structured list of actionable wellness recommendations.
No Flask or ML logic in this file.
"""
from typing import Any

RECOMMENDATIONS: dict[str, dict[str, list[str]]] = {
    "Normal": {
        "Mild": [
            "Maintain your healthy lifestyle — you're doing great!",
            "Continue regular physical activity (at least 30 min/day).",
            "Keep a consistent sleep schedule of 7–9 hours.",
            "Nurture social connections with friends and family.",
            "Practice mindfulness or journaling to stay grounded.",
        ],
        "Moderate": [
            "Stay active with daily walks or light exercise.",
            "Monitor stress levels and use breathing techniques.",
            "Maintain work-life balance by setting clear boundaries.",
            "Connect with supportive people regularly.",
            "Schedule regular health check-ins for peace of mind.",
        ],
        "Severe": [
            "Speak with a healthcare professional to discuss your well-being.",
            "Increase physical activity gradually and consistently.",
            "Establish a calming bedtime routine for quality sleep.",
            "Limit screen time especially before bed.",
            "Engage in social activities to boost mood.",
        ],
    },
    "Anxiety": {
        "Mild": [
            "Practice deep breathing or box breathing exercises daily.",
            "Limit caffeine and alcohol as they can worsen anxiety.",
            "Ensure 7–9 hours of quality sleep each night.",
            "Engage in regular physical activity to release tension.",
            "Try mindfulness meditation apps (e.g., Calm, Headspace).",
        ],
        "Moderate": [
            "Consider Cognitive Behavioral Therapy (CBT) with a licensed therapist.",
            "Practice progressive muscle relaxation daily.",
            "Reduce social media consumption to lower anxiety triggers.",
            "Establish a consistent daily routine for predictability.",
            "Talk to someone you trust about your worries.",
        ],
        "Severe": [
            "Consult a mental health professional as soon as possible.",
            "CBT and possibly medication may be recommended by your doctor.",
            "Avoid overwhelming situations — take breaks when needed.",
            "Join a support group for anxiety management.",
            "Focus on one task at a time to reduce overwhelm.",
        ],
    },
    "Depression": {
        "Mild": [
            "Engage in light exercise — even a 20-minute walk helps significantly.",
            "Maintain social connections — isolation worsens depression.",
            "Pursue hobbies or activities that once brought joy.",
            "Set small, achievable daily goals to build momentum.",
            "Get adequate sunlight exposure — aim for 15–30 min outdoors.",
        ],
        "Moderate": [
            "Seek professional help — psychotherapy is highly effective.",
            "Consider speaking with your doctor about treatment options.",
            "Establish a structured daily routine for stability.",
            "Reduce alcohol and substance use which worsen depression.",
            "Connect with mental health helplines if you feel overwhelmed.",
        ],
        "Severe": [
            "Immediately consult a psychiatrist or mental health professional.",
            "A combination of therapy and medication is often most effective.",
            "Reach out to crisis support lines if you feel at risk.",
            "Involve trusted family members in your support system.",
            "Avoid major life decisions during severe depressive episodes.",
        ],
    },
    "Burnout": {
        "Mild": [
            "Take regular short breaks throughout your workday.",
            "Prioritize tasks and delegate where possible.",
            "Set firm boundaries between work and personal time.",
            "Engage in restorative hobbies (reading, nature walks, art).",
            "Practice gratitude journaling each morning.",
        ],
        "Moderate": [
            "Take a proper vacation or time off from responsibilities.",
            "Work with a therapist on stress management strategies.",
            "Reduce workload by communicating limits to managers/professors.",
            "Incorporate daily meditation or yoga into your routine.",
            "Re-evaluate long-term goals and work environment.",
        ],
        "Severe": [
            "Take an immediate break from all major responsibilities.",
            "Consult a doctor — chronic burnout can cause physical health issues.",
            "Consider a career or environment change if burnout is persistent.",
            "Engage in intensive therapy focused on recovery and rebuilding.",
            "Rest, sleep, and nutrition are non-negotiable priorities right now.",
        ],
    },
}

DEFAULT_RECOMMENDATIONS = [
    "Take care of your mental health — it is just as important as physical health.",
    "Maintain a balanced routine with proper sleep, nutrition, and exercise.",
    "Connect with supportive friends, family, or a mental health professional.",
    "Monitor your stress levels and take proactive steps to reduce them.",
    "If in doubt, consult a healthcare professional for personalized guidance.",
]


def get_recommendations(condition: str, severity: str) -> list[str]:
    """
    Return a list of 5 actionable recommendations based on
    the predicted mental health condition and severity level.
    """
    condition = condition.strip()
    severity  = severity.strip()

    condition_map = RECOMMENDATIONS.get(condition)
    if not condition_map:
        return DEFAULT_RECOMMENDATIONS

    return condition_map.get(severity, list(condition_map.values())[0])


def get_crisis_resources() -> list[dict[str, str]]:
    """Return a list of global mental health crisis resources."""
    return [
        {"name": "iCall (India)",        "contact": "9152987821"},
        {"name": "Vandrevala Foundation", "contact": "1860-2662-345"},
        {"name": "NIMHANS (India)",       "contact": "080-46110007"},
        {"name": "Crisis Text Line (US)", "contact": "Text HOME to 741741"},
        {"name": "Samaritans (UK)",       "contact": "116 123"},
    ]
