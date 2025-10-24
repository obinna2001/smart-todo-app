import re
from email_validator import validate_email, EmailNotValidError, ValidatedEmail # type: ignore
from typing import Union, Tuple

class Validator:
    """A class to validate different components of a todo task."""

    @staticmethod
    def valid_email(email_address: str) -> Union[ValidatedEmail, str]:
        """check is an email address is valid.
        args:
            email_address: a potential email address in string format
        return:
            email: a valid email address in ValidatedEmail datatype
            err: error message
        """
        try:
            email = validate_email(email_address, check_deliverability=True)
            return email
        except EmailNotValidError:
            return "Invalid Email address"
    
    @staticmethod
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
        priority_match = priority_validator.search(priority)

        # valid priority level
        if priority_match:
            return True, "Priority level is valid"

        return False, "Invalid Priority Level. Priority Level are high, mild and low"

    @staticmethod
    def valid_status(status: str) -> Tuple[bool, str]:
        """check if task status is a valid input.
        args:
            status: task status from user input.
        return:
            Tuple[bool, str]:
                - (True, success_message) if valid
                - (False, error_message) if invalid
        """
        status_validator = re.compile(r"\b(complete|inprogress|incomplete)\b", re.IGNORECASE)

        # check if priority is high, low or mild
        check = status_validator.search(status)

        # valid status level
        if not check:
            return False, "Invalid or no task status given. Valid status are; Incomplete, Inprogress and Complete"
        
        return True, "Valid Task Status"
