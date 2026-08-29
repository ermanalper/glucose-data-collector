from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.events.events import timer_ticked_event
from app.core.config import FETCH_IN_MINUTES, IS_DEVELOPMENT

scheduler = AsyncIOScheduler()

def timer_interrupt_handler():
    # publish event
    print("Timer ticked")
    timer_ticked_event.send('system_scheduler', message="Timer interrupt")

def start_scheduler():
    # set the timer up
    if IS_DEVELOPMENT:
        scheduler.add_job(timer_interrupt_handler, 'interval', seconds=2)
    else:
        scheduler.add_job(timer_interrupt_handler, 'interval', minutes=FETCH_IN_MINUTES)
    scheduler.start()