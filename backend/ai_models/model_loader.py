import os
import joblib


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")


def load_category_model():
    model_path = os.path.join(MODEL_DIR, "category_model.pkl")
    vectorizer_path = os.path.join(MODEL_DIR, "category_vectorizer.pkl")

    if not os.path.exists(model_path):
        print("Category model not found:", model_path)
        return None, None

    if not os.path.exists(vectorizer_path):
        print("Category vectorizer not found:", vectorizer_path)
        return None, None

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    return model, vectorizer


def load_sentiment_model():
    model_path = os.path.join(MODEL_DIR, "sentiment_model.pkl")
    vectorizer_path = os.path.join(MODEL_DIR, "sentiment_vectorizer.pkl")

    if not os.path.exists(model_path):
        print("Sentiment model not found:", model_path)
        return None, None

    if not os.path.exists(vectorizer_path):
        print("Sentiment vectorizer not found:", vectorizer_path)
        return None, None

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    return model, vectorizer


def load_priority_model():
    model_path = os.path.join(MODEL_DIR, "priority_model.pkl")

    if not os.path.exists(model_path):
        print("Priority model not found:", model_path)
        return None

    model = joblib.load(model_path)
    return model
def load_csat_artifacts():
    keras_model_path = os.path.join(MODEL_DIR, "csat_model.keras")
    h5_model_path = os.path.join(MODEL_DIR, "csat_model.h5")
    scaler_path = os.path.join(MODEL_DIR, "csat_scaler.pkl")
    metadata_path = os.path.join(MODEL_DIR, "csat_metadata.pkl")

    model_path = None

    if os.path.exists(keras_model_path):
        model_path = keras_model_path
    elif os.path.exists(h5_model_path):
        model_path = h5_model_path

    if model_path is None:
        print("CSAT ANN model not found in:", MODEL_DIR)
        return None, None, None

    try:
        from tensorflow.keras.models import load_model
    except ImportError:
        print("TensorFlow is not installed. Cannot load CSAT ANN model.")
        return None, None, None

    try:
        model = load_model(model_path, compile=False)
        print("CSAT model loaded successfully:", model_path)
    except Exception as e:
        print("Failed to load CSAT model:", str(e))
        return None, None, None

    scaler = None
    metadata = None

    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)
        print("CSAT scaler loaded successfully.")

    if os.path.exists(metadata_path):
        metadata = joblib.load(metadata_path)
        print("CSAT metadata loaded successfully.")

    return model, scaler, metadata