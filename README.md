<div align="center"><h1 style="font-family: Georgia, serif;">Organize and Prioritize: TaskMate - A Simple CLI Todo App</h1></div>  
<h4 style="font-family: Georgia, serif;">TaskMate is a simple and friendly command-line interface app that helps you keep track of your schedules in this ever-busy 
world - built with Python, Typer, and Rich. TaskMate enables users to create, update, view, and delete tasks directly from the terminal with a Minimalist Monochrome 
interface.</h4>

<img width="3806" height="282" alt="table_output" src="https://github.com/user-attachments/assets/63be931a-3189-4328-b59d-aa7e442cb133" />

<div align='left'><h2 style="font-family: Georgia, serif;">Features</h2>
<ul>
  <li><h4 style="font-family: Georgia, serif;">Add new tasks with descriptions, tags, priorities, due date/time and optional Email.</h4></li>
  <li><h4 style="font-family: Georgia, serif;">Update existing tasks by task ID</h4></li>
  <li><h4 style="font-family: Georgia, serif;">Persistent storage using a JSON file</h4></li>
  <li><h4 style="font-family: Georgia, serif;">Smart natural language parsing using Regex</h4></li>
  <li><h4 style="font-family: Georgia, serif;">Task search by keyword pattern</h4></li>
  <li><h4 style="font-family: Georgia, serif;">Task filter by tags, date and priority levels</h4></li>
</ul>
<div align='left'><h2 style="font-family: Georgia, serif;">Project Structure</h2></div>
<img width="1231" height="1452" alt="TaskMate-project-structure" src="https://github.com/user-attachments/assets/667391a9-e0ad-4222-8953-285dfc40a684" />
<div align='left'><h2 style="font-family: Georgia, serif;">Installation</h2></div>
<h3 style="font-family: Georgia, serif;">Clone the Repository</h3>  
<h4 style="font-family: Georgia, serif;">Clone TaskMate repository using the git clone command and navigate to the project root folder using the cd command</h4>

```powershell
git clone https://github.com/obinna2001/smart-todo-app.git
cd todo-app
```
```powershell
cd todo-app
```
<h3 style="font-family: Georgia, serif;">Install Project Dependencies with Poetry</h3>
<h4 style="font-family: Georgia, serif;">
  If you don’t already have Poetry installed on your system, you can also visit the official installation page - 
  <a href="https://github.com/python-poetry/install.python-poetry.org" style="font-family: Georgia, serif;">
    Poetry Documentation
  </a>
</h4>
<h4 style="font-family: Georgia, serif;">After installing poetry on your system; run the following commands to install and activate TaskMate dependencies</h4>

```powershell
poetry install 
```
```powershell
poetry env activate
```
<div><h2 style="font-family: Georgia, serif;">Usage</h2></div>
<h4 style="font-family: Georgia, serif;">The CLI is powered by Typer — so all commands are discoverable via;</h4>

```powershell
poetry run taskmate --help
```
<h4 style="font-family: Georgia, serif;">Further information on the available command is accessible via poetry run taskmake command --help</h4>
<h4 style="font-family: Georgia, serif;">Example</h4>

```powershell
poetry run taskmate display --help
```
<div><h2 style="font-family: Georgia, serif;">TaskMate Command Sample</h2></div>
<h3 style="font-family: Georgia, serif;">Add a task</h3>
<h4 style="font-family: Georgia, serif;">When adding a task to TaskMate, the format observed in the sample below must be strictly adhered to. Email addresses are optional.</h4>

```powershell
poetry run taskmate add "Buying groceries @shopping #high due: tomorrow assigned: johndoe34@gmail.com
```



