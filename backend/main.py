from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import ticket_routes, blog_routes, dashboard_routes
from routes import ticket_routes, blog_routes, dashboard_routes, auth_routes
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartCX API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket_routes.router)
app.include_router(blog_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
def home():
    return {
        "message": "SmartCX backend with database is running successfully"
    }