import re
from datetime import datetime
from typing import Union, Tuple, List, Any
from todo_app.services.database_service import read_json
from todo_app.parsers.validator import valid_priority_level
from todo_app.utilis.utils import convert_datestring


def keyword_search(
    keyword: list[str],
) -> Union[Tuple[bool, str], Tuple[bool, List[Any]]]:
    """Search todo-app.json by keywords.
    args:
        keyword: list of word to perform the search query by eg. "meeting"
    return:
        result: list of matching task
        bool: True, False
        mssg: error message
    """

    # create a regex valid search word from keyword and a regex searcher
    search_string = "|".join(keyword)
    search_pattern = re.compile(search_string, re.IGNORECASE)

    # read todo-app.json
    todo_records = read_json()

    # check if todo_records is empty
    if not todo_records:
        mssg = "⛔ No record found - memory is Empty"
        return False, mssg

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
            mssg = f"No search result found for {keyword}"
            return False, mssg

        # keyword search successful. Return result
        return True, search_result

    # catch and return error
    except Exception as e:
        mssg = str(e)
        return False, mssg


def tag_filter(
    tag_list: list[str],
) -> Union[Tuple[bool, str], Tuple[bool, List[Any]]]:
    """Filter todo-app.json by task tag using keywords.
    args:
        tag_list: List containing tag filters
    return:
        (bool, list | str):
            - (True, search_result) if matches found
            - (False, mssg) if no matches or error
    """

    # load/read todo-app.json
    todo_records = read_json()

    # check if it's empty
    if not todo_records:
        mssg = "⛔ No record found - memory is Empty"
        return False, mssg

    # create a valid regex filter string from tag_list and tag filter
    filter_string = "|".join(tag_list)
    filter_pattern = re.compile(filter_string, re.IGNORECASE)

    # initialize list to store filter result
    filter_result = []

    # filter todo_records by tag value
    try:
        for task in todo_records:
            if filter_pattern.search(
                task["Tag"]
            ):  # filter by tag and store matching task
                filter_result.append(task)

        if not filter_result:
            mssg = f"No search result found for {tag_list}"
            return False, mssg

        # return True and result if task is found
        return True, filter_result

    except Exception as e:
        mssg = str(e)
        return False, mssg


def time_filter(
    time_list: list[str],
) -> Union[Tuple[bool, str], Tuple[bool, List[Any]]]:
    """Filter todo-app.json by task time using keywords.
    args:
        tag_list: List containing time filters
    return:
        (bool, list | str):
            - (True, filter_result) if matches found
            - (False, mssg) if no matches or error
    """

    # load/read todo-app.json
    todo_records = read_json()

    # check if it's empty
    if not todo_records:
        mssg = "⛔ No record found - memory is Empty"
        return False, mssg

    # normalize and validate time
    converted_time = []
    for value in time_list:
        status, result = convert_datestring(value)
        if not status:
            assert isinstance(result, str)
            return status, result  # if conversion fails

        # conversion successful
        assert isinstance(result, datetime)
        converted_time.append(str(result))

    # create a valid regex filter string from time_list and time filter
    filter_string = "|".join(converted_time)
    filter_pattern = re.compile(filter_string, re.IGNORECASE)

    # initialize list to store filter result
    filter_result = []

    # filter todo_records by tag value
    try:
        for task in todo_records:
            if filter_pattern.search(
                task["Time"]
            ):  # filter by tag and store matching task
                filter_result.append(task)

        if not filter_result:
            mssg = f"No search result found for {time_list}"
            return False, mssg

        # return True and result if task is found
        return True, filter_result

    except Exception as e:
        mssg = str(e)
        return False, mssg


def priority_filter(
    priority_list: list[str],
) -> Union[Tuple[bool, str], Tuple[bool, List[Any]]]:
    """Filter todo-app.json by task priority level using keywords.
    args:
        tag_list: List containing time filters
    return:
        (bool, list | str):
            - (True, filter_result) if matches found
            - (False, mssg) if no matches or error
    """
    # load/read todo-app.json
    todo_records = read_json()

    # check if it's empty
    if not todo_records:
        mssg = "⛔ No record found - memory is Empty"
        return False, mssg

    # check if input priority is valid
    for priority in priority_list:
        status, result = valid_priority_level(priority)
        if not status:
            return status, f"{result}. {priority} is given"

    # create a valid regex filter string from priority_list and priority filter
    filter_string = "|".join(priority_list)
    filter_pattern = re.compile(filter_string, re.IGNORECASE)

    # initialize list to store filter result
    filter_result = []

    # filter todo_records by tag value
    try:
        for task in todo_records:
            if filter_pattern.search(
                task["Priority"]
            ):  # filter by priority and store matching task
                filter_result.append(task)

        if not filter_result:
            mssg = f"No search result found for {priority_list}"
            return False, mssg

        # return True and result if task is found
        return True, filter_result

    except Exception as e:
        mssg = str(e)
        return False, mssg
