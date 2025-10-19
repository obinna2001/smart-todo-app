from todo_app.models.app import TodoApp

app = TodoApp()

sample = "buy groceries @shopping #high due:8pm assigned:okeyobinna2001@gmail.com"

def test_add_task():
    sample = "buy groceries @shopping #high due:8pm assigned:okeyobinna2001@gmail.com"

    status, message, output = app.add_task(sample)
    assert isinstance(status, bool)
    assert isinstance(message, str)
    assert isinstance(output, list)

