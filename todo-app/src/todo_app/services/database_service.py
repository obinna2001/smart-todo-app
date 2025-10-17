import json
import re
from typing import Union, Tuple, List, Any
from todo_app.parsers.validator import valid_email, valid_priority_level, valid_status
from todo_app.parsers.extractor import extract_taskid
from todo_app.utilis.utils import convert_datestring
from todo_app.config import JSON_DB_PATH

# extract everything in a string except the first 8 values
UPDATE_PATTERN = re.compile(r'^.{8}\s*(.*)')


def read_json() -> list:
    """Access todo-app.json """
    try:
        with open(JSON_DB_PATH, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def validate_taskid(task_id: str) -> Tuple[bool, str]:
    """check if a task id is valid.
        args:
            task_id: user input task id
        return:
            bool: True or False
            mssg: success message
            err: error message
    """
    # read todo-app.json
    json_tasks = read_json()

    # check for empty task_id
    if not task_id:
        err = '❌  Task id is empty'
        return False, err
    
    # extract all the task ID into a list
    task_ids = [task.get('ID') for task in json_tasks]

    if task_id in task_ids:
        mssg = '✔️  Task ID is valid'
        return True, mssg
    else:
        err = f'❌ Invalid Task ID. {task_id} does not exist!'
        return False, err

def save_json(data: dict) -> None:
    """save todo-app.json after every update"""
    with open(JSON_DB_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def upload_task(data: dict) -> List[Any]:
    """Save a task to todo-app.json"""
    todo_records = read_json()
    todo_records.append(data)
    with open(JSON_DB_PATH, 'w') as db:
        json.dump(todo_records, db, indent=4)
    
    print('successful- place holder message')
    
    return [dict]


def delete_tasks(index: List[Union[int, str]]) -> str:
    """Delete one or more tasks based on index or task ID."""
    todo_records = read_json()

    if not todo_records:
        return f"⛔ No record found - mermory is Empty"
    
    deleted_task = []
    not_found_task = []

    # First handle numeric indices
    for item in [i for i in index if isinstance(i, int)]:
        if 0 <= item < len(todo_records):
            deleted_task.append(todo_records.pop(item))
        else:
            not_found_task.append(item)

    # Then handle string based index
    # delete all records if 'all' is in index
    string_index = [item for item in index if isinstance(item, str)]
    if any(index.strip().lower() == 'all' for index in string_index):
        task_count = len(todo_records)

        # delete all records
        todo_records.clear()

        # update the cleared todo-app.json
        save_json(todo_records)

        # return status message
        return f"✔️  Delete successful - all {task_count} task(s) cleared"
        
    # delete record based task id
    for item in index:
        status, _ = validate_taskid(item)
        if status:
            # Find the task with matching ID
            task_to_remove = next((task for task in todo_records if task.get('ID') == item), None)
            if task_to_remove:
                todo_records.remove(task_to_remove)
                deleted_task.append(item)
            else:
                not_found_task.append(item)
        else:
            not_found_task.append(item)

    save_json(todo_records)

    if deleted_task and not_found_task:
        return f"🗑️  Deleted {len(deleted_task)} task(s), but {not_found_task} not found ⚠️."
    elif deleted_task:
        return f"🗑️  Deleted {len(deleted_task)} task(s) successfully."
    else:
        return f"❌ No matching tasks found for {index}."
    

def display_tasks(index: List[Union[int, str]]) -> Union[Tuple[bool, str], Tuple[bool, List[Any]]]:
    """To display tasks in the todo app based on task id, task index or 'all'.
        args:
            index: List of task index, task id or all
        return:
            err: error message
            bool: True or False
            to_display: list of extracted todo task to be display
    """
    # read todo-app.json
    todo_records = read_json()
    
    # check if todo_records is empty
    if not todo_records:
        err = "⛔ No record found - mermory is Empty"
        return False, err
    
    # initialize list to store extracted task and track task not found
    to_display = []
    not_found = []

    # Handle numeric based index
    for item in [i for i in index if isinstance(i, int)]:
        if 0 <= item < len(todo_records):
            to_display.append(todo_records[item])
        else:
            not_found.append(item)
        
    # Handle 'all' index
    # Display all task in todo record if index is 'all'
    string_index = [item for item in index if isinstance(item, str)]
    if any(item.strip().lower() == 'all' for item in string_index):
        for task in todo_records:
            to_display.append(task)

        return True, to_display
    
    # Handle task id based index
    for item in index:
        status, _ = validate_taskid(item)
        if status:
            # Find the task with matching ID
            task_ = next((task for task in todo_records if task.get('ID') == item), None)
            if task_:
                to_display.append(task_)
            else:
                not_found.append(item)
        else:
            not_found.append(item)

    save_json(todo_records)

    if to_display and not_found:
        print(f"✔️  Found {len(to_display)} task(s), but {not_found} not found ⚠️.")
        return True, to_display
    elif to_display:
        return True, to_display
    else:
        err = f"❌ No matching tasks found for {index}."
        return False, err
    
    
def update_description(update_values: str) -> Tuple[bool, str]:
    """"To update the description of an existing task based on task id.
        args:
            update_values: The new task values; format = task id task key task value. E.g 7d588667 buy food time
        return:
            err or mssg: error message or success message
            bool: True or False
    """
    # extract task id
    extract_id = extract_taskid(update_values)

    # validate task id
    status, result = validate_taskid(extract_id)
    if not status:
        return status, result   # status == False
    
    task_id = result

    # extract description
    description_match = UPDATE_PATTERN.search()
    if not description_match:
        err = '❌ Invalid or No description given.'
        return False, err
    
    # initialise description
    description = description_match.group(1).strip().title()

    # open todo-app.json to update decription
    todo_records = read_json()
    
    # update description of task with task_id
    for task in todo_records:
        if task_id == task.get('ID'):
            task['Description'] = description

    # save update
    save_json(todo_records)
    
    # return success message
    mssg = f'✔️  {task_id} description update successful'
    return True, mssg

def update_time(update_values: str) -> Tuple[bool, str]:
    """"To update the time of an existing task based on task id.
        args:
            update_values: The new task values; format = task id task key: task value. E.g 7d588667 tomorrow
        return:
            err or mssg: error message or success message
    """
    # extract task id
    extract_id = extract_taskid(update_values)

    # validate task id
    status, result = validate_taskid(extract_id)
    if not status:
        return status, result   # status == False
    
    task_id = result

    # extract time
    time_match = UPDATE_PATTERN.search(update_values)

    if not time_match:
        err = '❌  No value for time or date.'
        return False, err

    time_string = time_match.group(1).strip()
    status, result = convert_datestring(time_string)  # convert time string to datetime object

    # conversion fail
    if not status:
        return False, result
    
    task_time = result

    # open todo-app.json to update decription
    todo_records = read_json()
    
    # update time of task with task_id
    for task in todo_records:
        if task_id == task.get('ID'):
            task['Time'] = task_time

    # save update
    save_json(todo_records)
    
    # return success message
    mssg = f'✔️  {task_id} time update successful'
    return True, mssg

def update_email(update_values: str) -> Tuple[bool, str]:  
    """"To update the email address of an existing task based on task id.
        args:
            update_values: The new task values; format = task id task key: task value. E.g 7d588667 johndoe2025@gmail.com
        return:
            err or mssg: error message or success message
    """
    # extract task id
    extract_id = extract_taskid(update_values)

    # validate task id
    status, result = validate_taskid(extract_id)
    if not status:
        return status, result   # status == False
    
    task_id = result

    # extract email
    email_match = UPDATE_PATTERN.search(update_values)
    
    # check if email value is given
    if not email_match:
        err = '❌  No value for Email address.'
        return False, err
    
    mail_extract = email_match.group(1).strip()

    # check if email is valid
    valid_mail = valid_email(mail_extract)

    if isinstance(valid_mail, str):
        err = valid_mail
        return False, err

    email = valid_mail.email  # convert valid_mail to str

    # open todo-app.json to update decription
    todo_records = read_json()
    
    # update email of task with task_id
    for task in todo_records:
        if task_id == task.get('ID'):
            task['Email'] = email

    # save update
    save_json(todo_records)
    
    # return success message
    mssg = f'✔️  {task_id} Email update successful'
    return True, mssg

def update_tag(update_values: str) -> Tuple[bool, str]:
    """"To update the tag of an existing task based on task id.
        args:
            update_values: The new task values; format = task id task key: task value. E.g 7d588667 market
        return:
            err or mssg: error message or success message
    """
    # extract task id
    extract_id = extract_taskid(update_values)

    # validate task id
    status, result = validate_taskid(extract_id)
    if not status:
        return status, result   # status == False
    
    task_id = result

    # extract tag
    tag_match = UPDATE_PATTERN.search(update_values)
    
    # check if tag value is given
    if not tag_match:
        err = '❌  No value for tag.'
        return False, err
    
    tag = tag_match.group(1).strip().upper()

    # open todo-app.json to update decription
    todo_records = read_json()
    
    # update tag of task with task_id
    for task in todo_records:
        if task_id == task.get('ID'):
            task['Tag'] = tag

    # save update
    save_json(todo_records)
    
    # return success message
    mssg = f'✔️  {task_id} Tag update successful'
    return True, mssg


def update_priority(update_values: str) -> Tuple[bool, str]:  
    """"To update the priority of an existing task based on task id.
        args:
            update_values: The new task values; format = task id task key: task value. E.g 7d588667 johndoe2025@gmail.com
        return:
            err or mssg: error message or success message
    """
    # extract task id
    extract_id = extract_taskid(update_values)

    # validate task id
    status, result = validate_taskid(extract_id)
    if not status:
        return status, result   # status == False
    
    task_id = result

    # extract priority
    priority_match = UPDATE_PATTERN.search(update_values)
    
    # check if priority value is given
    if not priority_match:
        err = '❌  No value for Priority Level.'
        return False, err
    
    priority = priority_match.group(1).strip().title()

    # check if priority is valid
    status, result = valid_priority_level(priority)
    
    # if priority is invalid
    if not status:
        return status, result

    # open todo-app.json to update decription
    todo_records = read_json()
    
    # update description of task with task_id
    for task in todo_records:
        if task_id == task.get('ID'):
            task['Priority'] = priority

    # save update
    save_json(todo_records)
    
    # return success message
    mssg = f'✔️  {task_id} Priority Level update successful'
    return True, mssg


def update_status(update_values: str) -> Tuple[bool, str]:
    """"To update the status of an existing task based on task id.
        args:
            update_values: The new task values; format = task id task key task value. E.g 7d588667 Complete
        return:
            err or mssg: error message or success message
    """
    # extract task id
    extract_id = extract_taskid(update_values)

    # validate task id
    status, result = validate_taskid(extract_id)
    if not status:
        return status, result   # status == False
    
    task_id = result

    # extract status
    status_match = UPDATE_PATTERN.search(update_values)
    
    # check if status value is given
    if not status_match:
        err = '❌  No value for Status.'
        return False, err
    
    task_status = status_match.group(1).strip().title()

    # check if status is valid
    status, result = valid_status(task_status)
    
    # if status is invalid
    if not status:
        return status, result

    # open todo-app.json to update status
    todo_records = read_json()
    
    # update status of task with task_id
    if task_status == 'Incomplete':
        task_status = 'Incomplete  🟩⬜⬜⬜⬜'

    elif task_status == 'Complete':
        task_status = 'Complete  🟩🟩🟩🟩🟩'

    elif task_status == 'Inprogress':
        task_status = 'Inprogress  🟩🟩🟨⬜⬜'

    for task in todo_records:
        if task_id == task.get('ID'):
            task['Status'] = task_status

    # save update
    save_json(todo_records)
    
    # return success message
    mssg = f'✔️  {task_id} Task Status update successful'
    return True, mssg