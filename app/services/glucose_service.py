from app.core.dependencies import get_glucose_provider
import datetime


from app.events.events import timer_ticked_event
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.models.glucose import Glucose


# subscribe to event
@timer_ticked_event.connect
def sync_latest_dexcom_data(sender, **kwargs):
    print(f"[{datetime.datetime.now()}] Event caught! Fetch data from glucose provider and publish event.")
    provider: IGlucoseProvider = get_glucose_provider()
    latest_data: Glucose = provider.fetch_latest_reading()
    if latest_data:
        print(latest_data)
    else:
        print("No new data.")