from todo_app.parsers.extractor import Extractor
from datetime import datetime

app = Extractor()

def test_task_description_extraction():
    sample = "buy groceries @shopping #high due:8pm assigned:okeyobinna2001@gmail.com"
    status, message = app.extract_task_description(sample)
    assert status is True
    assert message == "Buy Groceries"

def test_missing_description_input_extraction():
    sample = "@shopping #high due:8pm assigned:okeyobinna2001@gmail.com"
    status, error_message = app.extract_task_description(sample)
    assert status is False
    assert error_message == "Task description not Found!"

def test_priority_level_extraction():
    sample = "buy groceries @shopping #high due:8pm assigned:okeyobinna2001@gmail.com"
    status, priority = app.extract_priority_level(sample)
    assert status is True
    assert priority == "High"

def test_missing_priority_level_input_extraction():
    sample = "buy groceries @shopping due:8pm assigned:okeyobinna2001@gmail.com"
    status, error_message = app.extract_priority_level(sample)
    assert status is False
    assert error_message == "Task Priority level not found!"

def test_wrong_priority_level_input_extraction():
    sample = "buy groceries @shopping #urgent due:8pm assigned:okeyobinna2001@gmail.com"
    status, error_message = app.extract_priority_level(sample)
    assert status is False
    assert error_message == "Invalid Priority Level. Priority Level are high, mild and low"

def test_tag_extraction():
    sample = "buy groceries @shopping #mild due:8pm assigned:okeyobinna2001@gmail.com"
    status, tag = app.extract_tag(sample)
    assert status is True
    assert tag == "Shopping"

def test_missing_tag_input_extraction():
    sample = "buy groceries #high due:8pm assigned:okeyobinna2001@gmail.com"
    status, error_message = app.extract_tag(sample)
    assert status is False
    assert error_message == "Task Tag not found!"

def test_email_extraction():
    sample = "buy groceries @shopping #high due:8pm assigned:okeyobinna2001@gmail.com"
    status, email = app.extract_email(sample)
    assert status is True
    assert email == "okeyobinna2001@gmail.com"

def test_missing_email_input_extraction():
    sample = "buy groceries @shopping #high due:8pm"
    status, error_message = app.extract_email(sample)
    assert status is False
    assert error_message == "Email not found."

def test_invalid_email_input_extraction():
    sample = "buy groceries @shopping #high due:8pm assigned:jhonobinna2001gmail.com"
    status, error_message = app.extract_email(sample)
    assert status is False
    assert error_message == "Invalid Email address"

def test_date_time_extraction():
    sample = "buy groceries @shopping #high due:tomorrow assigned:okeyobinna2001@gmail.com"
    status, due_date = app.extract_date(sample)
    assert status is True
    assert isinstance(due_date, datetime)

def test_missing_date_time_input_extraction():
    sample = "buy groceries @shopping #high assigned:johnjoe98@gmail.com"
    status, error_message = app.extract_date(sample)
    assert status is False
    assert error_message == "Invalid or No date found in task description."

def test_invalid_date_time_input_extraction():
    sample = "buy groceries @shopping #high due:someday assigned:jhonobinna2001gmail.com"
    status, error_message = app.extract_date(sample)
    assert status is False
    assert error_message == "Invalid or No date found in task description."