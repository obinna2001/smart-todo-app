from email_validator import validate_email, EmailNotValidError, ValidatedEmail
from typing import Union
import re

priority_validator = re.compile(r"\b(high|low|mild)\b", re.IGNORECASE)

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
        return 'Invalid Email address'
    

def valid_priority_level(priority: str) -> bool:
    """check is priority level is a valid input.
        args: 
            priority: priority from user input.
        return:
            bool: True or False
    """
    # check if priority is high, low or mild
    check = priority_validator.search(priority)

    if check:
        return True       
    else:
        return False