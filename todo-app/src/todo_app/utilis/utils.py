import re
import hashlib
from typing import Union, Tuple
from dateutil.parser import parse
from dateutil.parser import ParserError
from datetime import datetime, timedelta
import dateparser # type: ignore

DURATION_UNITS = {
    "minutes": ["minutes", "mins", "min" "minute"],
    "hour": ["hours", "hrs", "hour", "hr"],
    "day": ["days", "day", "days"],
    "week": ["weeks", "wks", "week"],
    "month": ["months", "month", "mths"],
    "year": ["yrs", "yr", "years", "year"],
}

# regex pattern to extract relative time units
DURATION_PATTERN = re.compile(
    r'(?<!\bin\s)(\d+)\s*(minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\b',
    re.IGNORECASE
)

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

def convert_datestring(date: str) -> Union[Tuple[bool, str], Tuple[bool, datetime]]:
    """convert a date string to datetime value.
        args:
            date: an extracted date like string
        returns:
            bool: True or False
            date: converted date string in datetime datatype
            err: error message
    """
    # initialise current time
    current_time = datetime.now()

    # normalize date string
    normalised_date = normalize_duration_string(date)

    # convert date_string to datetime
    # Check for phrases like "2 hours", "in 30 minutes"
    match = DURATION_PATTERN.search(normalised_date)
    
    # convert to date time is normalised_date is like 2 hour, 2 minutes, 1 year etc
    if match:
        num, unit = match.groups()  # unpacking value and time unit from match eg num = 1, unit = hour
        num = int(num)  # convert value (num) to integer

        # map to timedelta
        unit = unit.lower()
        if "min" in unit:
            delta = timedelta(minutes=num)
        elif "hour" in unit:
            delta = timedelta(hours=num)
        elif "day" in unit:
            delta = timedelta(days=num)
        elif "week" in unit:
            delta = timedelta(weeks=num)
        elif "month" in unit:
            delta = timedelta(days=30 * num)
        elif "year" in unit:
            delta = timedelta(days=365 * num)
        else:
            delta = timedelta()
        
        # calculate date/time
        date = current_time + delta

        # return True, date
        return True, date
    
    # convert other form of task time
    try:
        convert_date = parse(date)

    except (ParserError, ValueError):
        try:
            convert_date = dateparser.parse(
                date, 
                settings={
                    "PREFER_DATES_FROM": "future", 
                    "RELATIVE_BASE": current_time,
                    "RETURN_AS_TIMEZONE_AWARE": False,
                }
            )

            if convert_date is None:
                err = f'❌  Unable to convert {date} to datetime object'
                return False, err
            
        except Exception as e:
            err = str(e)
            return False, err
    
    # date return format year-month-day
    date = ensure_future(convert_date)
    return True, date


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