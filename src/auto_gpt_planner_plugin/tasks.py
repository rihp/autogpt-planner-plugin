import os
import json
from datetime import datetime

class Task:
    def __init__(self, task_id=None, description=None, deadline=None, priority=None, assignee=None, dependencies=None):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assignee = assignee
        self.dependencies = dependencies if dependencies else []
        self.completed = False

    def __len__(self):
        # Return the length of the description as the size of the task
        return len(self.description)

    def get_input(self, idx):
        # Retrieve the input associated with the task at the given index
        # In this case, we'll treat the description as the input and return the character at the given index
        return self.description[idx] if idx < len(self.description) else None

    def test_output(self, idx, output):
        # Test the output for the task at the given index
        # In this case, we'll compare the output with the character at the given index in the description
        return self.description[idx] == output if idx < len(self.description) else False

    def mark_completed(self):
        if self.dependencies:
            print("Error: Task has uncompleted dependencies.")
            return
        self.completed = True

    def calculate_progress(self):
        # Calculate the progress of the task based on its attributes
        # In this case, we'll treat the task as completed if there are no dependencies
        return 100 if not self.dependencies else 0

    def validate_task(self):
        # Validate the attributes of the task to ensure data integrity
        # In this case, we'll check that the task_id, description, and deadline are not None
        return self.task_id is not None and self.description is not None and self.deadline is not None

    def __str__(self):
        return f"Task ID: {self.task_id}\nDescription: {self.description}\nDeadline: {self.deadline}\nPriority: {self.priority}\nAssignee: {self.assignee}\nDependencies: {self.dependencies}\nCompleted: {self.completed}"


def get_task(task_id, task_file_path):
    if not os.path.exists(task_file_path):
        print("Error: Task file does not exist.")
        return None
    with open(task_file_path, "r") as file:
        tasks = json.load(file)
        for task in tasks:
            if task["task_id"] == task_id:
                return Task(
                    task_id=task["task_id"],
                    description=task["description"],
                    deadline=task["deadline"],
                    priority=task["priority"],
                    assignee=task["assignee"],
                    dependencies=task.get("dependencies", []),
                )
    print(f"Error: Task with ID {task_id} not found.")
    return None

def update_task_file(task, task_file_path):
    if not os.path.exists(task_file_path):
        print("Error: Task file does not exist.")
        return
    with open(task_file_path, "r+") as file:
        tasks = json.load(file)
        tasks.append(task.__dict__)
        file.seek(0)
        file.truncate()
        json.dump(tasks, file)

def create_task(task_id, description, deadline, priority, assignee, dependencies):
    new_task = Task(task_id, description, deadline, priority, assignee, dependencies)
    update_task_file(new_task, "tasks.json")