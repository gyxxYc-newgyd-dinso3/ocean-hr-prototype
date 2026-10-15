"""Research-only scaffold for supervised Big Five model experiments.

Do not connect this to hiring decisions. It is intentionally not loaded by the
web request path. Training requires consented, appropriately licensed text and
validated Big Five labels, plus fairness and validity evaluation.
"""
from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).resolve().parent / "ml_artifacts" / "experimental_big_five_pipeline.joblib"


def load_experimental_model():
    """Return a saved experimental model if one exists; otherwise None."""
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def predict_for_research_only(cv_text):
    """Research sandbox only; this is not used by Django views."""
    model = load_experimental_model()
    if model is None:
        return {"available": False, "message": "No trained model found. Provide a valid research dataset and evaluate a model first."}
    prediction = model.predict([cv_text])[0]
    dimensions = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    return {"available": True, "experimental": True, "scores": {k: float(v) for k, v in zip(dimensions, prediction)}}
