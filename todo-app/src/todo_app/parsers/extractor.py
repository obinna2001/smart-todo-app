import re
from dateutil.parser import parse
from dateutil.parser import ParserError
from datetime import datetime, timedelta
import dateparser # type: ignore
import copy

from todo_app.utilis.parser_utilis import normalize_duration_string, ensure_future

DATE_PATTERN = re.compile(
    r'\b('
    r'(?:\d{1,2}\s*(?:am|pm))|' # 3pm, 4am
    r'(?:\d+\s*(?:minute|minutes|day|days|week|weeks|month|months|year|years|mins|hr|hrs|hour|hours)s?)|'  # 30 minutes, 2 weeks
    r'(?:tomorrow|today|tonight|' # relative words
    r'(?:next|last)\s+(?:week|month|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday))|'  
    r'(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|' # weekdays
    r'(?:\b\d{4}-\d{2}-\d{2}\b)|' # 2025-01-14 (ISO format)
    r'(?:\b\d{1,2}[-/](?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[-/]\d{2,4}\b)|' # 01-feb-25, 1/Jan/2024
    r'(?:\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s*\d{4})?\b)' # July 2nd 2025
    r')\b',
    re.IGNORECASE
)

DURATION_PATTERN = re.compile(
    r'\bin\s+(\d+)\s*(minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\b',
    re.IGNORECASE
)

PRIORITY_PATTERN = re.compile(r"#(\w+)(?=.*\bdue\b)", re.IGNORECASE)

TAG_PATTERN = re.compile(r"@([^#]+?)#", re.IGNORECASE)

EMAIL_PATTERN = re.compile(r"assigned:([^\s]+)", re.IGNORECASE)


def extract_priority_level(task_description: str) -> str:
    """Extract task priority level from task descriptions.
    args:
        task_description: User task descriptin contain a task priority level eg #high, #low and #mild
    return:
        priority_level: extracted priority level in a string format
    """

    priority_matches = PRIORITY_PATTERN.findall(task_description)

    if not priority_matches:
        print('No priority level found in task')
        return None
    
    task_priority = priority_matches[0].strip()

    task_priority = task_priority.title()

    return task_priority

def extract_tag(task_description: str) -> str:
    tag_matches = TAG_PATTERN.search(task_description)
    if not tag_matches:
        print()
        return None
    
    return tag_matches.group(1).strip().title()

def extract_email(task_description: str) -> str:
    email_matches = EMAIL_PATTERN.findall(task_description)

    if not email_matches:
        print()
        return None
    
    return email_matches[0].strip()


def extract_date(task_description: str) -> datetime:
    """Extract valid date like format from task description, convert it to a datetime object and format it into a defined string output.
    args:
        task_description: User task description containing a valid date-like value eg. Tomorrow, yesterday, 3pm, monday e.t.c
    returns:
       date: A valid datetime object
    """
    # current time
    current_time = datetime.now()


    # extract valid date-like string from task_description
    date_matches = DATE_PATTERN.findall(task_description)
    
    # check if date match is found
    if not date_matches:
        print("No Date or Time value found")
        return None
    
    # extract date string
    date_string = date_matches[0].strip()

    # normalize date string
    normalised_date = normalize_duration_string(date_string)

    # convert date_string to datetime
    # Check for phrases like "in 2 hours", "in 30 minutes"
    match = DURATION_PATTERN.search(normalised_date)
    if match:
        num, unit = match.groups()
        num = int(num)

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

        return current_time + delta  # Always convert forward

    try:
        convert_date = parse(date_string)
    except (ParserError, ValueError):
        try:
            convert_date = dateparser.parse(
                date_string, 
                settings={
                    "PREFER_DATES_FROM": "future", 
                    "RELATIVE_BASE": current_time,
                    "RETURN_AS_TIMEZONE_AWARE": False,
                }
            )

            if convert_date is None:
                return None
            
        except Exception:
            return None
    
    return ensure_future(convert_date)


sample = "Buy groceries @shopping #high due:5 years assigned:alice@example.com"

print(datetime.now())
date = extract_date(sample)
print(f'extracted_date: {date}')
priority_level = extract_priority_level(sample)
print(f'extracted priority level: {priority_level}')
tag = extract_tag(sample)
print(f'extracted tag: {tag}')
email = extract_email(sample)
print(f'extracted email: {email}')