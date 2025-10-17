from todo_app.parsers.extractor import extract_task, extract_date, extract_priority_level, extract_email, extract_tag
from todo_app.utilis.utils import generate_taskID
from todo_app.services.database_service import upload_task, delete_tasks, update_description, update_email, update_time, update_priority, update_tag, update_status, display_tasks
from todo_app.services.task_service import keyword_search, tag_filter, time_filter, priority_filter
from typing import Union, Tuple, List, Any


class TodoApp:
    def __init__(self, user_input: str):
        self.user_input = user_input

    def add_task(self) -> List[Any]:
        """Assign a task based on user input and store in JSON_DB"""
        description_status, task_description = extract_task(self.user_input)
        time_status, task_time = extract_date(self.user_input)
        priority_status, task_priority = extract_priority_level(self.user_input)
        tag_status, task_tag = extract_tag(self.user_input)
        email_status, task_email = extract_email(self.user_input)
        
        # checking if user input is valid
        if not description_status: 
            raise task_description
        
        if not time_status:
            raise task_time
        
        if not priority_status:
            raise task_priority
        
        if not tag_status:
            raise task_tag
        
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
    
    def delete_task(self, index: List[Union[int, str]]) -> str:
        """Delete one or more tasks based on index, task ID or 'all'.
            args:
                index: list of task index which are either valid task id, task index or 'all'
            return:
                status_message: The status message of deletion process
            """
        status_message = delete_tasks(index)

        # return status
        return status_message
    
    def display_task(self, index: List[Union[int, str]]) -> Union[str, List[Any]]:
        """Delete one or more tasks based on index, task ID or 'all'.
            args:
                index: list of task index which are either valid task id, task index or 'all'
            return:
                result: The status message of deletion process or list of task to be displayed
            """
        
        status, result = display_tasks(index)
        if not status:
            return result
        
        return result


    def update_task_description(self, update_values: str) -> str:
        """"To update the description of an existing task based on the task id.
            args:
                update_values: The new task values; format = task id task key: task value. E.g '7d588660 buy food'
            return:
                status: True, False
                mssg: description update result 
        """
        status, mssg = update_description(update_values)
        
        # return error message if not successful
        if not status:
            return mssg
        
        return mssg
    
    def update_task_time(self, update_values: str) -> str:
        """"To update the time of an existing task based on the task id.
            args:
                update_values: The new task values; format = task id task key task value. E.g '9d30d4ab 4pm'
            return:
                status: True, False
                mssg: description update result 
        """
        status, mssg = update_time(update_values)
        
        # return error message if not successful
        if not status:
            return mssg
        
        return mssg
    
    def update_task_email(self, update_values: str) -> str:
        """"To update the email of an existing task based on the task id.
            args:
                update_values: The new task values; format = task id task key task value. E.g '9d30d4ab johnobinna700@gmail.com'
            return:
                status: True, False
                mssg: description update result 
        """
        status, mssg = update_email(update_values)
        
        # return error message if not successful
        if not status:
            return mssg
        
        return mssg   

    def update_task_priority(self, update_values: str) -> str:
        """"To update the priority level of an existing task based on the task id.
            args:
                update_values: The new task values; format = task id task key task value. E.g '9d30d4ab mild'
            return:
                status: True, False
                mssg: description update result 
        """
        status, mssg = update_priority(update_values)
        
        # return error message if not successful
        if not status:
            return mssg
        
        return mssg  

    def update_task_tag(self, update_values: str) -> str:
        """"To update the tag of an existing task based on the task id.
            args:
                update_values: The new task values; format = task id task key task value. E.g '9d30d4ab school'
            return:
                status: True, False
                mssg: description update result 
        """
        status, mssg = update_tag(update_values)
        
        # return error message if not successful
        if not status:
            return mssg
        
        return mssg 

    def update_task_status(self, update_values: str) -> str:
        """"To update the status of an existing task based on the task id.
            args:
                update_values: The new task values; format = task id task key task value. E.g '9d30d4ab Inprogress'
            return:
                status: True, False
                mssg: description update result 
        """
        status, mssg = update_status(update_values)
        
        # return error message if not successful
        if not status:
            return mssg
        
        return mssg

    def  task_keyword_search(self, keywords: List[str]) ->  Union[str, List[Any]]:
        """ Search and extract task from todo-app.json using keyword.
            args:
                keywords: List containing keywords
            return:
                (bool, list | str):
                    - (True, search_result| error message)
        """

        status, result = keyword_search(keywords)
                    


if __name__ == '__main__':
    """status: complete, inprogress and incomplete"""
    """update format: task id value example '7d588660 buy food', '9d30d4ab high', '9d30d4ab 4pm', '4253d1b5 incomplete'"""
    sample = "study bible and pray @worship #high due:2pm assigned:johnobinna700@gmail.com"
    app = TodoApp(sample)
    print(app.add_task(['all']))