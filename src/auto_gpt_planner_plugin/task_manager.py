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

    def add_task(self, task_description, deadline=None, priority=None, assignee=None):
        """Adds a task to the task manager."""
        task = {
            "task_id": self.task_counter,  # Modify this line
            "task_description": task_description,
            "completed": False,
            "deadline": deadline,
            "priority": priority,
            "assignee": assignee,
            "progress": 0
        }
        self.validate_task(task)
        self.tasks.append(task)
        self.save_tasks()  # Save tasks after adding a new one
        self.task_counter += 1

    def update_task_status(self, task_id, **kwargs):
        """Updates the status of a task in the task manager."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                task.update(kwargs)
        self.save_tasks()  # Save tasks after updating a task's status

    def delete_task(self, task_id):
        """Deletes a task from the task manager."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                self.tasks.remove(task)
        self.save_tasks()  # Save tasks after deleting a task

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
