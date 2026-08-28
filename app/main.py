from contextlib import asynccontextmanager
import uvicorn
from starlette.responses import JSONResponse

from app.api.routers import glucose_router
from app.core.exceptions import ResourceNotFoundException
from app.infrastructure.persistence.entities import glucose_orm
from fastapi import FastAPI, Request
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
app.include_router(glucose_router.router)

@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error_type": "NOT_FOUND",
            "message": exc.message,
            "path": request.url.path
        }
    )
@app.get("/")
async def root():
    return {"App running..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
