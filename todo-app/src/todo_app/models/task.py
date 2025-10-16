from todo_app.parsers.extractor import extract_task, extract_date, extract_priority_level, extract_email, extract_tag
from todo_app.utilis.utils import generate_taskID
from todo_app.utilis.json_utils import upload_task


class TodoApp:
    def __init__(self, user_input: str):
        self.user_input = user_input

    def add_task(self):
        """Assign a task based on user input and store in JSON_DB"""
        description_status, task_description = extract_task(self.user_input)
        time_status, task_time = extract_date(self.user_input)
        priority_status, task_priority = extract_priority_level(self.user_input)
        tag_status, task_tag = extract_tag(self.user_input)
        email_status, task_email = extract_email(self.user_input)
        
        # checking if user input is valid
        if not description_status: 
            return task_description
        
        if not time_status:
            return task_time
        
        if not priority_status:
            return task_priority
        
        if not tag_status:
            return task_tag
        
        if not email_status:
            if task_email == 'Email not found.':
                task_email = ""

            elif task_email == "Invalid Email address":
                raise task_email
        
        # create a unique task id
        task_id = generate_taskID(self.user_input)

        task = {
            'ID': task_id,
            'Time': str(task_time),
            'Description': task_description,
            'Priority': task_priority,
            'Tag': task_tag,
            'Email': task_email
        }

        # save task to todo-app.json
        return upload_task(task)
    
    def delete_task():
        pass


if __name__ == '__main__':
    sample = "study bible and pray @worship #high due:9pm assigned:okeyobinna2001@gmail.com"
    app = TodoApp(sample)
    print(app.add_task())