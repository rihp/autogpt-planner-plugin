import os
import json
from datetime import datetime

class TaskManager:
    """This class manages tasks."""

    def __init__(self, tasks_file=None):
        current_working_directory = os.getcwd()
        default_tasks_file = os.path.join(current_working_directory, "autogpt", "auto_gpt_workspace", "tasks.json")
        self.tasks_file = tasks_file if tasks_file else default_tasks_file
        self.tasks = []

        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as f:
                self.tasks = json.load(f)

    def validate_task(self, task):
        if not task.get('task_id'):
            raise ValueError('Task ID cannot be empty')
        if not task.get('task_description'):
            raise ValueError('Task description cannot be empty')
        if any(t['task_id'] == task['task_id'] for t in self.tasks):
            raise ValueError('Task ID already in use')
        if task.get('deadline'):
            try:
                datetime.strptime(task.get('deadline'), '%Y-%m-%d')
            except ValueError:
                raise ValueError('Deadline must be a valid date in YYYY-MM-DD format')

    def add_task(self, task_id, task_description, deadline=None, priority=None, assignee=None):
        """Adds a task to the task manager."""
        task = {
            "task_id": task_id,
            "task_description": task_description,
            "completed": False,
            "deadline": deadline,
            "priority": priority,
            "assignee": assignee,
            "progress": 0
        }
        self.validate_task(task)
        self.tasks.append(task)
        self.save_tasks()
        if self.planner:
            self.planner.update_plan()


    def load_tasks(self):
        """Loads tasks from the tasks file."""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, "r") as f:
                    self.tasks = json.load(f)
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def save_tasks(self):
        """Saves tasks to the tasks file."""
        try:
            with open(self.tasks_file, "w") as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {e}")

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
        self.save_tasks()
        if self.planner:
            self.planner.update_plan()

    def delete_task(self, task_id):
        """Deletes a task from the task manager."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                self.tasks.remove(task)
        self.save_tasks()
        if self.planner:
            self.planner.update_plan()

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