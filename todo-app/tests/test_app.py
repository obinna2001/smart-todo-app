from todo_app.models.app import TodoApp

app = TodoApp()

def test_success_add_task():
    sample = "buy groceries @shopping #high due:8pm assigned:okeyobinna2001@gmail.com"
    status, message, output = app.add_task(sample)
    assert status is True
    assert message == 'Task added'
    assert isinstance(output, list)
    assert all(isinstance(task, dict) for task in output)

def test_missing_description_add_task():
    sample = "@shopping #high due:8pm assigned:okeyobinna2001@gmail.com"
    status, message, output = app.add_task(sample)
    assert status is False
    assert output == []
    assert message == "Task description not Found!"

def test_missing_tag_add_task():
    sample = "buy groceries #high due:8pm assigned:okeyobinna2001@gmail.com"
    status, message, output = app.add_task(sample)
    assert status is False
    assert output == []
    assert message == 'Task Tag not found!'

def test_missing_priority_add_task():
    sample = "buy groceries @shopping due:8pm assigned:okeyobinna2001@gmail.com"
    status, message, output = app.add_task(sample)
    assert status is False
    assert output == []
    assert message == 'Task Priority level not found!'

def test_missing_time_date_add_task():
    sample = "buy groceries @shopping #high assigned:okeyobinna2001@gmail.com"
    status, message, output = app.add_task(sample)
    assert status is False
    assert output == []
    assert message == 'Invalid or No date found in task description.'

def test_missing_email_add_task():
    sample = "buy groceries @shopping #high due:8pm"
    status, message, output = app.add_task(sample)
    assert status is True
    assert message == 'Task added'
    assert isinstance(output, list)
    assert all(isinstance(task, dict) for task in output)