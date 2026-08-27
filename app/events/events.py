from blinker import signal

# 5-minutes event
timer_ticked_event = signal('timer-ticked-event')

# glucose data fetched event
new_glucose_data_event = signal('new-glucose-data-event')