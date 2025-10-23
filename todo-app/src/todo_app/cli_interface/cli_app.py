import typer  # type: ignore
from todo_app.models.app import TodoApp
from typing import Annotated, List, Optional
from rich import print # type: ignore
from rich import box # type: ignore
from rich.table import Table # type: ignore
from rich.console import Console # type: ignore

# creating reference to TodoApp, typer and Console
app = typer.Typer(help="Nsuso - A Smart Manager for all your activies")
todo_app = TodoApp()
console = Console()

# creating the display table for rich output
DISPLAY_TABLE = Table(box=box.SQUARE)
DISPLAY_TABLE.add_column("ID", style="cyan", no_wrap=True)
DISPLAY_TABLE.add_column("Description", style="magenta")
DISPLAY_TABLE.add_column("Tag", style="")
DISPLAY_TABLE.add_column("Priority", style="yellow")
DISPLAY_TABLE.add_column("Time", style="green")    
DISPLAY_TABLE.add_column("Status", style="")


@app.command(help="Add a new activity to Nsuso", name="add")
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


@app.command(help="Delete saved activites in Nsuso", name="delete")
def delete_tasks(
    indices: Annotated[
        List[str],
        typer.Argument(
            help=(
                "List of task IDs to delete specific tasks or 'all' to delete all tasks. "
                "Example: '011e00e8' 'f981351e'  or 'all'"
            )
        )
    ]
) -> str:
    status, message = todo_app.delete_task(indices)
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")
    
    print(f"[bold green]Success:[/bold green] {message}")  
    

@app.command(help="Display saved activites in Nsuso", name="display")
def display_tasks(
    indices: Annotated[
        List[str],
        typer.Argument(
            help=(
                "List of task IDs to display specific tasks or 'all' to display all tasks. "
                "Example: '011e00e8' 'f981351e'  or 'all'"
            )
        )
    ]
):
    status, message, result = todo_app.display_task(indices)
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")
    
    # display tasks in a table if retrieval is successful
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
    
@app.command(help="Update saved activites in Nsuso", name="update")
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
    if description:
        status, message = todo_app.update_task_description(description)   
    elif time:
        status, message = todo_app.update_task_time(time)    
    elif priority_level:
        status, message = todo_app.update_task_priority(priority_level)    
    elif email_address:
        status, message = todo_app.update_task_email(email_address)    
    else:
        status, message = todo_app.update_task_status(task_status)
        
    if not status:
        return print(f"[bold red]Error:[/bold red] {message}")
        
    return print(f"[bold green]Success:[/bold green] {message}")

@app.command(help='Find and retrieve saved activities in Nsuso based on user query', name='search')
def search_task(
    user_query : Annotated[
        List[str],
        typer.Argument(
            help=()
        )
    ]
):
    status, message, result = todo_app.task_keyword_search()


if __name__ == "__main__":
    app()