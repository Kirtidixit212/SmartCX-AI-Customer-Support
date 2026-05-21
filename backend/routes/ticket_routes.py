from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Ticket, Reply
from schemas import (
    TicketCreate,
    TicketStatusUpdate,
    TicketAssign,
    TicketFeedback,
    AgentReply,
)

from services.ai_service import (
    analyze_sentiment,
    predict_category,
    predict_priority,
    predict_csat,
    calculate_risk_score,
    get_escalation_level,
    calculate_sla_status,
    generate_suggested_reply,
    check_reply_quality,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/create")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(ticket.message)
    category = predict_category(ticket.message)

    priority = predict_priority(
        text=ticket.message,
        category=category,
        sentiment=sentiment,
        previous_complaints=ticket.previous_complaints,
        order_value=ticket.order_value,
    )

    predicted_csat = predict_csat(
        sentiment=sentiment,
        priority=priority,
        category=category,
        order_value=ticket.order_value,
        previous_complaints=ticket.previous_complaints,
        response_time_minutes=30,
        resolution_time_hours=24,
    )

    risk_score = calculate_risk_score(
        sentiment=sentiment,
        priority=priority,
        predicted_csat=predicted_csat,
        previous_complaints=ticket.previous_complaints,
    )

    escalation_level = get_escalation_level(
        priority=priority,
        risk_score=risk_score,
        predicted_csat=predicted_csat,
    )

    sla_status = calculate_sla_status(priority)
    suggested_reply = generate_suggested_reply(category, sentiment)

    new_ticket = Ticket(
        customer_name=ticket.customer_name,
        email=ticket.email,
        order_id=ticket.order_id,
        product_name=ticket.product_name,
        message=ticket.message,
        channel=ticket.channel,
        order_value=ticket.order_value,
        previous_complaints=ticket.previous_complaints,
        category=category,
        priority=priority,
        sentiment=sentiment,
        predicted_csat=predicted_csat,
        risk_score=risk_score,
        escalation_level=escalation_level,
        sla_status=sla_status,
        suggested_reply=suggested_reply,
        status="Pending",
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created and analyzed successfully",
        "ticket_id": new_ticket.ticket_id,
        "customer_name": new_ticket.customer_name,
        "email": new_ticket.email,
        "order_id": new_ticket.order_id,
        "product_name": new_ticket.product_name,
        "ticket_message": new_ticket.message,
        "category": new_ticket.category,
        "priority": new_ticket.priority,
        "sentiment": new_ticket.sentiment,
        "predicted_csat": new_ticket.predicted_csat,
        "risk_score": new_ticket.risk_score,
        "escalation_level": new_ticket.escalation_level,
        "sla_status": new_ticket.sla_status,
        "suggested_reply": new_ticket.suggested_reply,
        "assigned_agent": new_ticket.assigned_agent,
        "status": new_ticket.status,
    }


@router.get("/all")
def get_all_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).order_by(Ticket.ticket_id.desc()).all()
    return tickets


# This route must stay BEFORE /{ticket_id}
@router.get("/agent/{agent_name}/assigned")
def get_agent_assigned_tickets(agent_name: str, db: Session = Depends(get_db)):
    tickets = (
        db.query(Ticket)
        .filter(Ticket.assigned_agent == agent_name)
        .order_by(Ticket.ticket_id.desc())
        .all()
    )
    return tickets


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.put("/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    status_data: TicketStatusUpdate,
    db: Session = Depends(get_db),
):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = status_data.status

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket status updated successfully",
        "ticket_id": ticket.ticket_id,
        "status": ticket.status,
    }


@router.put("/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    assign_data: TicketAssign,
    db: Session = Depends(get_db),
):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.assigned_agent = assign_data.assigned_agent
    ticket.status = "Assigned"

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket assigned successfully",
        "ticket_id": ticket.ticket_id,
        "assigned_agent": ticket.assigned_agent,
        "status": ticket.status,
    }


@router.post("/{ticket_id}/reply")
def add_reply(
    ticket_id: int,
    reply_data: AgentReply,
    db: Session = Depends(get_db),
):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    quality = check_reply_quality(reply_data.reply_text)

    new_reply = Reply(
        ticket_id=ticket_id,
        agent_name=reply_data.agent_name,
        reply_text=reply_data.reply_text,
        reply_quality_score=quality["reply_quality_score"],
    )

    ticket.status = "In Progress"

    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)

    return {
        "message": "Reply added successfully",
        "ticket_id": ticket_id,
        "reply_quality_score": quality["reply_quality_score"],
        "suggestions": quality["suggestions"],
        "reply": new_reply.reply_text,
        "status": ticket.status,
    }


@router.put("/{ticket_id}/feedback")
def add_csat_feedback(
    ticket_id: int,
    feedback: TicketFeedback,
    db: Session = Depends(get_db),
):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.actual_csat = feedback.actual_csat

    db.commit()
    db.refresh(ticket)

    return {
        "message": "CSAT feedback saved successfully",
        "ticket_id": ticket.ticket_id,
        "predicted_csat": ticket.predicted_csat,
        "actual_csat": ticket.actual_csat,
    }