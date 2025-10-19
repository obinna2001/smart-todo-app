import re
from email_validator import validate_email, EmailNotValidError, ValidatedEmail
from typing import Union, Tuple


def valid_email(email_address: str) -> Union[ValidatedEmail, str]:
    """check is an email address is valid.
    args:
        email_address: a potential email address in string format
    return:
        email: a valid email address in ValidatedEmail datatype
        err: error message
    """
    try:
        email = validate_email(email_address)
        return email
    except EmailNotValidError:
        return "❌  Invalid Email address"


def valid_priority_level(priority: str) -> Tuple[bool, str]:
    """Check if task priority level is a valid input.
    args:
        priority: priority from user input.
    return:
        Tuple[bool, str]:
            - (True, success_message) if valid
            - (False, error_message) if invalid
    """

    priority_validator = re.compile(r"\b(high|low|mild)\b", re.IGNORECASE)

    # check if priority is high, low or mild
    check = priority_validator.search(priority)

    if check:
        mssg = "✔️  Priority level is valid"
        return True, mssg
    else:
        err = (
            "❌  Invalid Priority Level. Priority Level are high, mild and low"
        )
        return False, err


def valid_status(status: str) -> Tuple[bool, str]:
    """check if task status is a valid input.
    args:
        status: task status from user input.
    return:
        bool: True or False
        mssg: success message
        err: error message
    """
    status_validator = re.compile(
        r"\b(complete|inprogress|incomplete)\b", re.IGNORECASE
    )

    # check if priority is high, low or mild
    check = status_validator.search(status)

    if check:
        mssg = "✔️  Task Status is valid"
        return True, mssg
    else:
        err = "❌  Invalid Status. Status Incomplete, Inprogress and Complete"
        return False, err
