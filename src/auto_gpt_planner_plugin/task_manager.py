import os
import json
from .utils import process_response

class TaskManager:
    """This class manages tasks."""

    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file
        self.tasks = []

        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as f:
                self.tasks = json.load(f)

    def add_task(self, task_id, task_description, deadline=None, priority=None, assignee=None):
        """Adds a task to the task manager."""
        self.tasks.append({
            "task_id": task_id,
            "task_description": task_description,
            "completed": False,
            "deadline": deadline,
            "priority": priority,
            "assignee": assignee,
            "progress": 0
        })
        self.save_tasks()  # Save tasks after adding a new one

    def load_tasks(self):
        """Loads tasks from the tasks file."""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as f:
                self.tasks = json.load(f)

    def save_tasks(self):
        """Saves tasks to the tasks file."""
        with open(self.tasks_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def get_tasks(self):
        """Gets all tasks from the task manager."""
        return self.tasks

    def get_task(self, task_id):
        """Gets a task from the task manager by task id."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                return task

    def update_task_status(self, task_id, completed):
        """Updates the status of a task in the task manager."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                task["completed"] = completed
        self.save_tasks()  # Save tasks after updating a task's status

    def update_task_progress(self, task_id, progress):
        """Updates the progress of a task in the task manager."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                task["progress"] = progress
        self.save_tasks()  # Save tasks after updating a task's progress

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

        processed_report = process_response(report)  # Process the report using the imported function
        return processed_report
