"""
This class manages tasks.

Attributes:
  tasks_file (str): The path of the tasks file.
  tasks (list): A list of tasks.
  task_counter (int): The next task ID.

Methods:
  __init__(self, tasks_file="tasks.json"): Initialize the task manager.
  create_task(self, task): Create a task.
  execute_task(self, task): Execute a task.
  get_task_by_id(self, task_id): Get a task by its ID.
  get_incomplete_tasks(self): Get all tasks that are not yet completed.
  get_tasks_by_priority(self, priority): Get all tasks with a specific priority.
  get_task_file_path(self): Get the path of the tasks.json file.
  load_tasks(self): Load tasks from the tasks file.
  save_tasks(self): Save tasks to the tasks file.
  add_task(self, task_id=None, task_description=None, deadline=None, priority=None, assignee=None): Add a task to the task manager.
  add_tasks(self, task_list): Add multiple tasks to the task manager.
  update_task_status(self, task_id, **kwargs): Update the status of a task in the task manager.
  delete_task(self, task_id): Delete a task from the task manager.
  generate_report(self): Generate a report of the tasks.
  validate_task(self, task): Validate a task before adding it to the task manager.
"""

import os
import json
from datetime import datetime


class TaskManager:

    def __init__(self, tasks_file="tasks.json"):
        """Initialize the task manager."""
        self.tasks_file = tasks_file
        self.tasks = []
        self.task_counter = 0

        # Load tasks from the tasks file
        self.load_tasks()

    def create_task(self, task):
        """Create a task."""
        # Add the task to the task list
        self.tasks.append(task)
        self.save_tasks()

    def execute_task(self, task):
        """Execute a task."""
        # Update the task status to mark it as completed
        task["completed"] = True
        self.save_tasks()

    def get_task_by_id(self, task_id):
        """Get a task by its ID."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                return task
        return None

    def get_incomplete_tasks(self):
        """Get all tasks that are not yet completed."""
        return [task for task in self.tasks if not task["completed"]]

    def get_tasks_by_priority(self, priority):
        """Get all tasks with a specific priority."""
        return [task for task in self.tasks if task["priority"] == priority]

    def get_task_file_path(self):
        """Get the path of the tasks.json file."""
        current_working_directory = os.getcwd()
        return os.path.join(current_working_directory, "autogpt", "auto_gpt_workspace", "tasks.json")

    def load_tasks(self):
        """Load tasks from the tasks file."""
        file_name = self.get_task_file_path()

        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                self.tasks = json.load(f)

    def save_tasks(self):
        """Save tasks to the tasks file."""
        file_name = self.get_task_file_path()

        with open(file_name, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, task_id=None, task_description=None, deadline=None, priority=None, assignee=None):
        """Add a task to the task manager."""
        task = {
            "task_id": task_id if task_id is not None else self.task_counter,
            "task_description": task_description if task_description is not None else "No description",
            "completed": False,
            "deadline": deadline if deadline is not None else "No deadline",
            "priority": priority if priority is not None else "No priority",
            "assignee": assignee if assignee is not None else "No assignee",
            "progress": 0,
            "tree_of_thoughts": {}  # New attribute for Tree of Thoughts
        }
        self.validate_task(task)
        self.tasks.append(task)
        self.task_counter += 1
        self.logic_counter += 1  # Increment the logic counter

        # Only save tasks every 5 logic cycles
        if self.logic_counter % 5 == 0:
            self.save_tasks()

    def add_tasks(self, task_list):
        """Adds multiple tasks to the task manager."""
        for task in task_list:
            if not task.get('completed', False):
                self.add_task(**task)
                self.logic_counter += 1  # Increment the logic counter

        # Save tasks if the logic counter is a multiple of 5 after adding all tasks
        if self.logic_counter % 5 == 0:
            self.save_tasks()

    def update_task_status(self, task_id, **kwargs):
        """Updates the status of a task in the task manager."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                task.update(kwargs)
        self.save_tasks()

    def delete_task(self, task_id):
        """Deletes a task from the task manager."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                self.tasks.remove(task)
        self.save_tasks()

    def generate_report(self):
        """Generates a report of the tasks."""
        report = {
            "total_tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks if t["completed"]]),
            "incomplete_tasks": len([t for t in self.tasks if not t["completed"]]),
            "tasks_by_priority": {
                "high": len([t for t in self.tasks if t["priority"] == "high"]),
                "medium": len([t for t in self.tasks if t["priority"] == "medium"]),
                "low": len([t for t in self.tasks if t["priority"] == "low"]),
            },
            "tasks_by_assignee": {},
        }

        for task in self.tasks:
            if task["assignee"] not in report["tasks_by_assignee"]:
                report["tasks_by_assignee"][task["assignee"]] = 0
            report["tasks_by_assignee"][task["assignee"]] += 1

        return report

    def validate_task(self, task):
        """Validates a task before adding it to the task manager."""
        required_fields = ["task_id", "task_description", "completed", "progress"]

        for field in required_fields:
            if field not in task:
                raise ValueError(f"Task is missing {field}")

        if not isinstance(task["task_id"], int):
            raise ValueError("Task ID must be an integer")

        if not isinstance(task["task_description"], str):
            raise ValueError("Task description must be a string")

        if not isinstance(task["completed"], bool):
            raise ValueError("Task completion status must be a boolean")

        if not isinstance(task["progress"], int) or not (0 <= task["progress"] <= 100):
            raise ValueError("Task progress must be an integer between 0 and 100")

        if task["deadline"] is not None:
            try:
                datetime.strptime(task["deadline"], "%Y-%m-%d")
            except ValueError:
                raise ValueError("Task deadline must be a string in the format 'YYYY-MM-DD'")

        if task["priority"] is not None and task["priority"] not in ["high", "medium", "low", None]:
            raise ValueError("Task priority must be 'high', 'medium', 'low', or None")

        if task["assignee"] is not None and not isinstance(task["assignee"], str):
            raise ValueError("Task assignee must be a string")


if __name__ == "__main__":
    task_manager = TaskManager()

    # Create a task
    task = {
        "task_id": 1,
        "task_description": "Write a blog post",
        "deadline": "2023-06-01",
        "priority": "high",
        "assignee": "Bard",
    }
    task_manager.add_task(task)

    # Get the task by its ID
    task = task_manager.get_task_by_id(1)
    print(task)

    # Get all tasks that are not yet completed
    incomplete_tasks = task_manager.get_incomplete_tasks()
    print(incomplete_tasks)

    # Get all tasks with a specific priority
    high_priority_tasks = task_manager.get_tasks_by_priority("high")
    print(high_priority_tasks)

    # Generate a report of the tasks
    report = task_manager.generate_report()
    print(report)
