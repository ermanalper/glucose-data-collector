from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services.scheduler import start_scheduler
import app.services.glucose_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 5-minutes timer
    start_scheduler()

    yield

    # codes that run before the api shutting down. (close db connection etc)
    print("FastAPI app shutting down...")



app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"App running..."}

