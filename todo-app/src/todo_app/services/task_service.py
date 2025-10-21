import re
from datetime import datetime
from typing import Tuple, List, Any
from todo_app.services.database_service import DatabaseService
from todo_app.parsers.validator import Validator
from todo_app.utilis.utils import convert_datestring

class TaskService:
    db_service = DatabaseService()
    validator = Validator()
    
    @classmethod
    def keyword_search(cls, keyword: list[str]) -> Tuple[bool, str, List[Any]]:
        """Search todo-app.json by keywords.
            args:
                keyword: list of word to perform the search query by eg. "meeting"
            return:
                (bool, str, List):
                    - (True | False, empty message | error message, List of search result | empty list)
        """

        # create a regex valid search word from keyword and a regex searcher
        search_string = "|".join(keyword)
        search_pattern = re.compile(search_string, re.IGNORECASE)

        # read todo-app.json
        todo_records = cls.db_service.read_json()

        # check if todo_records is empty
        if not todo_records:
           return False, "No record found - memory is Empty", []

        # initializing a list to store search result
        search_result = []

        # search todo-app.json based on keyword
        try:
            for task in todo_records:
                if any(search_pattern.search(str(value)) for value in task.values()):
                    # store task with keyword to search_result
                    search_result.append(task)

            if not search_result:
                # return an error message is no task has the keyword
                return False, f"No search result found for {keyword}", []

            # keyword search successful. Return result
            return True, "", search_result

        # catch and return error
        except Exception as e:
            return False, str(e), []

    @classmethod
    def tag_filter(cls, tag_list: list[str]) ->Tuple[bool, str, List[Any]]:
        """Filter todo-app.json by task tag using keywords.
            args:
                tag_list: List containing tag filters
            return:
                (bool, str, List[Any]):
                    - (True, empty string, List[dict]) if matches found
                    - (False, error message, empty list) if no matches or error
        """

        # load/read todo-app.json
        todo_records = cls.db_service.read_json()

        # check if it's empty
        if not todo_records:
            return False, "No record found - memory is Empty", []

        # create a valid regex filter string from tag_list and tag filter
        filter_string = "|".join(tag_list)
        filter_pattern = re.compile(filter_string, re.IGNORECASE)

        # initialize list to store filter result
        filter_result = []

        # filter todo_records by tag value
        try:
            for task in todo_records:
                if filter_pattern.search(task["Tag"]):  # filter by tag and store matching task
                    filter_result.append(task)

            if not filter_result:
                return False, f"No search result found for {tag_list}", []

            # return True and result if task is found
            return True, "", filter_result   

        except Exception as e:
            return False, str(e), []

    @classmethod
    def time_filter(cls, time_list: list[str]) -> Tuple[bool, str, List[Any]]:
        """Filter todo-app.json by task time using keywords.
            args:
                tag_list: List containing time filters
            return: 
                (bool, str, List[Any]):
                    - (True, empty string, List[dict]) if matches found
                    - (False, error message, empty list) if no matches or error
        """

        # load/read todo-app.json
        todo_records = cls.db_service.read_json()

        # check if it's empty
        if not todo_records:
            return False, "No record found - memory is Empty", []

        # normalize and validate time
        converted_time = []
        for value in time_list:
            if not value.strip():
                continue # skip empty string
            status, result = convert_datestring(value)
            if not status:
                assert isinstance(result, str)
                return status, result, []  # if conversion fails

            # conversion successful
            assert isinstance(result, datetime)
            converted_time.append(str(result))

        # create a valid regex filter string from time_list and time filter
        print(converted_time)
        filter_string = "|".join([f"^{time.split()[0]}" for time in converted_time])
        filter_pattern = re.compile(filter_string, re.IGNORECASE)
        print(filter_pattern)

        # initialize list to store filter result
        filter_result = []

        # filter todo_records by tag value
        try:
            for task in todo_records:
                if filter_pattern.search(task["Time"]):  # filter by tag and store matching task
                    filter_result.append(task)

            if not filter_result:
                return False, f"No search result found for {time_list}", []

            # return True and result if task is found
            return True, '', filter_result

        except Exception as e:
            return False, str(e), []

    @classmethod
    def priority_filter(cls, priority_list: list[str]) -> Tuple[bool, str, List[Any]]:
        """Filter todo-app.json by task priority level using keywords.
            args:
                tag_list: List containing time filters
            return: 
                (bool, str, List[Any]):
                    - (True, empty string, List[dict]) if matches found
                    - (False, error message, empty list) if no matches or error
        """
        # load/read todo-app.json
        todo_records = cls.db_service.read_json()

        # check if it's empty
        if not todo_records:
            return False, "No record found - memory is Empty", []

        # check if input priority is valid
        for priority in priority_list:
            status, result = cls.validator.valid_priority_level(priority)
            if not status:
                return status, result, []  

        # create a valid regex filter string from priority_list and priority filter
        filter_string = "|".join(priority_list)
        filter_pattern = re.compile(filter_string, re.IGNORECASE)

        # initialize list to store filter result
        filter_result = []

        # filter todo_records by tag value
        try:
            for task in todo_records:
                if filter_pattern.search(task["Priority"]):  # filter by priority and store matching task
                    filter_result.append(task)

            if not filter_result:
                return False, f"No search result found for {'; '.join(priority_list)}", []

            # return True and result if task is found
            return True, "", filter_result

        except Exception as e:
            return False, str(e), []
