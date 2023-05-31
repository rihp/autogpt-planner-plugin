import os
from sqlalchemy.orm import Session
from .models import Task, Base, engine
import datetime

class TaskManager:
    """
    This class manages tasks in a SQLite database using SQLAlchemy. 
    It provides methods to create, execute, retrieve, and delete tasks, as well as to generate a report of tasks.
    """

    def __init__(self):
        """
        Initialize the task manager by creating a new session with the database engine.
        """
        self.session = Session(engine)

    def create_tasks(self, plan):
        """
        Creates tasks based on the provided plan.
        Args:
            plan (list): A list of task descriptions.
        Returns:
            tasks (list): A list of Task objects.
        """
        tasks = []
        for task_description in plan:
            task = Task(
                description=task_description,
                deadline=None,
                priority=None,
                assignee=None,
                dependencies=None
            )
            tasks.append(task)
        self.session.add_all(tasks)
        self.session.commit()
        return tasks

    def execute_task(self, task_id):
        """
        Mark a task as completed in the database.
        """
        task = self.get_task_by_id(task_id)
        task.completed = True
        self.session.commit()

    def get_task_by_id(self, task_id):
        """
        Retrieve a task from the database by its ID.
        """
        return self.session.query(Task).filter_by(id=task_id).first()

    def get_incomplete_tasks(self):
        """
        Retrieve all tasks from the database that have not been completed.
        """
        return self.session.query(Task).filter_by(completed=False).all()

    def get_tasks_by_priority(self, priority):
        """
        Retrieve all tasks from the database with a specific priority.
        """
        return self.session.query(Task).filter_by(priority=priority).all()

    def add_task(self, task_description, deadline=None, priority=None, assignee=None):
        """
        Add a task to the task manager.
        """
        task = Task(
            description=task_description,
            deadline=deadline,
            priority=priority,
            assignee=assignee,
            dependencies=None
        )
        self.session.add(task)
        self.session.commit()

    def delete_task(self, task_id):
        """
        Deletes a task from the task manager.
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()

    def generate_report(self):
        """
        Generates a report of the tasks.
        """
        total_tasks = self.session.query(Task).count()
        completed_tasks = self.session.query(Task).filter_by(completed=True).count()
        incomplete_tasks = total_tasks - completed_tasks

        report = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "incomplete_tasks": incomplete_tasks,
        }

        return report
