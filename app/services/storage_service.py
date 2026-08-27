from app.core.dependencies import get_glucose_repository
from app.events.events import new_glucose_data_event


@new_glucose_data_event.connect
def handle_new_glucose_data(sender, **kwargs):
    glucose_data = kwargs.get('glucose_data')

    if glucose_data:
        repo = get_glucose_repository()
        repo.save(glucose_data) #write to database