from fastapi import FastAPI
from app.api import plans_router
from app.db.session import init_db
from app.core.scheduler import scheduler

app = FastAPI()

app.include_router(plans_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    init_db()
    scheduler.start()

@app.get("/")
def read_root():
    return {"message": "Backend is up and running!"}
