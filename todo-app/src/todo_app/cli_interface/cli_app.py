import typer  # type: ignore
from todo_app.models.app import TodoApp
from typing import Annotated, List, Optional
from todo_app.cli_interface.cli_helper import parse_options
from rich import print # type: ignore
from rich import box # type: ignore
from rich.table import Table # type: ignore
from rich.console import Console # type: ignore

# creating reference to TodoApp, typer and Console
app = typer.Typer(help="TaskMate - A Smart Manager for all your activies")
todo_app = TodoApp()
console = Console()

# creating the display table for rich output
DISPLAY_TABLE = Table(box=box.SQUARE)
DISPLAY_TABLE.add_column("ID", no_wrap=True)
DISPLAY_TABLE.add_column("Description", no_wrap=True)
DISPLAY_TABLE.add_column("Tag", no_wrap=True)
DISPLAY_TABLE.add_column("Priority", no_wrap=True)
DISPLAY_TABLE.add_column("Time", no_wrap=True)    
DISPLAY_TABLE.add_column("Status", no_wrap=True)


@app.command(help="Add a new activity to TaskMate", name="add")
def add_task(
    task_input: Annotated[
        str, 
        typer.Argument(
            help=(
                "Task input containing description, tag, priority, due time and optional assigned email. "
                "Example: evening mass @worship #high due:6pm assigned:johndoe34@gmail.com"
            )
        )
    ]
):
    status, message, result = todo_app.add_task(task_input)
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")
    
    # task already exist
    if status and not result:
        return print(f"[bold yellow]Info:[/bold yellow] {message}")
    
    # print message and display table if task is added successfully
    print(f"[bold green]Success:[/bold green] {message}")
    
    DISPLAY_TABLE.add_row(
        result[0]['ID'],
        result[0]['Description'],
        result[0]['Tag'],
        result[0]['Priority'],
        result[0]['Time'],
        result[0]['Status']  
    )
    
    console.print(DISPLAY_TABLE)


@app.command(help="Delete saved activites in TaskMate", name="delete")
def delete_tasks(
    all_input: Optional[str] =
        typer.Option(
            None,
            '--all',
            help="Delete all task or activities in TaskMate using 'delete -all .' command "
        ),
    indices: Optional[str] = 
        typer.Option(
            None,
            '--id',
            parser=parse_options,
            help="Delete selected task or activities based on task ids. Example delete -id 'fe567d7n 890e67b0'"        
        )
    
) -> str:
    
    # if --all argument is used
    if all_input:
        status, message = todo_app.delete_all_task()
        if not status:
            return print(f"[bold yellow]Info:[/bold yellow] {message}")
        
        return print(f"[bold green]Success:[/bold green] {message}")
    
    # if --id argument is used 
    status, message = todo_app.delete_task(indices)
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")
    
    # some task failed or were not found
    if status and 'not found' in  message:
        return print(f"[bold yellow]Info:[/bold yellow] {message}")
    
    # all provided task where found and deleted
    return print(f"[bold green]Success:[/bold green] {message}")  
    

@app.command(help="Display saved activites in TaskMate", name="display")
def display_tasks(
    indices: Optional[List[str]] = 
        typer.Option(
            None,
            "--id",
            parser=parse_options,
            help="List of task IDs to display specific tasks. Example: '011e00e8' 'f981351e'" 
        ),
        
    all_input: Optional[str] = 
        typer.Option(
            None,
            "--all",
            help='Display all avaliable task',
        )        
):  
    # if -all argument is used
    if all_input:
        status, message, result = todo_app.display_all_task()      
        if not status:  # empty Database
            return print(f"[bold yellow]Info:[/bold yellow] {message}")  
        
        # successful.
        for task in result:
            DISPLAY_TABLE.add_row(
                task['ID'],
                task['Description'],
                task['Tag'],
                task['Priority'],
                task['Time'],
                task['Status']  
            )
            
        return console.print(DISPLAY_TABLE)  # display output
        
    # if --id argument is used  
    # unpack indices from a nested list to a list 
    index_values = []
    for list_ in indices:
        index_values.extend(list_)
    
    status, message, result = todo_app.display_task(index_values)
    # No record found for user input
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")
    
    # Empty database.
    elif status and not result:
        return print(f"[bold yellow]Info:[/bold yellow] {message}")
    
    # some successful some not found
    elif status and result and message:
        print(f"[bold yellow]Info:[/bold yellow] {message}")
        for task in result:
            DISPLAY_TABLE.add_row(
                task['ID'],
                task['Description'],
                task['Tag'],
                task['Priority'],
                task['Time'],
                task['Status']  
            )    
                 
    # all provided ids were retrieved
    else:
        for task in result:
            DISPLAY_TABLE.add_row(
                task['ID'],
                task['Description'],
                task['Tag'],
                task['Priority'],
                task['Time'],
                task['Status']  
            )
    
    console.print(DISPLAY_TABLE)
    
@app.command(help="Update saved activites in TaskMate", name="update")
def update_task(
    description : Optional[str] = 
        typer.Option(
            None,
            "--description",
            help="Update task description based on task ID. Example: '011e00e8 attend NGUSA meeting'"
        ),
    time : Optional[str] =
        typer.Option(
            None,
            "--time",
            "--date",
            help="Update task due time based on task ID. Example: '011e00e8 5pm'",
        ),
    priority_level : Optional[str] = 
        typer.Option(
            None,
            "--priority",
            help="Update task priority based on task ID. Example: '011e00e8 high'",
        ),
    email_address : Optional[str] = 
        typer.Option(
            None,
            "--email",
            help="Update task assigned email based on task ID. Example: '011e00e8 matthewjoe65@gmail.com'",
        ),
    task_status : Optional[str] = 
        typer.Option(
            None,
            "--status",
            help="Update task status based on task ID. Example: '011e00e8 Complete'",
        ),
):
    if description: # if --description
        status, message = todo_app.update_task_description(description)   
    elif time:  # if --time/--date
        status, message = todo_app.update_task_time(time)    
    elif priority_level: # if --priority
        status, message = todo_app.update_task_priority(priority_level)    
    elif email_address:  # if --email
        status, message = todo_app.update_task_email(email_address)    
    else:  # if --status
        status, message = todo_app.update_task_status(task_status)
    
    # update not successful   
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")
    
    # task update successful    
    return print(f"[bold green]Success:[/bold green] {message}")


@app.command(help='Find and retrieve saved activities in TaskMate based on command query', name='search')
def search_task(
    user_query : Annotated[
        List[str],
        typer.Argument(
            help=("Search for saved task containing specific words in them")
        )
    ]
):
    status, message, result = todo_app.task_keyword_search(user_query)
    # if search was not successful
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")
    
    # if database is empty
    if status and not result:
        return print(f"[bold yellow]Info:[/bold yellow] {message}")
    
    # all search query found 
    print(f"[bold green]Success:[/bold green] {message}")
    
    for task in result:
        DISPLAY_TABLE.add_row(
            task['ID'],
            task['Description'],
            task['Tag'],
            task['Priority'],
            task['Time'],
            task['Status']
        )
    
    console.print(DISPLAY_TABLE)
    
@app.command(name='list', help="Filter and task by Priority levels, Tags and Time/date in TaskMate run")
def filter_task(
    tag : Optional[List[str]] = 
    typer.Option(
        None,
        "--tag",
        parser=parse_options,
        help="Filter saved tasks based on Tag value Example school, religion etc"
    ),
    priority: Optional[List[str]] = 
    typer.Option(
        None,
        "--priority",
        parser=parse_options,
        help="Filter saved tasks based on Priority levels; High, Mild and Low"
    ),
    due: Optional[List[str]] = 
    typer.Option(
        None,
        "--due",
        "--time",
        "--date",
        parser=parse_options,
        help="Filter saved tasks based on due date or time example 10/02/2024, tomorrow, today, 3pm etc"
    ), 
    status_: Optional[List[str]] = 
    typer.Option(
        None,
        "--status",
        parser=parse_options,
        help="Filter saved tasks based on status example complete, incomplete and inprogress"
    )
):
    
    if tag:
        tags = []  # empty string to store input values
        for value in tag:
            tags.extend(value)
        status, message, result = todo_app.task_tag_filter(tags)
          
    elif priority:
        priorities = []  # empty string to store input values
        for value in priority:
            priorities.extend(value)           
        status, message, result = todo_app.task_priority_filter(priorities)
        
    elif status_:
        task_status = []  # empty string to store input values
        for value in status_:
            task_status.extend(value)           
        status, message, result = todo_app.task_status_filter(task_status)     
           
    else:
        dates = []  # empty string to store input values
        for value in due:
            dates.extend(value)                 
        status, message, result = todo_app.task_time_filter(dates)
        
    # failed filter query    
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")  
    
    # If database is empty
    if status and not result:
        return print(f"[bold yellow]Info:[/bold yellow] {message}")
    
    for task in result:
        DISPLAY_TABLE.add_row(
            task['ID'],
            task['Description'],
            task['Tag'],
            task['Priority'],
            task['Time'],
            task['Status']
        )
    
    console.print(DISPLAY_TABLE)
    
    
if __name__ == "__main__":
    app()