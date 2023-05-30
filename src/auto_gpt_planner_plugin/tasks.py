"""
This module provides a class for representing tasks and functions for
working with tasks.

Classes:

* Task: A class representing a task.

Functions:

* get_task(task_id, task_file_path): Get a task by ID from a task file.
* update_task_file(task, task_file_path): Update a task file with a task.
* create_task(task_id, description, deadline, priority, assignee, dependencies): Create a new task and add it to a task file.

"""

import os
import json
from auto_gpt_planner_plugin.tasks import update_task_file


class Task:
    """
    A class representing a task.

    Attributes:

        task_id: The ID of the task.
        description: The description of the task.
        deadline: The deadline for the task.
        priority: The priority of the task.
        assignee: The assignee of the task.
        dependencies: The dependencies of the task.
        completed: Whether the task is completed.

    """

    def __init__(self, task_id=None, description=None, deadline=None, priority=None, assignee=None, dependencies=None):
        """
        Initialize a Task object.

        Args:

            task_id: The ID of the task.
            description: The description of the task.
            deadline: The deadline for the task.
            priority: The priority of the task.
            assignee: The assignee of the task.
            dependencies: The dependencies of the task.

        """

        self.task_id = task_id
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assignee = assignee
        self.dependencies = dependencies if dependencies else []
        self.completed = False

    def __len__(self):
        """
        Return the length of the description as the size of the task.

        Returns:

            The length of the description.

        """

        return len(self.description)

    def get_input(self, idx):
        """
        Retrieve the input associated with the task at the given index.

        Args:

            idx: The index of the input.

        Returns:

            The input at the given index.

        """

        return self.description[idx] if idx < len(self.description) else None

    def test_output(self, idx, output):
        """
        Test the output for the task at the given index.

        Args:

            idx: The index of the output.
            output: The output to test.

        Returns:

            True if the output is correct, False otherwise.

        """

        return self.description[idx] == output if idx < len(self.description) else False

    def mark_completed(self):
        """
        Mark the task as completed.

        Raises:

            RuntimeError: If the task has uncompleted dependencies.

        """

        if self.dependencies:
            raise RuntimeError("Task has uncompleted dependencies.")
        self.completed = True

    def calculate_progress(self):
        """
        Calculate the progress of the task based on its attributes.

        Returns:

            The progress of the task as a percentage.

        """

        return 100 if not self.dependencies else 0

    def validate_task(self):
        """
        Validate the attributes of the task to ensure data integrity.

        Raises:

            RuntimeError: If any of the task attributes are invalid.

        """

        if not self.task_id or not self.description or not self.deadline:
            raise RuntimeError("Invalid task attributes.")

    def __str__(self):
        """
        Print a string representation of the task.

        Returns:

            A string representation of the task.

        """

        return f"Task ID: {self.task_id}\nDescription: {self.description}\nDeadline: {self.deadline}\nPriority: {self.priority}\nAssignee: {self.assignee}\nDependencies: {self.dependencies}\nCompleted: {self.completed}"

    def get_task(task_id, task_file_path):
        """
        Get a task by ID from a task file.

        Args:

            task_id: The ID of the task.
            task_file_path: The path to the task file.

        Returns:

            The task with the given ID, or None if the task is not found.

        """

        if not os.path.exists(task_file_path):
            raise FileNotFoundError(f"Task file {task_file_path} does not exist.")

        with open(task_file_path, "r") as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in {task_file_path}.")

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

            return None

    def update_task_file(task, task_file_path):
        """
        Update a task file with a task.

        Args:

            task: The task to add to the task file.
            task_file_path: The path to the task file.

        """

        if not os.path.exists(task_file_path):
            raise FileNotFoundError(f"Task file {task_file_path} does not exist.")

        with open(task_file_path, "r+") as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in {task_file_path}.")

            tasks.append(task.__dict__)
            file.seek(0)
            file.truncate()
            json.dump(tasks, file)


    def create_task(task_id, description, deadline, priority, assignee, dependencies):
        """
        Create a new task and add it to a task file.

        Args:

            task_id: The ID of the task.
            description: The description of the task.
            deadline: The deadline for the task.
            priority: The priority of the task.
            assignee: The assignee of the task.
            dependencies: The dependencies of the task.

        """

        if not all([task_id, description, deadline, priority, assignee, dependencies]):
            raise ValueError("All task attributes must be provided.")

        new_task = Task(task_id, description, deadline, priority, assignee, dependencies)
        update_task_file(new_task, "tasks.json")
