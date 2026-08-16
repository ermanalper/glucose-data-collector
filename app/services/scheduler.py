from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.events.events import timer_ticked_event

scheduler = AsyncIOScheduler()

FETCH_IN_MINUTES = 5

def timer_interrupt_handler():
    # publish event
    timer_ticked_event.send('system_scheduler', message="Timer interrupt")

def start_scheduler():
    # set the timer up
    scheduler.add_job(timer_interrupt_handler, 'interval', minutes=FETCH_IN_MINUTES)
    scheduler.start()