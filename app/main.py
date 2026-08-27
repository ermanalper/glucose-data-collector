from contextlib import asynccontextmanager

import uvicorn

from app.infrastructure.persistence.entities import glucose_orm
from fastapi import FastAPI
import app.services.glucose_service
import app.services.storage_service
from app.infrastructure.persistence.database import Base, engine
from app.services.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 5-minutes timer
    start_scheduler()

    yield

    # codes that run before the api shutting down. (close db connection etc)
    print("FastAPI app shutting down...")


Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"App running..."}

