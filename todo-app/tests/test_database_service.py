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
        "Status": "Incomplete"
    }
    status, message, tasks = db_service.upload_task(task)
    assert status is True
    assert isinstance(message, str)
    assert isinstance(tasks, list)
    assert all(isinstance(task, dict) for task in tasks)

def test_display_all_tasks():
    status, message, task = db_service.display_all_tasks()
    assert status is True
    assert message == ''
    assert isinstance(task, list)
    assert all(isinstance(task, dict) for task in task)

def test_display_tasks():
    task_ids = ["f7d92f3b"]
    status, message, task = db_service.display_tasks(task_ids)
    assert status is True
    assert message == ''
    assert isinstance(task, list)
    assert all(isinstance(task, dict) for task in task)

def test_display_tasks_invalid_id():
    task_ids = ['nmdhs87g', 'kifs73hd']
    status, message, task = db_service.display_tasks(task_ids)
    assert status is False
    assert isinstance(message, str)
    assert task == []

def test_display_mixed_id():
    task_ids = ['nmdhs87g', 'kifs73hd', "f7d92f3b"]
    status, message, task = db_service.display_tasks(task_ids)
    assert status is True
    assert isinstance(message, str)
    assert isinstance(task, list)
    assert all(isinstance(task, dict) for task in task)  

def test_update_description():
    task_id = 'f7d92f3b'
    update_values = f'{task_id} Updated test task'
    status, message = db_service.update_description(update_values)
    assert status is True
    assert isinstance(message, str)

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
    task_id = '76339f3c'
    update_values = f'{task_id} '
    status, message = db_service.update_description(update_values)
    assert status is False
    assert isinstance(message, str)

def test_update_time():
    task_id = '76339f3c'
    update_values = f'{task_id} 2024-06-15 14:30'
    status, message = db_service.update_time(update_values)
    assert status is True
    assert isinstance(message, str)

def test_missing_update_time_value():
    task_id = '76339f3c'
    update_values = f'{task_id} '
    status, message = db_service.update_time(update_values)
    assert status is False
    assert isinstance(message, str)

def test_invalid_update_time_id():
    task_id = 'ydhfi73g'
    update_values = f'{task_id} 2024-06-15 14:30'
    status, message = db_service.update_time(update_values)
    assert status is False
    assert isinstance(message, str)

def test_update_email():
    task_id = '76339f3c'
    update_values = f'{task_id} johndoe789@gmail.com'
    status, message = db_service.update_email(update_values)
    assert status is True
    assert isinstance(message, str)

def test_missing_update_email_value():
    task_id = '76339f3c'
    update_values = f'{task_id} '
    status, message = db_service.update_email(update_values)
    assert status is False
    assert isinstance(message, str)

def test_update_priority():
    task_id = '76339f3c'
    update_values = f'{task_id} high'
    status, message = db_service.update_priority(update_values)
    assert status is True
    assert isinstance(message, str)

def test_missing_update_priority_value():
    task_id = '76339f3c'
    update_values = f'{task_id} '
    status, message = db_service.update_priority(update_values)
    assert status is False
    assert isinstance(message, str)

def test_update_status():
    task_id = '76339f3c'
    update_values = f'{task_id} complete'
    status, message = db_service.update_status(update_values)
    assert status is True
    assert isinstance(message, str)

# def test_delete_all_task():
#     message = db_service.delete_all_tasks()
#     assert message == "Delete successful - all {task_count} task(s) cleared" 

# def test_delete_invalid_task():
#     task_id = ['09dhf73g']
#     message = db_service.delete_tasks(task_id)
#     assert message == f"No matching tasks found for {task_id}."

# def test_delete_mixed_tasks():
#     task_id = ['09dhf73g', '76339f3c76487gtd', "ed8f905f"]
#     message = db_service.delete_tasks(task_id)
#     assert message == f"Deleted 1 task(s), but {['09dhf73g', 'ed8f905f']} not found."


