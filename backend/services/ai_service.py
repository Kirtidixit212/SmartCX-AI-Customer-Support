import pandas as pd

from utils.preprocessing import clean_text

from ai_models.model_loader import (
    load_category_model,
    load_sentiment_model,
    load_priority_model,
)

from ai_models.csat_model import predict_csat_with_ann


def analyze_sentiment(text: str) -> str:
    cleaned_text = clean_text(text)

    model, vectorizer = load_sentiment_model()

    if model is not None and vectorizer is not None:
        text_vector = vectorizer.transform([cleaned_text])
        prediction = model.predict(text_vector)[0]
        return prediction

    # Fallback rule-based sentiment if ML model is not available
    very_negative_words = [
        "worst", "angry", "fraud", "cheated", "terrible", "useless",
        "complaint", "legal", "scam", "horrible", "unacceptable"
    ]

    negative_words = [
        "bad", "delay", "delayed", "refund", "poor", "broken",
        "damaged", "issue", "problem", "not received", "deducted",
        "late", "missing", "unresolved", "disappointed"
    ]

    positive_words = [
        "good", "great", "happy", "thanks", "thank", "helpful",
        "resolved", "satisfied", "excellent", "quick", "supportive",
        "polite", "appreciate"
    ]

    very_negative_count = sum(1 for word in very_negative_words if word in cleaned_text)
    negative_count = sum(1 for word in negative_words if word in cleaned_text)
    positive_count = sum(1 for word in positive_words if word in cleaned_text)

    if very_negative_count >= 1 or negative_count >= 3:
        return "Very Negative"

    if negative_count > positive_count:
        return "Negative"

    if positive_count > negative_count:
        return "Positive"

    return "Neutral"


def predict_category(text: str) -> str:
    cleaned_text = clean_text(text)

    model, vectorizer = load_category_model()

    if model is not None and vectorizer is not None:
        text_vector = vectorizer.transform([cleaned_text])
        prediction = model.predict(text_vector)[0]
        return prediction

    # Fallback rule-based prediction if ML model is not available
    if "refund" in cleaned_text or "money" in cleaned_text or "deducted" in cleaned_text:
        return "Refund Issue"

    if "payment" in cleaned_text or "transaction" in cleaned_text or "upi" in cleaned_text:
        return "Payment Issue"

    if (
        "late" in cleaned_text
        or "delay" in cleaned_text
        or "delivery" in cleaned_text
        or "not received" in cleaned_text
    ):
        return "Delivery Issue"

    if "broken" in cleaned_text or "damaged" in cleaned_text or "defective" in cleaned_text:
        return "Product Damage"

    if "return" in cleaned_text or "replace" in cleaned_text or "replacement" in cleaned_text:
        return "Return Request"

    if "login" in cleaned_text or "account" in cleaned_text or "password" in cleaned_text:
        return "Account/Login Issue"

    if "cancel" in cleaned_text or "cancellation" in cleaned_text:
        return "Order Cancellation"

    return "General Query"


def predict_priority(
    text: str,
    category: str,
    sentiment: str,
    previous_complaints: int = 0,
    order_value: float = 0
) -> str:
    previous_complaints = previous_complaints or 0
    order_value = order_value or 0

    model = load_priority_model()

    if model is not None:
        input_data = pd.DataFrame([{
            "message": text,
            "category": category,
            "sentiment": sentiment,
            "previous_complaints": previous_complaints,
            "order_value": order_value,
        }])

        prediction = model.predict(input_data)[0]
        return prediction

    # Fallback rule-based prediction
    if sentiment == "Very Negative" or previous_complaints >= 4:
        return "Critical"

    if category in ["Refund Issue", "Payment Issue", "Product Damage"] and sentiment in ["Negative", "Very Negative"]:
        return "High"

    if sentiment == "Negative" or previous_complaints >= 2:
        return "Medium"

    return "Low"


def predict_csat(
    sentiment: str,
    priority: str,
    category: str = "General Query",
    order_value: float = 0,
    previous_complaints: int = 0,
    response_time_minutes: float = 30,
    resolution_time_hours: float = 24,
) -> int:
    """
    Uses DeepCSAT ANN model if available.
    Falls back to rule-based CSAT if ANN model fails.
    """

    ann_prediction = predict_csat_with_ann(
        category=category,
        priority=priority,
        sentiment=sentiment,
        order_value=order_value,
        previous_complaints=previous_complaints,
        response_time_minutes=response_time_minutes,
        resolution_time_hours=resolution_time_hours,
    )

    if ann_prediction is not None:
        return int(ann_prediction)

    # Fallback rule-based CSAT
    if sentiment == "Very Negative" or priority == "Critical":
        return 1

    if sentiment == "Negative" or priority == "High":
        return 2

    if sentiment == "Neutral" or priority == "Medium":
        return 3

    if sentiment == "Positive" and priority in ["Low", "Medium"]:
        return 5

    return 3


def calculate_risk_score(
    sentiment: str,
    priority: str,
    predicted_csat: int,
    previous_complaints: int = 0
) -> int:
    previous_complaints = previous_complaints or 0
    score = 0

    if sentiment == "Very Negative":
        score += 35
    elif sentiment == "Negative":
        score += 25
    elif sentiment == "Neutral":
        score += 10

    if priority == "Critical":
        score += 30
    elif priority == "High":
        score += 20
    elif priority == "Medium":
        score += 10

    if predicted_csat <= 2:
        score += 25
    elif predicted_csat == 3:
        score += 10

    score += min(previous_complaints * 5, 20)

    return min(score, 100)


def get_escalation_level(priority: str, risk_score: int, predicted_csat: int) -> str:
    if risk_score >= 85 or priority == "Critical":
        return "Urgent Escalation"

    if risk_score >= 70 or predicted_csat <= 2:
        return "Manager Level"

    if risk_score >= 50:
        return "Senior Agent"

    return "No Escalation"


def calculate_sla_status(priority: str) -> str:
    if priority in ["Critical", "High"]:
        return "At Risk"

    return "On Track"


def generate_suggested_reply(category: str, sentiment: str) -> str:
    templates = {
        "Refund Issue": "We apologize for the inconvenience. Our refund team will verify your payment details and update you shortly.",
        "Payment Issue": "We are sorry for the payment-related issue. Our team will check the transaction status and provide an update soon.",
        "Delivery Issue": "We apologize for the delivery delay. Our logistics team is checking your order status and will update you shortly.",
        "Product Damage": "We are sorry that you received a damaged product. Please share product images so we can help with replacement or refund.",
        "Return Request": "We understand your return request. Our support team will guide you through the return or replacement process.",
        "Account/Login Issue": "We are sorry for the login issue. Please try resetting your password or wait while our team checks your account.",
        "Order Cancellation": "We have received your cancellation request. Our team will check the order status and update you shortly.",
        "General Query": "Thank you for reaching out. Our support team will review your query and respond shortly."
    }

    return templates.get(category, templates["General Query"])


def check_reply_quality(reply_text: str) -> dict:
    text = clean_text(reply_text)
    score = 50
    suggestions = []

    empathy_words = ["sorry", "apologize", "understand", "inconvenience"]
    action_words = ["check", "update", "resolve", "verify", "help"]

    if any(word in text for word in empathy_words):
        score += 20
    else:
        suggestions.append("Add empathy or apology.")

    if any(word in text for word in action_words):
        score += 20
    else:
        suggestions.append("Add a clear next step.")

    if len(text.split()) >= 12:
        score += 10
    else:
        suggestions.append("Make the reply more detailed.")

    return {
        "reply_quality_score": min(score, 100),
        "suggestions": suggestions
    }


def moderate_blog(content: str) -> str:
    text = clean_text(content)

    abusive_words = ["abuse", "stupid", "idiot", "fraud", "scam"]
    spam_words = ["click here", "free money", "http", "www"]

    if len(text.split()) < 10:
        return "Flagged - Too Short"

    if any(word in text for word in abusive_words):
        return "Flagged - Abusive Language"

    if any(word in text for word in spam_words):
        return "Flagged - Spam"

    return "Pending Review"