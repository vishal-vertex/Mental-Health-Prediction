"""
Application configuration loaded from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    # Flask
    DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    PORT: int = int(os.getenv("FLASK_PORT", 5000))

    # CORS
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173"
    ).split(",")

    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DATASET_PATH: str = os.path.join(BASE_DIR, "dataset", "mental_health_prediction.csv")
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")

    # Model artifact file names
    CONDITION_MODEL_FILE: str = "condition_model.pkl"
    SEVERITY_MODEL_FILE: str = "severity_model.pkl"
    TREATMENT_MODEL_FILE: str = "treatment_model.pkl"
    SCALER_FILE: str = "scaler.pkl"
    LABEL_ENCODERS_FILE: str = "label_encoders.pkl"
    METRICS_FILE: str = "model_metrics.json"
