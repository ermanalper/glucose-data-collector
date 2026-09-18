from fastapi import APIRouter, Depends

from app.core.dependencies import get_test_clients_service
from app.infrastructure.interfaces.test_clients_service_interface import ITestClientsService

router = APIRouter(prefix="/api/v1/clients", tags=["Test Clients"])

@router.post("/test-client")
def run_client_test_protocol(
        client_name: str,
        service: ITestClientsService = Depends(get_test_clients_service)
):
    service.run_client_test_protocols(client_name=client_name)