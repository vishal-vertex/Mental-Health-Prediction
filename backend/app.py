"""
Flask application entry point.

Responsibilities:
    - Create and configure the Flask app
    - Register all Blueprints
    - Enable CORS
    - Load ML models once at startup
    - Initialise Gemini service
    - Run the development server
"""
import logging
import sys

from flask import Flask, jsonify
from flask_cors import CORS

from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def create_app(cfg: Config = None) -> Flask:
    """Application factory — creates and configures the Flask app."""
    if cfg is None:
        cfg = Config()

    app = Flask(__name__)
    app.config.from_object(cfg)

    # ── CORS ──────────────────────────────────────────────────────
    CORS(app, origins=cfg.CORS_ORIGINS, supports_credentials=True)

    # ── Load ML models at startup (once) ──────────────────────────
    from models.predict_model import registry as model_registry
    try:
        model_registry.load(cfg.MODELS_DIR, cfg)
    except RuntimeError as exc:
        logger.error(str(exc))
        logger.error("Start the server anyway — prediction endpoints will be unavailable until models are trained.")

    # ── Initialise Gemini ──────────────────────────────────────────
    from services import gemini_service
    gemini_service.initialise(cfg.GEMINI_API_KEY)

    # ── Register Blueprints ───────────────────────────────────────
    from routes.prediction_routes    import prediction_bp
    from routes.recommendation_routes import recommendation_bp

    app.register_blueprint(prediction_bp)
    app.register_blueprint(recommendation_bp)

    # ── Health check ──────────────────────────────────────────────
    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status":        "ok",
            "service":       "AI Mental Health Prediction API",
            "models_loaded": model_registry.is_loaded(),
            "version":       "1.0.0",
        })

    # ── Global error handlers ─────────────────────────────────────
    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"success": False, "error": "Endpoint not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"success": False, "error": "Method not allowed."}), 405

    @app.errorhandler(500)
    def internal_error(_):
        return jsonify({"success": False, "error": "Internal server error."}), 500

    logger.info("Flask app created successfully.")
    return app


if __name__ == "__main__":
    config = Config()
    application = create_app(config)
    application.run(
        host="0.0.0.0",
        port=config.PORT,
        debug=config.DEBUG,
    )
