from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import plans_router
from app.db.session import init_db
from app.core.scheduler import scheduler

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plans_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    init_db()
    scheduler.start()

@app.get("/")
def read_root():
    return {"message": "Backend is up and running!"}
