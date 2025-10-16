import re
from datetime import datetime, timedelta
import hashlib

DURATION_UNITS = {
    "minutes": ["minutes", "mins", "min" "minute"],
    "hour": ["hours", "hrs", "hour", "hr"],
    "day": ["days", "day", "days"],
    "week": ["weeks", "wks", "week"],
    "month": ["months", "month", "mths"],
    "year": ["yrs", "yr", "years", "year"],
}

time_unit_pattern = re.compile(r'^(?P<num>\d+)\s*(?P<unit>[a-zA-Z]+)$')

def normalize_duration_string(date: str) -> str:
    """
    Turn "2 hours" -> "2 hour", "1hr" -> "1 hour", "30 mins" -> "30 minutes".
    Returns normalized string or original if not a pure duration.
    args:
        date: a date-like string
    return:
        num: number in string format
        unit: valid unit of time
    """
    time = date.strip().lower()

    time_unit = time_unit_pattern.findall(time)
    normalised_unit  = ''

    if time_unit:
        digit, unit = time_unit[0]
        for key, value in DURATION_UNITS.items():
            if unit in value:
                normalised_unit = key

        if normalised_unit:
            return f"{digit} {normalised_unit}"

    return time

def ensure_future(convert_date: datetime) -> datetime:
    """Ensure that date is always in future time and not in past.
    args:
        convert_date: task description time in datetime datatype
    return:
        convert_date: processed convert_date
    """    
    # initialise current time
    now = datetime.now()

    if convert_date < now:
        # If it's today but earlier, assume the date to betomorrow
        if convert_date.date() == now.date():
            convert_date += timedelta(days=1)

        # If it's a weekday or relative date that still landed in the past, increase it by a week
        elif (now - convert_date).days < 7:
            convert_date += timedelta(days=7)
        
        # if month is less than current month increase it by 1 year
        elif (now.month > convert_date.month):
            convert_date += timedelta(days=365)

    return convert_date

def generate_taskID(task_description: str) -> str:
    """Generate a unique id for each user task based on task description and time of creation
        args:
            task_description: user task
        return:
            task_id = task unique id
    """
    # generate current time
    current_time = datetime.now()

    # convert time to str
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # concatenate task_description and timestamp to generate unique id_text
    id_text = task_description + timestamp
    
    # transform id_text to a SHA256 hash
    id_generator = hashlib.sha256(id_text.encode())
    
    # short id_generator to just 8 characters
    task_id = id_generator.hexdigest()[:8]
    
    # return the generated task id
    return task_id