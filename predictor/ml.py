import joblib
import pandas as pd
from django.conf import settings

_bundle = None


def _load():
    global _bundle
    if _bundle is None:
        if not settings.MODEL_PATH.exists():
            raise FileNotFoundError("Model not found. Run: python ml_model/train_model.py")
        _bundle = joblib.load(settings.MODEL_PATH)
    return _bundle


def predict(data: dict):
    """Return (will_subscribe: bool, probability: float)."""
    bundle = _load()
    proba = float(bundle["model"].predict_proba(pd.DataFrame([data]))[0][1])
    return proba >= 0.5, proba


def model_accuracy():
    return _load().get("accuracy")
