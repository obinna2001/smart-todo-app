from todo_app.services.task_service import TaskService

task_service = TaskService()

def test_keyword_search():
    keywords = ["complete", 'shopping', 'johnobinna700@gmail.com']
    status, message, tasks = task_service.keyword_search(keywords)
    assert status is True
    assert message == ''
    assert isinstance(tasks, list)
    assert all(isinstance(task, dict) for task in tasks)

def test_wrong_keyword_search():
    keywords = ["university", "paris"]
    status, message, tasks = task_service.keyword_search(keywords)
    assert status is False
    assert message == f'No search result found for {keywords}'
    assert tasks == []

def test_tag_filter():
    tag_filters = ["shopping", "worship"]
    status, message, tasks = task_service.tag_filter(tag_filters)
    assert status is True
    assert message == ''
    assert isinstance(tasks, list)
    assert all(isinstance(task, dict) for task in tasks)

def test_wrong_tag_filter():
    tag_filters = ["holiday", "vacation"]
    status, message, tasks = task_service.tag_filter(tag_filters)
    assert status is False
    assert message == f'No search result found for {tag_filters}'
    assert tasks == []

def test_time_filter():
    time_filters = ["", "2025-10-12", 'yesterday']
    status, message, tasks = task_service.time_filter(time_filters)
    assert status is True
    assert message == ''
    assert isinstance(tasks, list)
    assert all(isinstance(task, dict) for task in tasks)

def test_wrong_time_filter():
    time_filters = ["1990-01-01", "2000-12-12"]
    status, message, tasks = task_service.time_filter(time_filters)
    assert status is False
    assert message == f'No search result found for {time_filters}'
    assert tasks == []

def test_priority_filter():
    priority_filters = ["high", "mild"]
    status, message, tasks = task_service.priority_filter(priority_filters)
    assert status is True
    assert message == ''
    assert isinstance(tasks, list)
    assert all(isinstance(task, dict) for task in tasks)

def test_wrong_priority_filter():
    priority_filters = ["urgent", "critical"]
    status, message, tasks = task_service.priority_filter(priority_filters)
    assert status is False
    assert message == 'Invalid Priority Level. Priority Level are high, mild and low'
    assert tasks == []