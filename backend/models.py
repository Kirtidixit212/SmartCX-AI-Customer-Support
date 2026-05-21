from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func

from database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    order_id = Column(String(50), nullable=True)
    product_name = Column(String(150), nullable=True)
    message = Column(Text, nullable=False)
    channel = Column(String(50), default="Web")
    order_value = Column(Float, default=0)
    previous_complaints = Column(Integer, default=0)

    category = Column(String(100))
    priority = Column(String(50))
    sentiment = Column(String(50))
    predicted_csat = Column(Integer)
    actual_csat = Column(Integer, nullable=True)

    risk_score = Column(Float)
    escalation_level = Column(String(100))
    sla_status = Column(String(50), default="On Track")
    suggested_reply = Column(Text)

    assigned_agent = Column(String(100), nullable=True)
    status = Column(String(50), default="Pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)


class Blog(Base):
    __tablename__ = "blogs"

    blog_id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    order_id = Column(String(50), nullable=True)
    product_name = Column(String(150), nullable=True)

    predicted_category = Column(String(100))
    sentiment = Column(String(50))
    moderation_status = Column(String(100))
    admin_status = Column(String(50), default="Pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)


class Reply(Base):
    __tablename__ = "replies"

    reply_id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(Integer, nullable=False)
    agent_name = Column(String(100), nullable=False)
    reply_text = Column(Text, nullable=False)
    reply_quality_score = Column(Float, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    article_id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())