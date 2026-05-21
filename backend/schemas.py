from pydantic import BaseModel, EmailStr
from typing import Optional


class TicketCreate(BaseModel):
    customer_name: str
    email: EmailStr
    order_id: Optional[str] = None
    product_name: Optional[str] = None
    message: str
    channel: Optional[str] = "Web"
    order_value: Optional[float] = 0
    previous_complaints: Optional[int] = 0


class TicketStatusUpdate(BaseModel):
    status: str


class TicketAssign(BaseModel):
    assigned_agent: str


class TicketFeedback(BaseModel):
    actual_csat: int


class AgentReply(BaseModel):
    ticket_id: int
    agent_name: str
    reply_text: str


class BlogCreate(BaseModel):
    customer_name: str
    title: str
    content: str
    rating: int
    order_id: Optional[str] = None
    product_name: Optional[str] = None


class BlogStatusUpdate(BaseModel):
    admin_status: str


class KnowledgeCreate(BaseModel):
    title: str
    category: str
    content: str
    tags: Optional[str] = None
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: str    