import re
from datetime import datetime, timedelta

DURATION_UNITS = {
    "minutes": ["minutes", "mins", "min" "minute"],
    "hr": ["hours", "hrs", "hour", "hr"],
    "day": ["days", "day", "days"],
    "week": ["weeks", "wks", "week"],
    "month": ["months", "month", "mths"],
    "year": ["yrs", "yr", "years", "year"],
}

time_unit_pattern = re.compile(r'^(?P<num>\d+)\s*(?P<unit>[a-zA-Z]+)$')

def normalize_duration_string(date: str) -> str:
    """
    Turn "2 hour" -> "in 2 hours", "1hr" -> "in 1 hours", "30 mins" -> "in 30 minutes".
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
            return f"in {digit} {normalised_unit}"

    return time

def ensure_future(convert_date: datetime) -> datetime:
    """Ensure that date is always in future time"""

    now = datetime.now()
    if convert_date < now:

        # If it's today but earlier, assume tomorrow
        if convert_date.date() == now.date():
            convert_date += timedelta(days=1)

        # If it's a weekday or relative date that still landed in the past, bump by a week
        elif (now - convert_date).days < 7:
            convert_date += timedelta(days=7)
    return convert_date


if __name__ == '__main__':
    sample = '40 minutes'

    check_ = normalize_duration_string(sample)
    print(check_)