from datetime import datetime, time
from time import sleep


def time_check():
    # Get the current time in the desired time zone
    # time_zone = pytz.timezone('Your_Time_Zone_Here')
    current_time = datetime.now().time()

    # Define the time range
    start_time = datetime.strptime('22:00', '%H:%M').time()
    end_time = datetime.strptime('01:00', '%H:%M').time()

    if start_time <= current_time or current_time <= end_time:
        return True
    else:
        return False


while time_check():
    print('run')
    sleep(6)
else:
    print('wait')
    sleep(60)
