from abc import ABC, abstractmethod


class ITestClientsService(ABC):
    @abstractmethod
    def run_client_test_protocols(self, client_name: str):
        pass