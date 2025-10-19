from todo_app.models.app import TodoApp

app = TodoApp()

def test_missing_description_add_task():
    sample = "@shopping #high due:8pm assigned:okeyobinna2001@gmail.com"
    error_message = app.add_task(sample)
    assert error_message == "Task description not Found!"

def test_missing_tag_add_task():
    sample = "buy groceries #high due:8pm assigned:okeyobinna2001@gmail.com"
    error_message = app.add_task(sample)
    assert error_message == 'Task Tag not found!'