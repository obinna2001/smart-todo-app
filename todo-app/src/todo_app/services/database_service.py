import json
import re
from typing import Union, Tuple, List, Any, Dict
from todo_app.parsers.validator import Validator
from todo_app.parsers.extractor import Extractor
from todo_app.utilis.utils import convert_datestring
from todo_app.config import JSON_DB_PATH

# extract everything in a string except the first 8 values
UPDATE_PATTERN = re.compile(r"^.{8}\s+(.+)")

class DatabaseService:
    """A class to handle database operations for the todo app."""
    def __init__(self):
        self.validator = Validator()
        self.extractor = Extractor()
    
    def read_json(self) -> list:
        """Access todo-app.json"""
        try:
            with open(JSON_DB_PATH, "r") as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def _save_json(self, data: List[Dict[str, Any]]) -> None:
        """save todo-app.json after every update"""
        with open(JSON_DB_PATH, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def _validate_taskid(self, task_id: str) -> Tuple[bool, str]:
        """check if a task id is valid.
            args:
                task_id: user input task id
            return: 
                (True | False,  success message | error message)
        """
        # read todo-app.json
        json_tasks = self.read_json()

        # # check for empty task_id
        # if not task_id:
        #     return False, "Task id is empty"

        # extract all the task ID into a list
        task_ids = [task.get("ID") for task in json_tasks]

        if task_id in task_ids:
            return True, "Task ID is valid"
    
        return False, f"Invalid Task ID. {task_id} does not exist!"

    def upload_task(self, data: dict) -> Tuple[bool, str, List[Any]]:
        """Save a task to todo-app.json.
            args:
                data: dictionary containing user task
            return: 
                (True | False, success message | error message, list of uploaded task | empty list)
        """
        todo_records = self.read_json()
        todo_records.append(data)
        try:
            with open(JSON_DB_PATH, "w") as db:
                json.dump(todo_records, db, indent=4)

            return True, "Task added", [data]
    
        except Exception as e:
            return False, str(e), []


    def delete_tasks(self, index: List[Union[int, str]]) -> str:
        """Delete one or more tasks based on index or task ID.
            args:
                index: list of task index which are either valid task id, task index or 'all'
            return:
                status_message: The status message of deletion process
        """
        todo_records = self.read_json()

        if not todo_records:
            return "No record found - mermory is Empty"

        deleted_task: List[Union[str, int]] = []
        not_found_task: List[Union[str, int]] = []

        # First handle numeric indices
        int_indices = [i for i in index if isinstance(i, int)]
        for idx in int_indices:
            if 0 <= idx < len(todo_records):
                todo_records.pop(idx)
                deleted_task.append(idx)
            else:
                not_found_task.append(idx)

        # Then handle string based index
        string_index = [item for item in index if isinstance(item, str)]

        # delete all records if 'all' is in index
        if any(idx.strip().lower() == "all" for idx in string_index):
            task_count = len(todo_records)

            # delete all records
            todo_records.clear()

            # update the cleared todo-app.json
            self._save_json(todo_records)

            # return status message
            return f"Delete successful - all {task_count} task(s) cleared"

        # delete record based task id
        for id in string_index:
            status, _ = self._validate_taskid(id)

            if status:
                # Find the task with matching ID
                task_to_remove = next(
                    (task for task in todo_records if task.get("ID") == id), None
                )
                if task_to_remove:
                    todo_records.remove(task_to_remove)
                    deleted_task.append(id)
                else:
                    not_found_task.append(id)
            else:
                not_found_task.append(id)

        self._save_json(todo_records)

        if deleted_task and not_found_task:
            return (
                f"Deleted {len(deleted_task)} task(s), but {not_found_task} not found."
            )
        elif deleted_task:
            return f"Deleted {len(deleted_task)} task(s) successfully."
        else:
            return f"No matching tasks found for {index}."


    def display_tasks(
        self, index: List[Union[int, str]],
    ) -> Tuple[bool, str, List[Any]]:
        """To display tasks in the todo app based on task id, task index or 'all'.
               args:
                   index: List of task index, task id or all
               return:
                    (bool, str, List[Any]):
                        - (True | False,  success message | error message, List of tasks | empty list)
        """
        # read todo-app.json
        todo_records = self.read_json()

        # check if todo_records is empty
        if not todo_records:
            return False, "No record found - Memory is Empty", []

        # initialize list to store extracted task and track task not found
        to_display: List[Dict[str, Any]] = []
        not_found: List[Union[str, int]] = []

        # Handle numeric based index
        int_indices = [i for i in index if isinstance(i, int)]
        for idx in int_indices:
            if 0 <= idx < len(todo_records):
                to_display.append(todo_records[idx])
            else:
                not_found.append(idx)

        # Handle string based index
        string_index = [id for id in index if isinstance(id, str)]

        # Display all task in todo record if index is 'all'
        if any(item.strip().lower() == "all" for item in string_index):
            for task in todo_records:
                to_display.append(task)
            
            self._save_json(todo_records)
            return True, "", to_display

        # Handle task id based index
        for id in string_index:
            status, _ = self._validate_taskid(id)
            if status:
                # Find the task with matching ID
                task_ = next(
                    (task for task in todo_records if task.get("ID") == id), None)

                if task_:
                    to_display.append(task_)
                else:
                    not_found.append(id)
            else:
                not_found.append(id)

        self._save_json(todo_records)

        if to_display and not_found:
            return True, f"Found {len(to_display)} task(s), but {not_found} not found.", to_display
    
        elif to_display:
            return True, "", to_display
    
        else:
            return False, f"No matching tasks found for {index}.", []


    def update_description(self, update_values: str) -> Tuple[bool, str]:
        """ "To update the description of an existing task based on task id.
            args:
                update_values: The new task values; format = task id task key task value. E.g 7d588667 buy food time
            return:
                (bool, str):
                    - (True | False,  success message | error message)
        """
        # extract task id
        extract_id = self.extractor.extract_taskid(update_values)

        # validate task id
        status, result = self._validate_taskid(extract_id)
        if not status:
            return status, result  # status == False

        task_id = extract_id

        # extract description
        description_match = UPDATE_PATTERN.search(update_values)

        # check if description value is given
        if not description_match:
            return False, "No description given."     

        description = description_match.group(1).strip().title()

        # open todo-app.json to update decription
        todo_records = self.read_json()

        # update description of task with task_id
        for task in todo_records:
            if task_id == task.get("ID"):
                task["Description"] = description

        # save update
        self._save_json(todo_records)

        # return success message
        return True, f"{task_id} description update successful."


    def update_time(self, update_values: str) -> Tuple[bool, str]:
        """To update the time of an existing task based on task id.
            args:
                update_values: The new task values; format = task id task key: task value. E.g 7d588667 tomorrow
            return:
                (bool, str):
                    - (True | False,  success message | error message)
        """
        # extract task id
        extract_id = self.extractor.extract_taskid(update_values)

        # validate task id
        status, result = self._validate_taskid(extract_id)
        if not status:
            return status, result  # status == False

        task_id = extract_id

        # extract time
        time_match = UPDATE_PATTERN.search(update_values)

        # check if time value is given
        if not time_match:
            return False, "No value for time or date."
        
        time_string = time_match.group(1).strip()

        # convert time string to datetime object
        status, result = convert_datestring(time_string)  # convert time string to datetime object

        # conversion fail
        if not status:
            return status, result
    
        # create a task_time variable if conversion is successful
        task_time: str = str(result)

        # open todo-app.json to update decription
        todo_records = self.read_json()

        # update time of task with task_id
        for task in todo_records:
            if task_id == task.get("ID"):
                task["Time"] = task_time

        # save update
        self._save_json(todo_records)

        # return success message
        return True, f"{task_id} time update successful."


    def update_email(self, update_values: str) -> Tuple[bool, str]:
        """To update the email address of an existing task based on task id.
            args:
                update_values: The new task values; format = task id task key: task value. E.g 7d588667 johndoe2025@gmail.com
            return:
                (bool, str):
                    - (True | False,  success message | error message)
        """
        # extract task id
        extract_id = self.extractor.extract_taskid(update_values)

        # validate task id
        status, result = self._validate_taskid(extract_id)
        if not status:
            return status, result  # status == False

        task_id = extract_id

        # extract email
        email_match = UPDATE_PATTERN.search(update_values)

        # check if email value is given
        if not email_match:
            return False, "No value for Email address."  
              
        mail_extract = email_match.group(1).strip()

        # check if email is valid
        valid_mail = self.validator.valid_email(mail_extract)

        if isinstance(valid_mail, str):
            return False, valid_mail   # if email address is not valid

        email = valid_mail.normalized  # convert valid_mail to str

        # open todo-app.json to update decription
        todo_records = self.read_json()

        # update email of task with task_id
        for task in todo_records:
            if task_id == task.get("ID"):
                task["Email"] = email

        # save update
        self._save_json(todo_records)

        # return success message
        return True, f"{task_id} Email update successful"


    def update_tag(self, update_values: str) -> Tuple[bool, str]:
        """To update the tag of an existing task based on task id.
            args:
                update_values: The new task values; format = task id task key: task value. E.g 7d588667 market
            return:
                (bool, str):
                    - (True | False,  success message | error message)
        """
        # extract task id
        extract_id = self.extractor.extract_taskid(update_values)

        # validate task id
        status, result = self._validate_taskid(extract_id)
        if not status:
            return status, result  # status == False

        task_id = extract_id

        # extract tag
        tag_match = UPDATE_PATTERN.search(update_values)

        # check if tag value is given
        if not tag_match:
            return False, "Tag value is empty."

        tag = tag_match.group(1).strip().upper()

        # open todo-app.json to update decription
        todo_records = self.read_json()

        # update tag of task with task_id
        for task in todo_records:
            if task_id == task.get("ID"):
                task["Tag"] = tag

        # save update
        self._save_json(todo_records)

        # return success message
        return True, f"{task_id} Tag update successful"


    def update_priority(self, update_values: str) -> Tuple[bool, str]:
        """To update the priority of an existing task based on task id.
            args:
                update_values: The new task values; format = task id task key: task value. E.g 7d588667 johndoe2025@gmail.com
            return:
                (bool, str):
                    - (True | False,  success message | error message)
        """
        # extract task id
        extract_id = self.extractor.extract_taskid(update_values)

        # validate task id
        status, result = self._validate_taskid(extract_id)
        if not status:
            return status, result  # status == False

        task_id = extract_id

        # extract priority
        priority_match = UPDATE_PATTERN.search(update_values)

        # check if priority value is given
        if not priority_match:
            return False, "Priority Level is empty."

        priority = priority_match.group(1).strip().title()

        # check if priority is valid
        status, result = self.validator.valid_priority_level(priority)

        # if priority is invalid
        if not status:
            return status, result

        # open todo-app.json to update decription
        todo_records = self.read_json()

        # update description of task with task_id
        for task in todo_records:
            if task_id == task.get("ID"):
                task["Priority"] = priority

        # save update
        self._save_json(todo_records)

        # return success message
        return True, f"{task_id} Priority Level update successful"


    def update_status(self, update_values: str) -> Tuple[bool, str]:
        """To update the status of an existing task based on task id.
            args:
                update_values: The new task values; format = task id task key task value. E.g 7d588667 Complete
            return:
                (bool, str):
                    - (True | False,  success message | error message)
        """
        # extract task id
        extract_id = self.extractor.extract_taskid(update_values)

        # validate task id
        status, result = self._validate_taskid(extract_id)
        if not status:
            return status, result  # status == False

        task_id = extract_id

        # extract status
        status_match = UPDATE_PATTERN.search(update_values)

        # check if status value is given
        if not status_match:
            return False, "No value for Status."   

        task_status = status_match.group(1).strip().title()

        # check if status is valid
        status, result = self.validator.valid_status(task_status)

        # if status is invalid
        if not status:
            return status, result

        # open todo-app.json to update status
        todo_records = self.read_json()

        # update status of task with task_id
        if task_status == "Incomplete":
            task_status = "Incomplete  🟩⬜⬜⬜⬜"

        elif task_status == "Complete":
            task_status = "Complete  🟩🟩🟩🟩🟩"

        elif task_status == "Inprogress":
            task_status = "Inprogress  🟩🟩🟨⬜⬜"

        for task in todo_records:
            if task_id == task.get("ID"):
                task["Status"] = task_status

        # save update
        self._save_json(todo_records)

        # return success message
        return True, f"{task_id} Task Status update successful"


# if __name__ == '__main__':
#     db_service = DatabaseService()
#     status, message, tasks = db_service.display_tasks(['ed8f905f'])
#     print(tasks)