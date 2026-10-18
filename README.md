# Mental Health Prediction

A web app that uses three Random Forest classifiers to predict a mental-health
condition, severity, and treatment category from 15 user-provided features.
This is an educational project, not a medical diagnosis or treatment
recommendation.

## Backend

The prediction API is in `backend/app.py`. Model inference and preprocessing
are kept in `backend/models/`. The backend contains the saved model artifacts
for inference; training data and training scripts are not included.

```text
backend/
  app.py                 API routes, validation, and response formatting
  config.py              Environment settings and model artifact paths
  models/
    predict_model.py     Loads saved models and runs predictions
    preprocess.py        Shared feature preprocessing
    *.pkl                Trained models and preprocessing artifacts
    model_metrics.json   Evaluation metrics shown on the About page
```

To run the API locally from the repository root:

```powershell
cd backend
python -m pip install -r requirements.txt
python app.py
```

The saved model artifacts are included. The server reads `FLASK_PORT`,
`FLASK_DEBUG`, and `CORS_ORIGINS` from the environment; see
`backend/.env.example`.

## Prediction API

`POST /api/predict` accepts JSON containing `age`, `gender`, `occupation`,
`sleep_hours`, `sleep_quality`, `social_media_hours`,
`academic_work_pressure`, `physical_activity_days`, `stress_level`,
`anxiety_score`, `depression_score`, `work_life_balance`, `mood_score`,
`concentration_level`, and `social_support`.

The response includes `condition`, `severity`, `treatment`, `confidence`, and
`prediction_time`. `GET /api/model-info` returns the stored evaluation metrics;
`GET /` reports whether the saved models loaded successfully.

The frontend lives in `frontend/`. Configure `VITE_API_BASE_URL` if the API is
not running at `http://localhost:5000`.
