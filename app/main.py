from contextlib import asynccontextmanager
import uvicorn
from starlette.responses import JSONResponse

from app.api.routers import glucose_router, insulin_router, meal_router, stream_router, alarm_router, test_client_router
from app.api.security import verify_api_key
from app.core.dependencies import get_glucose_service, get_insulin_service, get_meal_service, get_alarm_service, \
    get_test_clients_service
from app.core.exceptions import ResourceNotFoundException, DatabaseError
from app.infrastructure.persistence.entities import glucose_orm
from app.infrastructure.persistence.entities import insulin_orm
from fastapi import FastAPI, Request, Depends
import app.services.glucose_service
from app.infrastructure.persistence.database import Base, engine
from app.services.scheduler import start_scheduler
from app.services.push_glucose_to_sse import push_glucose_to_sse
from app.services.push_alarm_to_sse import push_set_alarm_to_sse, push_reset_alarm_to_sse, reset_alarms_of_user_event
from app.services.push_test_client_to_sse import push_reset_alarm_to_sse
def _init_services():
    get_glucose_service()
    get_insulin_service()
    get_meal_service()
    get_alarm_service()
    get_test_clients_service()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 5-minutes timer
    start_scheduler()

    _init_services()

    yield

    # codes that run before the api shutting down. (close db connection etc)
    print("FastAPI app shutting down...")


Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)

'''
If you don't want to add an API secret key to your backend, you may use the following router
initializations
app.include_router(glucose_router.router)
app.include_router(insulin_router.router)
app.include_router(meal_router.router)
'''
app.include_router(glucose_router.router, dependencies=[Depends(verify_api_key)])
app.include_router(insulin_router.router, dependencies=[Depends(verify_api_key)])
app.include_router(meal_router.router, dependencies=[Depends(verify_api_key)])
app.include_router(alarm_router.router, dependencies=[Depends(verify_api_key)])
app.include_router(test_client_router.router, dependencies=[Depends(verify_api_key)])


app.include_router(stream_router.router, dependencies=[Depends(verify_api_key)])

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


@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    status_code = 409 if "already" in exc.message else 400

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error_type": "DATABASE_ERROR",
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
