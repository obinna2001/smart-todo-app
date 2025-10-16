from todo_app.parsers.extractor import extract_task, extract_date, extract_priority_level, extract_email, extract_tag
from todo_app.utilis.utils import generate_taskID
from todo_app.utilis.json_utils import upload_task, save_json, read_json
from typing import Union


class TodoApp:
    def __init__(self, user_input: str):
        self.user_input = user_input

    def add_task(self):
        """Assign a task based on user input and store in JSON_DB"""
        description_status, task_description = extract_task(self.user_input)
        time_status, task_time = extract_date(self.user_input)
        priority_status, task_priority = extract_priority_level(self.user_input)
        tag_status, task_tag = extract_tag(self.user_input)
        email_status, task_email = extract_email(self.user_input)
        
        # checking if user input is valid
        if not description_status: 
            return task_description
        
        if not time_status:
            return task_time
        
        if not priority_status:
            return task_priority
        
        if not tag_status:
            return task_tag
        
        if not email_status:
            if task_email == 'Email not found.':
                task_email = ""

            elif task_email == "Invalid Email address":
                raise task_email
        
        # create a unique task id and status
        task_id = generate_taskID(self.user_input)
        status = "Incomplete 🟩⬜⬜⬜⬜"

        # create task
        task = {
            'ID': task_id,
            'Time': str(task_time),
            'Description': task_description,
            'Priority': task_priority,
            'Tag': task_tag,
            'Email': task_email,
            'Status': status
        }

        # save task to todo-app.json
        return upload_task(task)
    

    def delete_tasks(self, index: list[Union[int, str]]) -> str:
        """Delete one or more tasks based on index or task ID."""
        todo_records = read_json()

        if not todo_records:
            return f"⛔ No record found - mermory is Empty"
        
        # delete all records if index is 'all'
        if isinstance(index, str) and 'all' in [item.lower() for item in index]:
            # instantiate the count of records to be deleted
            task_count = len(todo_records)

            # delete all records
            todo_records.clear()

            # update the cleared todo-app.json
            save_json(todo_records)

            # return status message
            return f"✔️  Delete successful - {task_count} task(s) all cleared"
    
        deleted_task = []
        not_found_task = []

        # First handle numeric indices
        for item in [i for i in index if isinstance(i, int)]:
            if 0 <= item < len(todo_records):
                deleted_task.append(todo_records.pop(item))
            else:
                not_found_task.append(item)

        # Then handle string-based IDs
        for item in [i for i in index if isinstance(i, str)]:
                    if isinstance(index, str) and 'all' in [item.lower() for item in index]:
            # instantiate the count of records to be deleted
            task_count = len(todo_records)

            # delete all records
            todo_records.clear()

            # update the cleared todo-app.json
            save_json(todo_records)

            # return status message
            return f"✔️  Delete successful - {task_count} task(s) all cleared"
            found = next((t for t in todo_records if t.get("ID") == item), None)
            if found:
                todo_records.remove(found)
                deleted_task.append(found)
            else:
                not_found_task.append(item)

        save_json(todo_records)

        if deleted_task and not not_found_task:
            return f"🗑️  Deleted {len(deleted_task)} task(s) successfully."
    
        elif deleted_task and not_found_task:
            return f"🗑️  Deleted {len(deleted_task)} task(s), but {not_found_task} not found ⚠️."
    
        else:
            return f"❌ No matching tasks found for {index}."
        
    
    def update_task_status(self, status: str) -> str:
        pass


if __name__ == '__main__':
    sample = "study bible and pray @worship #high due:2pm assigned:okeyobinna2001@gmail.com"
    app = TodoApp(sample)
    print(app.delete_all())