import json
from todo_app.config import JSON_DB_PATH
from typing import Union

def read_json() -> list:
    """Access todo-app.json """
    try:
        with open(JSON_DB_PATH, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(data: dict) -> None:
    """save todo-app.json after every update"""
    with open(JSON_DB_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def upload_task(data: dict) -> str:
    """Save a task to todo-app.json"""
    todo_records = read_json()
    todo_records.append(data)
    with open(JSON_DB_PATH, 'w') as db:
        json.dump(todo_records, db, indent=4)

    return f"✔️  Task added: {data['Description']}\n #️⃣  Task ID: {data['ID']} 🏷️ Tags: {data['Tag']} |⚡ Priority: {data['Priority']} | 🕒 Due: {data['Time']} | ⏳ Status: {data['Status']}"


def update_task_status():
    pass