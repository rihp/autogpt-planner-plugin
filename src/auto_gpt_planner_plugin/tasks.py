import os
import json
from datetime import datetime


class Task:
    def __init__(self, task_id=None, description=None, deadline=None, priority=None, assignee=None):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assignee = assignee

    def __len__(self):
        # Return the length or size of the task (if applicable)
        pass

    def get_input(self, idx):
        # Retrieve the input associated with the task at the given index (if applicable)
        pass

    def test_output(self, idx, output):
        # Test the output for the task at the given index (if applicable)
        pass

    def mark_completed(self):
        # Mark the task as completed
        pass

    def calculate_progress(self):
        # Calculate the progress of the task based on its attributes (if applicable)
        pass

    def validate_task(self):
        # Validate the attributes of the task to ensure data integrity
        pass

    def __str__(self):
        return f"Task ID: {self.task_id}\nDescription: {self.description}\nDeadline: {self.deadline}\nPriority: {self.priority}\nAssignee: {self.assignee}"


def get_task(task_id, task_file_path):
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
                )
    return None
