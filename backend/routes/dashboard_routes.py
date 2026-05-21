from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Ticket, Blog

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/admin")
def admin_dashboard(db: Session = Depends(get_db)):
    total_tickets = db.query(Ticket).count()
    pending_tickets = db.query(Ticket).filter(Ticket.status == "Pending").count()
    resolved_tickets = db.query(Ticket).filter(Ticket.status == "Resolved").count()

    high_priority_tickets = db.query(Ticket).filter(
        Ticket.priority.in_(["High", "Critical"])
    ).count()

    negative_tickets = db.query(Ticket).filter(
        Ticket.sentiment.in_(["Negative", "Very Negative"])
    ).count()

    tickets = db.query(Ticket).all()

    if len(tickets) > 0:
        average_csat = sum((ticket.predicted_csat or 0) for ticket in tickets) / len(tickets)
    else:
        average_csat = 0

    if total_tickets > 0:
        negative_sentiment_percent = round((negative_tickets / total_tickets) * 100, 2)
    else:
        negative_sentiment_percent = 0

    sla_breaches = db.query(Ticket).filter(Ticket.sla_status == "Breached").count()
    pending_blog_approvals = db.query(Blog).filter(Blog.admin_status == "Pending").count()

    return {
        "total_tickets": total_tickets,
        "pending_tickets": pending_tickets,
        "resolved_tickets": resolved_tickets,
        "high_priority_tickets": high_priority_tickets,
        "average_csat": round(average_csat, 2),
        "negative_sentiment_percent": negative_sentiment_percent,
        "sla_breaches": sla_breaches,
        "pending_blog_approvals": pending_blog_approvals
    }


@router.get("/ticket-category")
def ticket_category_chart(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    category_counts = {}

    for ticket in tickets:
        category = ticket.category or "Unknown"
        category_counts[category] = category_counts.get(category, 0) + 1

    return category_counts


@router.get("/sentiment")
def sentiment_chart(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    sentiment_counts = {}

    for ticket in tickets:
        sentiment = ticket.sentiment or "Unknown"
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1

    return sentiment_counts


@router.get("/blog-analytics")
def blog_analytics(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()

    total_blogs = len(blogs)
    approved_blogs = len([blog for blog in blogs if blog.admin_status == "Approved"])
    pending_blogs = len([blog for blog in blogs if blog.admin_status == "Pending"])
    rejected_blogs = len([blog for blog in blogs if blog.admin_status == "Rejected"])

    if len(blogs) > 0:
        average_rating = sum((blog.rating or 0) for blog in blogs) / len(blogs)
    else:
        average_rating = 0

    sentiment_distribution = {}

    for blog in blogs:
        sentiment = blog.sentiment or "Unknown"
        sentiment_distribution[sentiment] = sentiment_distribution.get(sentiment, 0) + 1

    return {
        "total_blogs": total_blogs,
        "approved_blogs": approved_blogs,
        "pending_blogs": pending_blogs,
        "rejected_blogs": rejected_blogs,
        "average_rating": round(average_rating, 2),
        "sentiment_distribution": sentiment_distribution
    }
@router.get("/agent/{agent_name}")
def agent_dashboard(agent_name: str, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.assigned_agent == agent_name).all()

    assigned_tickets = len(tickets)

    high_priority_tickets = len([
        ticket for ticket in tickets
        if ticket.priority in ["High", "Critical"]
    ])

    resolved_tickets = len([
        ticket for ticket in tickets
        if ticket.status == "Resolved"
    ])

    if tickets:
        average_csat = sum((ticket.predicted_csat or 0) for ticket in tickets) / len(tickets)
    else:
        average_csat = 0

    return {
        "agent_name": agent_name,
        "assigned_tickets": assigned_tickets,
        "high_priority_tickets": high_priority_tickets,
        "resolved_tickets": resolved_tickets,
        "average_csat": round(average_csat, 2)
    }