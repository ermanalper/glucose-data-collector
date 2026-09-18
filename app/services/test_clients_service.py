from app.events.events import run_test_client_protocol_event
from app.infrastructure.interfaces.test_clients_service_interface import ITestClientsService


class TestClientsServiceImpl(ITestClientsService):
    def run_client_test_protocols(self, client_name: str):
        run_test_client_protocol_event.send(client_name=client_name)