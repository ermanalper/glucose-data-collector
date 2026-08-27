from app.core.dependencies import get_glucose_provider
import datetime


from app.events.events import timer_ticked_event, new_glucose_data_event
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
        new_glucose_data_event.send('glucose_service', glucose_data=latest_data) #publish glucose data
    else:
        print("No new data.")