import os
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "eCommerce_Customer_support_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

os.makedirs(MODEL_DIR, exist_ok=True)


def build_csat_artifacts():
    df = pd.read_csv(DATA_PATH)

    print("Original shape:", df.shape)

    # Drop unnecessary columns as per DeepCSAT notebook
    columns_to_drop = [
        "Unique id",
        "Customer Remarks",
        "Order_id",
        "order_date_time",
        "Customer_City",
        "Product_category",
        "Item_price",
        "connected_handling_time",
        "Agent_name",
        "Supervisor",
        "Manager",
    ]

    df = df.drop(columns=columns_to_drop, errors="ignore")

    # Drop missing rows
    df = df.dropna()

    # Convert date columns
    df["Issue_reported at"] = pd.to_datetime(
        df["Issue_reported at"],
        errors="coerce",
        dayfirst=True
    )

    df["issue_responded"] = pd.to_datetime(
        df["issue_responded"],
        errors="coerce",
        dayfirst=True
    )

    df["Survey_response_Date"] = pd.to_datetime(
        df["Survey_response_Date"],
        errors="coerce",
        dayfirst=True
    )

    df = df.dropna()

    # Create response_time in minutes
    df["response_time"] = (
        df["issue_responded"] - df["Issue_reported at"]
    ).dt.total_seconds() / 60

    # Remove negative response times
    df = df[df["response_time"] >= 0]

    # Remove response_time outliers using IQR
    Q1 = df["response_time"].quantile(0.25)
    Q3 = df["response_time"].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df = df[
        (df["response_time"] >= lower_bound) &
        (df["response_time"] <= upper_bound)
    ]

    # Drop date columns after creating response_time
    df = df.drop(
        columns=[
            "Issue_reported at",
            "issue_responded",
            "Survey_response_Date",
        ],
        errors="ignore"
    )

    # One-hot encode categorical columns
    categorical_columns = [
        "channel_name",
        "category",
        "Sub-category",
        "Tenure Bucket",
        "Agent Shift",
    ]

    df_encoded = pd.get_dummies(
        df,
        columns=categorical_columns,
        drop_first=False
    )

    # Separate X and y
    X = df_encoded.drop("CSAT Score", axis=1)
    y = df_encoded["CSAT Score"]

    print("Processed X shape:", X.shape)
    print("Target shape:", y.shape)

    scaler = StandardScaler()
    scaler.fit(X)

    feature_columns = X.columns.tolist()

    metadata = {
        "feature_columns": feature_columns,
        "categorical_columns": categorical_columns,
        "response_time_median": float(df["response_time"].median()),
        "response_time_mean": float(df["response_time"].mean()),
        "target_column": "CSAT Score",
        "input_feature_count": len(feature_columns),
    }

    scaler_path = os.path.join(MODEL_DIR, "csat_scaler.pkl")
    metadata_path = os.path.join(MODEL_DIR, "csat_metadata.pkl")

    joblib.dump(scaler, scaler_path)
    joblib.dump(metadata, metadata_path)

    print("CSAT scaler saved:", scaler_path)
    print("CSAT metadata saved:", metadata_path)
    print("Number of features:", len(feature_columns))

    print("\nFeature columns:")
    for col in feature_columns:
        print(col)


if __name__ == "__main__":
    build_csat_artifacts()