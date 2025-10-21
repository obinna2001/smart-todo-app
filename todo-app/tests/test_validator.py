from todo_app.parsers.validator import Validator

validator = Validator()

def test_valid_email():
    email = "okeyobinna2001@gmail.com"
    result = validator.valid_email(email)
    assert result.normalized == email

def test_invalid_email():
    email = "zubimobinnaokechukwu@gmail..com"
    result = validator.valid_email(email)
    assert result == "Invalid Email address"

def test_valid_priority_level():
    priority = "High"
    is_valid, message = validator.valid_priority_level(priority)
    assert is_valid is True
    assert message == "Priority level is valid"

def test_invalid_priority_level():
    priority = "Urgent"
    is_valid, message = validator.valid_priority_level(priority)
    assert is_valid is False
    assert message == "Invalid Priority Level. Priority Level are high, mild and low"

def test_valid_status():
    status = "Complete"
    is_valid, message = validator.valid_status(status)
    assert is_valid is True
    assert message == "Valid Task Status"

def test_invalid_status():
    status = "Done"
    is_valid, message = validator.valid_status(status)
    assert is_valid is False
    assert message == "Invalid or No Task Status given. Status Incomplete, Inprogress and Complete"