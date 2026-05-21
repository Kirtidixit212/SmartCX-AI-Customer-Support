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
    # Positive
    ("Thank you for solving my issue quickly", "Positive"),
    ("The support team was very helpful", "Positive"),
    ("I am happy with the service", "Positive"),
    ("My issue was resolved perfectly", "Positive"),
    ("Excellent customer support experience", "Positive"),
    ("The agent was polite and supportive", "Positive"),
    ("I received my refund quickly thank you", "Positive"),
    ("Very good service and fast response", "Positive"),
    ("I am satisfied with the solution", "Positive"),
    ("The product replacement was smooth", "Positive"),
    ("Support team helped me very well", "Positive"),
    ("Great experience with customer care", "Positive"),
    ("The delivery issue was fixed quickly", "Positive"),
    ("I appreciate the fast support", "Positive"),
    ("The agent explained everything clearly", "Positive"),

    # Neutral
    ("I need help with my order", "Neutral"),
    ("Can you tell me the status of my ticket", "Neutral"),
    ("I want to know about the return policy", "Neutral"),
    ("Please provide more information about my order", "Neutral"),
    ("I have a question about my product", "Neutral"),
    ("Can you check my delivery status", "Neutral"),
    ("I want to update my address", "Neutral"),
    ("Please tell me the refund timeline", "Neutral"),
    ("I need information about warranty", "Neutral"),
    ("Where can I download my invoice", "Neutral"),
    ("I want to contact customer support", "Neutral"),
    ("Can you explain the exchange process", "Neutral"),
    ("I want to know when my order will arrive", "Neutral"),
    ("Please share order tracking details", "Neutral"),
    ("I need assistance with my account", "Neutral"),

    # Negative
    ("My order is delayed and I am disappointed", "Negative"),
    ("The support response is very slow", "Negative"),
    ("I did not receive my refund yet", "Negative"),
    ("The product quality is poor", "Negative"),
    ("My payment was deducted but order was not placed", "Negative"),
    ("I am not happy with this service", "Negative"),
    ("Delivery is late and nobody updated me", "Negative"),
    ("The agent did not solve my issue", "Negative"),
    ("I received a damaged product", "Negative"),
    ("Refund is pending for many days", "Negative"),
    ("This is a bad customer experience", "Negative"),
    ("My issue is still unresolved", "Negative"),
    ("The product is not working properly", "Negative"),
    ("I am facing the same problem again", "Negative"),
    ("Support team is not responding", "Negative"),

    # Very Negative
    ("Worst service ever I am very angry", "Very Negative"),
    ("This is completely unacceptable and terrible", "Very Negative"),
    ("I feel cheated because my money is gone", "Very Negative"),
    ("I will file a complaint against this company", "Very Negative"),
    ("This looks like fraud and scam", "Very Negative"),
    ("Nobody is helping me and this is horrible", "Very Negative"),
    ("I am extremely frustrated with your service", "Very Negative"),
    ("Very poor service I will never order again", "Very Negative"),
    ("This company has wasted my time and money", "Very Negative"),
    ("I want immediate action or I will complain legally", "Very Negative"),
    ("I am very angry because refund is not given", "Very Negative"),
    ("This is the worst customer support experience", "Very Negative"),
    ("Completely useless support and no solution", "Very Negative"),
    ("I have been cheated by this order process", "Very Negative"),
    ("Terrible experience and no one is taking responsibility", "Very Negative"),
]

df = pd.DataFrame(data, columns=["text", "sentiment"])

X = df["text"]
y = df["sentiment"]

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

model_path = os.path.join(MODEL_DIR, "sentiment_model.pkl")
vectorizer_path = os.path.join(MODEL_DIR, "sentiment_vectorizer.pkl")

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print("\nSentiment model saved successfully.")
print("Model path:", model_path)
print("Vectorizer path:", vectorizer_path)