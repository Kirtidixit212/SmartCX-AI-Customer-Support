import os
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

os.makedirs(MODEL_DIR, exist_ok=True)


data = [
    # Refund Issue
    ("I want my refund because my order was cancelled", "Refund Issue"),
    ("My money was deducted but I did not receive refund", "Refund Issue"),
    ("Refund is still pending after many days", "Refund Issue"),
    ("I returned the product but refund is not credited", "Refund Issue"),
    ("Payment deducted twice and refund not received", "Refund Issue"),
    ("I need my refund urgently", "Refund Issue"),
    ("Refund amount is not showing in my account", "Refund Issue"),
    ("I cancelled order but money is not refunded", "Refund Issue"),
    ("I have been waiting for refund for one week", "Refund Issue"),
    ("Refund process is very slow", "Refund Issue"),
    ("My refund request is not processed", "Refund Issue"),
    ("I did not get refund after return pickup", "Refund Issue"),

    # Payment Issue
    ("Payment failed but amount was deducted", "Payment Issue"),
    ("Transaction failed during checkout", "Payment Issue"),
    ("UPI payment is not working", "Payment Issue"),
    ("My card payment failed", "Payment Issue"),
    ("I cannot complete payment", "Payment Issue"),
    ("Payment gateway is showing error", "Payment Issue"),
    ("Money deducted but order not placed", "Payment Issue"),
    ("I am facing payment issue while ordering", "Payment Issue"),
    ("Net banking payment failed", "Payment Issue"),
    ("Payment page is not loading", "Payment Issue"),
    ("My transaction is stuck", "Payment Issue"),
    ("I paid but order confirmation is not showing", "Payment Issue"),

    # Delivery Issue
    ("My order is delayed", "Delivery Issue"),
    ("Delivery is late and I need my product", "Delivery Issue"),
    ("I have not received my order yet", "Delivery Issue"),
    ("Where is my delivery", "Delivery Issue"),
    ("Order tracking is not updating", "Delivery Issue"),
    ("Package is stuck in transit", "Delivery Issue"),
    ("Delivery partner did not call me", "Delivery Issue"),
    ("My parcel has not arrived", "Delivery Issue"),
    ("Delivery date passed but product not received", "Delivery Issue"),
    ("My shipment is delayed", "Delivery Issue"),
    ("The courier is not delivering my package", "Delivery Issue"),
    ("Order status says shipped but I have not received it", "Delivery Issue"),

    # Product Damage
    ("I received a damaged product", "Product Damage"),
    ("The item is broken", "Product Damage"),
    ("Product is defective and not working", "Product Damage"),
    ("My package arrived damaged", "Product Damage"),
    ("The screen is cracked", "Product Damage"),
    ("The product quality is very poor", "Product Damage"),
    ("I got a broken item", "Product Damage"),
    ("The product is not working properly", "Product Damage"),
    ("Product has scratches and dents", "Product Damage"),
    ("Item is damaged inside the box", "Product Damage"),
    ("Received defective electronic item", "Product Damage"),
    ("The product stopped working after delivery", "Product Damage"),

    # Return Request
    ("I want to return this product", "Return Request"),
    ("How can I return my order", "Return Request"),
    ("Please arrange return pickup", "Return Request"),
    ("I want replacement for this item", "Return Request"),
    ("Return request is not accepted", "Return Request"),
    ("I need to exchange this product", "Return Request"),
    ("The product is not suitable and I want return", "Return Request"),
    ("Please start return process", "Return Request"),
    ("I want to replace this product", "Return Request"),
    ("Return pickup has not been scheduled", "Return Request"),
    ("I selected wrong size and want exchange", "Return Request"),
    ("Please help me return my order", "Return Request"),

    # Account/Login Issue
    ("I cannot login to my account", "Account/Login Issue"),
    ("Password reset is not working", "Account/Login Issue"),
    ("My account is locked", "Account/Login Issue"),
    ("I forgot my password", "Account/Login Issue"),
    ("Login OTP is not received", "Account/Login Issue"),
    ("I cannot access my profile", "Account/Login Issue"),
    ("Account verification failed", "Account/Login Issue"),
    ("I am unable to sign in", "Account/Login Issue"),
    ("My email verification is not working", "Account/Login Issue"),
    ("I cannot update my account details", "Account/Login Issue"),
    ("My login page keeps showing error", "Account/Login Issue"),
    ("I am not able to open my account", "Account/Login Issue"),

    # Order Cancellation
    ("I want to cancel my order", "Order Cancellation"),
    ("Please cancel this order", "Order Cancellation"),
    ("Cancel request is not working", "Order Cancellation"),
    ("I placed wrong order and want cancellation", "Order Cancellation"),
    ("Order cancellation failed", "Order Cancellation"),
    ("Can I cancel my product", "Order Cancellation"),
    ("I need to stop this order", "Order Cancellation"),
    ("Cancel my order immediately", "Order Cancellation"),
    ("I ordered by mistake please cancel it", "Order Cancellation"),
    ("Cancellation option is not visible", "Order Cancellation"),
    ("I want to cancel before shipping", "Order Cancellation"),
    ("Please stop dispatch and cancel order", "Order Cancellation"),

    # General Query
    ("I want to know your return policy", "General Query"),
    ("How can I contact support", "General Query"),
    ("What are your delivery charges", "General Query"),
    ("I need information about warranty", "General Query"),
    ("Can you tell me product details", "General Query"),
    ("Where can I find invoice", "General Query"),
    ("I have a general question", "General Query"),
    ("Please help me with my query", "General Query"),
    ("What is the warranty period", "General Query"),
    ("Where can I download invoice", "General Query"),
    ("Can you explain the offer details", "General Query"),
    ("I need help understanding product specifications", "General Query"),
]


df = pd.DataFrame(data, columns=["text", "category"])

X = df["text"]
y = df["category"]

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_features=3000
)

X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

model_path = os.path.join(MODEL_DIR, "category_model.pkl")
vectorizer_path = os.path.join(MODEL_DIR, "category_vectorizer.pkl")

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print("\nModel saved successfully.")
print("Model path:", model_path)
print("Vectorizer path:", vectorizer_path)