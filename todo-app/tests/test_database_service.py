from todo_app.services.database_service import DatabaseService

db_service = DatabaseService()

def test_upload_task():
    task = {
        "ID": "76487gtd",
        "Time": "2024-06-01 10:00:00",
        "Description": "Test task",
        "Priority": "High",
        "Tag": "Testing",
        "Email": "",
        "Status": "Incomplete 🟩⬜⬜⬜⬜"
    }
    status, message, tasks = db_service.upload_task(task)
    assert status is True
    assert message == 'Task added'
    assert isinstance(tasks, list)
    assert all(isinstance(task, dict) for task in tasks)

def test_display_tasks_by_index():
    index = [0, 1, 2]
    status, message, task = db_service.display_tasks(index)
    assert status is True
    assert message == ''
    assert isinstance(task, list)
    assert all(isinstance(task, dict) for task in task)

def test_display_tasks_by_id():
    task_ids = ['76487gtd']
    status, message, task = db_service.display_tasks(task_ids)
    assert status is True
    assert message == ''
    assert isinstance(task, list)
    assert all(isinstance(task, dict) for task in task)

def test_display_tasks_by_all():
    index = ['all']
    status, message, task = db_service.display_tasks(index)
    assert status is True
    assert message == ''
    assert isinstance(task, list)
    assert all(isinstance(task, dict) for task in task)

def test_display_tasks_invalid_index():
    index = [100000000, 300000000000]
    status, message, task = db_service.display_tasks(index)
    assert status is False
    assert message == f'No matching tasks found for {index}.'
    assert task == []

def test_display_tasks_invalid_id():
    task_ids = ['nmdhs87g', 'kifs73hd']
    status, message, task = db_service.display_tasks(task_ids)
    assert status is False
    assert message == f'No matching tasks found for {task_ids}.'
    assert task == []

def test_update_description():
    task_id = '76487gtd'
    update_values = '76487gtd Updated test task'
    status, message = db_service.update_description(update_values)
    assert status is True
    assert message == f"{task_id} description update successful."

def test_invalid_update_description_id():
    task_id = 'ydhfi73g'
    update_values = f'{task_id} Updated test task'
    status, message = db_service.update_description(update_values)
    assert status is False
    assert message == f"Invalid Task ID. {task_id} does not exist!"

def test_empty_update_decription_id():
    update_values = 'call john to congratulate him'
    status, message = db_service.update_description(update_values)
    assert status is False
    assert isinstance(message, str)

def test_empty_update_description_value():
    task_id = '76487gtd'
    update_values = f'{task_id} '
    status, message = db_service.update_description(update_values)
    assert status is False
    assert message == "No description given."

def test_update_time():
    task_id = '76487gtd'
    update_values = f'{task_id} 2024-06-15 14:30'
    status, message = db_service.update_time(update_values)
    assert status is True
    assert message == f"{task_id} time update successful."

def test_missing_update_time_value():
    task_id = '76487gtd'
    update_values = f'{task_id} '
    status, message = db_service.update_time(update_values)
    assert status is False
    assert message == "No value for time or date."

def test_invalid_update_time_id():
    task_id = 'ydhfi73g'
    update_values = f'{task_id} 2024-06-15 14:30'
    status, message = db_service.update_time(update_values)
    assert status is False
    assert message == f"Invalid Task ID. {task_id} does not exist!"

def test_update_email():
    task_id = '76487gtd'
    update_values = f'{task_id} johndoe789@gmail.com'
    status, message = db_service.update_email(update_values)
    assert status is True
    assert message == f"{task_id} Email update successful"

def test_missing_update_email_value():
    task_id = '76487gtd'
    update_values = f'{task_id} '
    status, message = db_service.update_email(update_values)
    assert status is False
    assert message == "No value for Email address."

def test_update_tag():
    task_id = '76487gtd'
    update_values = f'{task_id} Work'
    status, message = db_service.update_tag(update_values)
    assert status is True
    assert message == f"{task_id} Tag update successful"

def test_missing_update_tag_value():
    task_id = '76487gtd'
    update_values = f'{task_id} '
    status, message = db_service.update_tag(update_values)
    assert status is False
    assert message == "Tag value is empty."

def test_update_priority():
    task_id = '76487gtd'
    update_values = f'{task_id} high'
    status, message = db_service.update_priority(update_values)
    assert status is True
    assert message == f"{task_id} Priority Level update successful"

def test_missing_update_priority_value():
    task_id = '76487gtd'
    update_values = f'{task_id} '
    status, message = db_service.update_priority(update_values)
    assert status is False
    assert message == "Priority Level is empty."

def test_update_status():
    task_id = '76487gtd'
    update_values = f'{task_id} complete'
    status, message = db_service.update_status(update_values)
    assert status is True
    assert message == f"{task_id} Task Status update successful"