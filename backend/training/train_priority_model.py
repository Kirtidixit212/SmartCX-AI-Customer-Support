import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

os.makedirs(MODEL_DIR, exist_ok=True)


data = [
    # Low Priority
    ("I want to know your return policy", "General Query", "Neutral", 0, 500, "Low"),
    ("Can you tell me product warranty details", "General Query", "Neutral", 0, 800, "Low"),
    ("Where can I download my invoice", "General Query", "Neutral", 0, 300, "Low"),
    ("I need information about delivery charges", "General Query", "Neutral", 0, 400, "Low"),
    ("Can you explain exchange process", "General Query", "Neutral", 0, 700, "Low"),
    ("I want to update my profile details", "Account/Login Issue", "Neutral", 0, 500, "Low"),
    ("Please share product specifications", "General Query", "Neutral", 0, 900, "Low"),
    ("I have a question about offers", "General Query", "Neutral", 0, 1000, "Low"),

    # Medium Priority
    ("My order is delayed and tracking is not updating", "Delivery Issue", "Negative", 1, 1200, "Medium"),
    ("I did not receive login OTP", "Account/Login Issue", "Negative", 1, 500, "Medium"),
    ("Return pickup has not been scheduled", "Return Request", "Negative", 1, 1500, "Medium"),
    ("My product is not suitable and I want return", "Return Request", "Neutral", 1, 1800, "Medium"),
    ("Support team is not responding to my query", "General Query", "Negative", 2, 600, "Medium"),
    ("My delivery is late by two days", "Delivery Issue", "Negative", 1, 900, "Medium"),
    ("I cannot access my account", "Account/Login Issue", "Negative", 1, 700, "Medium"),
    ("My issue is still unresolved", "General Query", "Negative", 2, 1000, "Medium"),

    # High Priority
    ("My refund is delayed and nobody is helping me", "Refund Issue", "Negative", 2, 2500, "High"),
    ("Payment failed but amount was deducted", "Payment Issue", "Negative", 2, 3000, "High"),
    ("I received a damaged product and need replacement", "Product Damage", "Negative", 1, 4000, "High"),
    ("Money deducted but order was not placed", "Payment Issue", "Negative", 2, 3500, "High"),
    ("Refund is pending for many days", "Refund Issue", "Negative", 3, 2000, "High"),
    ("Product is broken and not working", "Product Damage", "Negative", 2, 5000, "High"),
    ("My delivery is delayed and product is urgent", "Delivery Issue", "Negative", 3, 2500, "High"),
    ("I returned the product but refund is not credited", "Refund Issue", "Negative", 2, 3200, "High"),

    # Critical Priority
    ("Worst service ever I am very angry and want immediate action", "Refund Issue", "Very Negative", 4, 5000, "Critical"),
    ("This is fraud my money is gone and nobody is helping", "Payment Issue", "Very Negative", 4, 8000, "Critical"),
    ("I will file a complaint because refund is not given", "Refund Issue", "Very Negative", 5, 6000, "Critical"),
    ("I received a damaged expensive product and support ignored me", "Product Damage", "Very Negative", 4, 10000, "Critical"),
    ("Very poor service I will never order again", "Delivery Issue", "Very Negative", 4, 3500, "Critical"),
    ("This company cheated me payment deducted no order no refund", "Payment Issue", "Very Negative", 5, 7000, "Critical"),
    ("I need urgent help nobody is responding and issue is serious", "General Query", "Very Negative", 5, 4500, "Critical"),
    ("Terrible experience no solution after many complaints", "Refund Issue", "Very Negative", 5, 9000, "Critical"),

    # More Low
    ("Thank you I just want confirmation about warranty", "General Query", "Positive", 0, 400, "Low"),
    ("Support was helpful I only need invoice", "General Query", "Positive", 0, 300, "Low"),
    ("Can you tell me delivery estimate", "General Query", "Neutral", 0, 600, "Low"),
    ("I want to know product details", "General Query", "Neutral", 0, 800, "Low"),

    # More Medium
    ("My password reset is not working", "Account/Login Issue", "Negative", 1, 600, "Medium"),
    ("Return option is not visible", "Return Request", "Negative", 1, 1100, "Medium"),
    ("Order tracking is stuck", "Delivery Issue", "Negative", 1, 1300, "Medium"),
    ("My parcel is late", "Delivery Issue", "Negative", 1, 1400, "Medium"),

    # More High
    ("Payment deducted twice and refund not received", "Refund Issue", "Negative", 3, 2800, "High"),
    ("The screen is cracked and I want replacement", "Product Damage", "Negative", 2, 6000, "High"),
    ("My order was cancelled but money not refunded", "Refund Issue", "Negative", 3, 2400, "High"),
    ("Transaction failed and money is deducted", "Payment Issue", "Negative", 2, 2200, "High"),

    # More Critical
    ("I am extremely frustrated and will complain legally", "Refund Issue", "Very Negative", 5, 10000, "Critical"),
    ("This is scam payment deducted and support disappeared", "Payment Issue", "Very Negative", 5, 8500, "Critical"),
    ("Worst customer support and no one is taking responsibility", "General Query", "Very Negative", 4, 5000, "Critical"),
    ("I feel cheated damaged product and no refund", "Product Damage", "Very Negative", 4, 7500, "Critical"),
]

df = pd.DataFrame(
    data,
    columns=[
        "message",
        "category",
        "sentiment",
        "previous_complaints",
        "order_value",
        "priority",
    ],
)

X = df[["message", "category", "sentiment", "previous_complaints", "order_value"]]
y = df["priority"]

preprocessor = ColumnTransformer(
    transformers=[
        ("message_tfidf", TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=3000
        ), "message"),

        ("category_ohe", OneHotEncoder(handle_unknown="ignore"), ["category"]),
        ("sentiment_ohe", OneHotEncoder(handle_unknown="ignore"), ["sentiment"]),
        ("numeric", StandardScaler(), ["previous_complaints", "order_value"]),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

model_path = os.path.join(MODEL_DIR, "priority_model.pkl")
joblib.dump(model, model_path)

print("\nPriority model saved successfully.")
print("Model path:", model_path)