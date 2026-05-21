import numpy as np
import pandas as pd

from ai_models.model_loader import load_csat_artifacts


def map_smartcx_to_deepcsat_category(category: str) -> str:
    mapping = {
        "Refund Issue": "Returns",
        "Payment Issue": "Payments",
        "Delivery Issue": "Shipping",
        "Product Damage": "Product Queries",
        "Return Request": "Returns",
        "Account/Login Issue": "Account",
        "Order Cancellation": "Cancellation",
        "General Query": "Product Queries",
    }

    return mapping.get(category, "Product Queries")


def map_smartcx_to_deepcsat_subcategory(category: str) -> str:
    mapping = {
        "Refund Issue": "Refund Related",
        "Payment Issue": "Payment Related",
        "Delivery Issue": "Delivery Related",
        "Product Damage": "Product Specific Information",
        "Return Request": "Return request",
        "Account/Login Issue": "Login Issues",
        "Order Cancellation": "Order Cancellation",
        "General Query": "Product Specific Information",
    }

    return mapping.get(category, "Product Specific Information")


def predict_csat_with_ann(
    category: str,
    priority: str,
    sentiment: str,
    order_value: float = 0,
    previous_complaints: int = 0,
    response_time_minutes: float = 30,
    resolution_time_hours: float = 24,
):
    """
    Predict CSAT using DeepCSAT ANN model.

    Uses:
    - csat_model.h5
    - csat_scaler.pkl
    - csat_metadata.pkl
    """

    model, scaler, metadata = load_csat_artifacts()

    if model is None or scaler is None or metadata is None:
        print("CSAT artifacts missing. Falling back to rule-based CSAT.")
        return None

    try:
        feature_columns = metadata["feature_columns"]
        response_time_default = metadata.get("response_time_median", 30)

        deepcsat_category = map_smartcx_to_deepcsat_category(category)
        deepcsat_subcategory = map_smartcx_to_deepcsat_subcategory(category)

        if priority in ["Critical", "High"] or sentiment in ["Negative", "Very Negative"]:
            channel_name = "Inbound"
        else:
            channel_name = "Outcall"

        if priority in ["Critical", "High"]:
            tenure_bucket = ">90"
        else:
            tenure_bucket = "On Job Training"

        agent_shift = "Morning"

        response_time = response_time_minutes or response_time_default

        input_df = pd.DataFrame(
            np.zeros((1, len(feature_columns))),
            columns=feature_columns
        )

        raw_features = {
            "response_time": response_time,
            f"channel_name_{channel_name}": 1,
            f"category_{deepcsat_category}": 1,
            f"Sub-category_{deepcsat_subcategory}": 1,
            f"Tenure Bucket_{tenure_bucket}": 1,
            f"Agent Shift_{agent_shift}": 1,
        }

        for col, value in raw_features.items():
            if col in input_df.columns:
                input_df.loc[0, col] = value
            else:
                print(f"CSAT feature column not found and skipped: {col}")

        input_scaled = scaler.transform(input_df)

        print("CSAT input shape:", input_scaled.shape)
        print("Model expected shape:", model.input_shape)

        prediction = model.predict(input_scaled)

        print("Raw CSAT prediction:", prediction)

        predicted_class = int(np.argmax(prediction, axis=1)[0])

        # ANN output classes are 0-4, convert to CSAT 1-5
        predicted_csat = predicted_class + 1

        predicted_csat = max(1, min(5, predicted_csat))

        return predicted_csat

    except Exception as e:
        print("CSAT ANN prediction failed:", str(e))
        return None