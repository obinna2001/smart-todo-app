import re
from dateutil.parser import parse
from dateutil.parser import ParserError
from datetime import datetime, timedelta
import dateparser # type: ignore
from typing import Tuple, Union
from email_validator import ValidatedEmail # type: ignore

from todo_app.utilis.utils import normalize_duration_string, ensure_future
from todo_app.parsers.validator import valid_email

# regex pattern to extract date from task description
DATE_PATTERN = re.compile(
    r'\b('
    r'(?:\d{1,2}\s*(?:am|pm))|'  # 3pm, 4am
    r'(?:\d+\s*(?:minute|minutes|day|days|week|weeks|month|months|year|years|mins|hr|hrs|hour|hours)s?)|'  # 30 minutes, 2 weeks
    r'(?:tomorrow|today|tonight|'
    r'(?:next|last)\s+(?:week|month|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday))|'
    r'(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|'
    r'(?:\b\d{4}-\d{2}-\d{2}\b)|'  # 2025-01-14
    r'(?:\b\d{1,2}[-/](?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[-/]\d{2,4}\b)|'  # 01-feb-25, 1/Jan/2024
    r'(?:\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s*\d{4})?\b)|'  # July 2nd 2025
    r'(?:\b\d{1,2}(?:st|nd|rd|th)?\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)(?:\s+\d{4})?\b)|'  # 1st February, 2 February, 2nd January 2025
    r'(?:\b\d{1,2}/\d{1,2}/\d{4}\b)|'  # 23/02/2026
    r'(?:\b\d{4}/\d{1,2}/\d{1,2}\b)|'  # 2026/02/23
    r'(?:\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s*\d{4})?\b)'  # Feb 1st, 2025
    r')\b',
    re.IGNORECASE
)

# regex pattern to extract relative time units
DURATION_PATTERN = re.compile(
    r'(?<!\bin\s)(\d+)\s*(minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\b',
    re.IGNORECASE
)

# regex pattern to extract priority level from task description
PRIORITY_PATTERN = re.compile(r"#(\w+)(?=.*\bdue\b)", re.IGNORECASE)

# regex pattern to extract tag from task description
TAG_PATTERN = re.compile(r"@([^#]+?)#", re.IGNORECASE)

# regex pattern to extract email from task description
EMAIL_PATTERN = re.compile(r"assigned:([^\s]+)", re.IGNORECASE)


def extract_task(task_description: str) -> Tuple[bool, str]:
    """Extract task priority level from task descriptions.
        args:
            task_description: User task descriptin contain a message eg buy groceries, watch man utd vs liverpool game
        return:
            task: extracted task in a string format
            bool: True, False
            err = error message
    """
    task_match = re.match(r"^(.*?)@", task_description)
    
    # check if task if present in task descritption
    if not task_match:
        err = 'Task not Found!'
        return False, err
    
    # return task if found
    task = task_match.group(1).strip().title()  # extract clean and normalize task
    return True, task


def extract_priority_level(task_description: str) -> Tuple[bool, str]:
    """Extract task priority level from task descriptions.
        args:
            task_description: User task descriptin contain a task priority level eg #high, #low and #mild
        return:
            bool: True, False
            priority_level: extracted priority level in a string format
            err: error message
    """
    # extract priority level from task description
    priority_matches = PRIORITY_PATTERN.findall(task_description)
    
    # return None is priority level not found
    if not priority_matches:
        err = 'Task Priority level not found!'
        return False, err
    
    # strip priority level of empty space
    task_priority = priority_matches[0].strip()
    
    # convert priority level to title case
    task_priority = task_priority.title()
    
    # return extracted priority level
    return True, task_priority

def extract_tag(task_description: str) -> Tuple[bool, str]:
    """Extract task tag from task decsription.
        args:
            task_description: User task descriptin contain a task tag eg #shopping, #religion, #relaxation, #worship etc
        return:
            tag: task tag eg WORSHIP, SCHOOL etc
            err: error message
            bool: True, False
    """
    # extract tag from task description
    tag_matches = TAG_PATTERN.search(task_description)

    # check if valid tag is found
    if not tag_matches:
        err = 'Task Tag not found!'
        return False, err
    
    # extract and strip tag of whitespace if valid tag is found
    tag_match = tag_matches.group(1).strip()
    
    # convert tag to upper case
    tag = tag_match.upper()
    
    # return extracted tag
    return True, tag

def extract_email(task_description: str) -> Tuple[bool, str]:
    """Extract task email from task decsription.
        args:
            task_description: User task descriptin contain a task email
        return:
            email: A valid email address eg mark20@gmail.com, kenbrave198@email.com
            bool: True, False
            err: error message
    """

    # extract valid email string from the task description
    email_matches = EMAIL_PATTERN.findall(task_description)
    
    # check if email is found in task description
    if not email_matches:
        err = 'Email not found. '
        return False, err
    
    # extract and strip email of whitespaces
    email = email_matches[0].strip()

    # check if email is valid
    valid_mail = valid_email(email)

    if isinstance(valid_mail, ValidatedEmail):
        email = valid_mail.email  # convert valid_mail to str
        return True, email
    
    elif isinstance(valid_mail, str):
        err = valid_mail
        return False, err

def extract_date(task_description: str) -> Union[Tuple[bool, datetime], Tuple[bool, str]]:
    """Extract valid date like format from task description, convert it to a datetime object and format it into a defined string output.
       args:
            task_description: User task description containing a valid date-like value eg. Tomorrow, yesterday, 3pm, monday e.t.c
        returns:
           date: A valid datetime object
           bool: True, False
           err: error message
    """
    # current time
    current_time = datetime.now()

    # extract valid date-like string from task_description
    date_matches = DATE_PATTERN.findall(task_description)
    
    # check if date match is found
    if not date_matches:
        err = "Invalid or No date found in task description"
        return False, err
    
    # extract date string
    date_string = date_matches[0].strip()

    # normalize date string
    normalised_date = normalize_duration_string(date_string)

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
    
    # convert other form of task description time
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
                err = f'Unable to convert {date_string} to datetime object'
                return False, err
            
        except Exception as e:
            err = str(e)
            return False, err
    
    # date return format year-month-day
    return True, ensure_future(convert_date)
