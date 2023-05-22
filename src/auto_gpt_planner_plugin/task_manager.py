import os
import json

class TaskManager:
    """This class manages tasks."""

    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file
        self.tasks = []

        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as f:
                self.tasks = json.load(f)

    def validate_task(self, task):
        if not task.get('task_description'):
            raise ValueError('Task description cannot be empty')
        if any(t['task_id'] == task['task_id'] for t in self.tasks):
            raise ValueError('Task ID already in use')

    def add_task(self, task):
        """Adds a task to the task manager."""
        self.validate_task(task)
        self.tasks.append(task)
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

    def get_tasks(self, completed=None):
        """Gets all tasks from the task manager."""
        if completed is None:
            return self.tasks
        return [t for t in self.tasks if t['completed'] == completed]

    def get_task(self, task_id):
        """Gets a task from the task manager by task id."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                return task

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
