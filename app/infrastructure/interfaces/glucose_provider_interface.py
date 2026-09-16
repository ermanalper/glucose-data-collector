from abc import ABC, abstractmethod

from app.core.exceptions import AmbiguousFunctionCallException
from app.models.glucose import Glucose

'''
PULL CLIENTS:
    A pull client is a glucose provider implementation that fetches the glucose data from a remote repo, e.g. Nightscout
    These pull clients fetch data with each timer tick, and publish new glucose data event

PUSH CLIENTS:
    A push client gets the data posted to this backend using the relevant endpoint, 
    and then publishes the new glucose data event
'''

class IGlucoseProvider(ABC):
   pass

class IPullClient(IGlucoseProvider):
    @abstractmethod
    def fetch_latest_reading(self, sender=None, **kwargs) -> Glucose:
        raise AmbiguousFunctionCallException(
            "This function can only be used by 'pull clients'. If this exception is raised, then, "
            "it is not overridden in the currently set client (it is a push client)."
            "See the notes at glucose_provider_interface.py for further information")

class IPushClient(IGlucoseProvider):
    @abstractmethod
    def process_pushed_data(self, **kwargs):
        raise AmbiguousFunctionCallException(
            "This function can only be used by 'push clients'. If this exception is raised, then, "
            "it is not overridden in the currently set client (it is a pull client)."
            "See the notes at glucose_provider_interface.py for further information")
