from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database import get_db
from models import Blog
from schemas import BlogCreate, BlogStatusUpdate
from services.ai_service import analyze_sentiment, predict_category, moderate_blog

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post("/create")
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(blog.content)
    predicted_category = predict_category(blog.content)
    moderation_status = moderate_blog(blog.content)

    new_blog = Blog(
        customer_name=blog.customer_name,
        title=blog.title,
        content=blog.content,
        rating=blog.rating,
        order_id=blog.order_id,
        product_name=blog.product_name,
        predicted_category=predicted_category,
        sentiment=sentiment,
        moderation_status=moderation_status,
        admin_status="Pending"
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return {
        "message": "Blog submitted successfully and sent for admin approval",
        "blog_id": new_blog.blog_id,
        "customer_name": new_blog.customer_name,
        "title": new_blog.title,
        "rating": new_blog.rating,
        "predicted_category": new_blog.predicted_category,
        "sentiment": new_blog.sentiment,
        "moderation_status": new_blog.moderation_status,
        "admin_status": new_blog.admin_status
    }


@router.get("/all")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).order_by(Blog.blog_id.desc()).all()
    return blogs


@router.get("/public")
def get_public_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).filter(Blog.admin_status == "Approved").order_by(Blog.blog_id.desc()).all()
    return {
        "blogs": blogs
    }


@router.get("/{blog_id}")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.blog_id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


@router.put("/{blog_id}/status")
def update_blog_status(
    blog_id: int,
    status_data: BlogStatusUpdate,
    db: Session = Depends(get_db)
):
    blog = db.query(Blog).filter(Blog.blog_id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.admin_status = status_data.admin_status

    if status_data.admin_status == "Approved":
        blog.approved_at = func.now()

    db.commit()
    db.refresh(blog)

    return {
        "message": "Blog status updated successfully",
        "blog_id": blog.blog_id,
        "admin_status": blog.admin_status
    }