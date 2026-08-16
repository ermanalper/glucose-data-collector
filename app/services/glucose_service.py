# app/services/glucose_service.py
from app.events import events
import datetime

from app.events.events import timer_ticked_event


# subscribe to event
@timer_ticked_event.connect
def sync_latest_dexcom_data(sender, **kwargs):
    print(f"[{datetime.datetime.now()}] Event caught! Fetch data from dexcom share and publish event")
