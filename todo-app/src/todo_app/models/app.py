from todo_app.parsers.extractor import (
    extract_task,
    extract_date,
    extract_priority_level,
    extract_email,
    extract_tag,
)
from todo_app.utilis.utils import generate_taskID
from todo_app.services.database_service import (
    upload_task,
    delete_tasks,
    update_description,
    update_email,
    update_time,
    update_priority,
    update_tag,
    update_status,
    display_tasks,
)
from todo_app.services.task_service import (
    keyword_search,
    tag_filter,
    time_filter,
    priority_filter,
)
from typing import Union, List, Any, Tuple


class TodoApp:
    def __init__(self):
        pass

    def add_task(self, user_input: str) -> Tuple[bool, str, List[Any]]:
        """Assign a task based on user input and store in JSON_DB
           args:
                user_input: A valid user input. Example buy groceries @shopping #high due:8pm assigned:okeyobinna2001@gmail.com
           return:
               (True|False, success message|error message, List[Dict]|[])
        """
        description_status, task_description = extract_task(user_input)
        time_status, task_time = extract_date(user_input)
        priority_status, task_priority = extract_priority_level(user_input)
        tag_status, task_tag = extract_tag(user_input)
        email_status, task_email = extract_email(user_input)

        # checking if user input is valid
        if not description_status:
            raise ValueError(task_description)

        if not time_status:
            raise ValueError(task_time)

        if not priority_status:
            raise ValueError(task_priority)

        if not tag_status:
            raise ValueError(task_tag)

        if not email_status:
            if task_email == "Email not found.":
                task_email = ""

            elif task_email == "Invalid Email address":
                raise ValueError(task_email)

        # create a unique task id and status
        task_id = generate_taskID(user_input)
        status = "Incomplete 🟩⬜⬜⬜⬜"

        # create task
        task = {
            "ID": task_id,
            "Time": str(task_time),
            "Description": task_description,
            "Priority": task_priority,
            "Tag": task_tag,
            "Email": task_email,
            "Status": status,
        }

        # save task to todo-app.json
        return upload_task(task)

    def delete_task(self, index: List[Union[int, str]]) -> str:
        """Delete one or more tasks based on index, task ID or 'all'.
        args:
            index: list of task index which are either valid task id, task index or 'all'
        return:
            status_message: The status message of deletion process
        """
        return delete_tasks(index)

    def display_task(self, index: List[Union[int, str]]) -> Union[Tuple[bool, str], Tuple[bool, List[Any]], Tuple[bool, str, List[Any]]]:
        """Delete one or more tasks based on index, task ID or 'all'.
        args:
            index: list of task index which are either valid task id, task index or 'all'
        return:
            (bool, str) | (bool, List[Any]) | (bool, str, List[Any]):
                - (True | False,  success message | error message)
        """
        return display_tasks(index)

    def update_task_description(self, update_values: str) -> str:
        """ "To update the description of an existing task based on the task id.
        args:
            update_values: The new task values; format = task id task key: task value. E.g '7d588660 buy food'
        return:
            (bool, list | str):
                - (True | False,  success message | error message)
        """
        return update_description(update_values)


    def update_task_time(self, update_values: str) -> str:
        """ "To update the time of an existing task based on the task id.
        args:
            update_values: The new task values; format = task id task key task value. E.g '9d30d4ab 4pm'
        return:
            (bool, list | str):
                - (True | False,  success message | error message)
        """
        return update_time(update_values)

    def update_task_email(self, update_values: str) -> str:
        """ "To update the email of an existing task based on the task id.
        args:
            update_values: The new task values; format = task id task key task value. E.g '9d30d4ab johnobinna700@gmail.com'
        return:
            (bool, list | str):
                - (True | False,  success message | error message)
        """
        return update_email(update_values)

    def update_task_priority(self, update_values: str) -> str:
        """ "To update the priority level of an existing task based on the task id.
        args:
            update_values: The new task values; format = task id task key task value. E.g '9d30d4ab mild'
        return:
            (bool, list | str):
                - (True | False,  success message | error message)
        """
        return update_priority(update_values)

    def update_task_tag(self, update_values: str) -> str:
        """ "To update the tag of an existing task based on the task id.
        args:
            update_values: The new task values; format = task id task key task value. E.g '9d30d4ab school'
        return:
            (bool, list | str):
                - (True | False,  success message | error message)
        """
        return update_tag(update_values)

    def update_task_status(self, update_values: str) -> str:
        """ "To update the status of an existing task based on the task id.
        args:
            update_values: The new task values; format = task id task key task value. E.g '9d30d4ab Inprogress'
        return:
            (bool, list | str):
                - (True | False,  success message | error message)
        """
        return update_status(update_values)

    def task_keyword_search(self, keywords: List[str]) -> Union[str, List[Any]]:
        """Search and extract task from todo-app.json using keyword.
        args:
            keywords: List containing keywords
        return:
            (bool, list | str):
                - (True | False,  search_result | error message)
        """

        return keyword_search(keywords)

    def task_tag_filter(self, tag_filters_list: List[str]) -> Union[str, List[Any]]:
        """Search and extract task from todo-app.json based on tag filters.
        args:
            tag_list: List containing tag filters example ['shopping', 'religion']
        return:
            (bool, list | str):
                - (True | False,  search_result | error message)
        """

        return tag_filter(tag_filters_list)

    def task_time_filter(self, time_filters_list: List[str]) -> Union[str, List[Any]]:
        """Search and extract task from todo-app.json based on time filters.
        args:
            tag_list: List containing time filters example ['yesterday', '2 weeks']
        return:
            (bool, list | str):
                - (True | False,  search_result | error message)
        """
        return time_filter(time_filters_list)


    def task_priority_filter(
        self, priority_filters_list: List[str]
    ) -> Union[str, List[Any]]:
        """Search and extract task from todo-app.json based on priority filters.
        args:
            tag_list: List containing priority filters example ['high', 'mild', 'low']
        return:
            (bool, list | str):
                - (True | False,  search_result | error message)
        """
        return priority_filter(priority_filters_list)



if __name__ == "__main__":
    """status: complete, inprogress and incomplete"""
    """update format: task id value example '7d588660 buy food', '9d30d4ab high', '9d30d4ab 4pm', '4253d1b5 incomplete'"""
