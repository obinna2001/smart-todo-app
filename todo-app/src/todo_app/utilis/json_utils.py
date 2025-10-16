import json
from todo_app.config import JSON_DB_PATH

def read_json() -> list:
    """Access todo-app.json """
    try:
        with open(JSON_DB_PATH, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def upload_task(data: dict) -> None:
    """Save a task to todo-app.json"""
    todo_records = read_json()
    todo_records.append(data)
    with open(JSON_DB_PATH, 'w') as db:
        json.dump(todo_records, db, indent=4)

    return f"✅ Task added: {data['Description']}\n 🏷️ Tags: {data['Tag']} |⚡ Priority: {data['Priority']} | 🕒 Due: {data['Time']}"

 