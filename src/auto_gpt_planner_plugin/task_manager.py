import os
import json
from datetime import datetime

class TaskManager:
    """This class manages tasks."""

    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file
        self.tasks = []
        self.task_counter = 0

        # Load tasks from the tasks file
        self.load_tasks()

    def get_task_file_path(self):
        """Get the path of the tasks.json file."""
        current_working_directory = os.getcwd()
        return os.path.join(current_working_directory, "autogpt", "auto_gpt_workspace", "tasks.json")

    def load_tasks(self):
        """Loads tasks from the tasks file."""
        file_name = self.get_task_file_path()

        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                self.tasks = json.load(f)

    def save_tasks(self):
        """Saves tasks to the tasks file."""
        file_name = self.get_task_file_path()

        with open(file_name, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, task_id=None, task_description=None, deadline=None, priority=None, assignee=None):
        """Adds a task to the task manager."""
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
        self.save_tasks()
        self.task_counter += 1

    def add_tasks(self, task_list):
        """Adds multiple tasks to the task manager."""
        for task in task_list:
            if not task.get('completed', False):
                self.add_task(**task)

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
