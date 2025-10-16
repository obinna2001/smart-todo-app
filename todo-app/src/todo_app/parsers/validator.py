from email_validator import validate_email, EmailNotValidError, ValidatedEmail
from typing import Union

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