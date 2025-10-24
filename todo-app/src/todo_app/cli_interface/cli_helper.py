from typing import List

def parse_options(value:str) -> List[str]:
    """Split typer Option input into a list
        args:
            value: typer string input
        return:
            value_list = A list of values based on typer input
    """
    
    value_list = [item for item in value.split(' ')]
    return value_list
   