import os
import uuid
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from database import Plan, Task

import tasks

Base = declarative_base()

class Utils:
    """
    This class contains utility functions for the AutoGPT Planner Plugin.
    """

    @staticmethod
    def generate_unique_id():
        """
        Generates a unique ID using the uuid library.

        Returns:
            str: A unique ID.
        """
        return str(uuid.uuid4())

    @staticmethod
    def create_database(db_name):
        """
        Creates a new SQLite database with the given name.

        Args:
            db_name (str): The name of the database to be created.

        Returns:
            sqlalchemy.engine.Engine: The engine connected to the new database.
        """
        engine = create_engine(f'sqlite:///{db_name}.db')
        Base.metadata.create_all(engine)
        return engine

    @staticmethod
    def create_session(engine):
        """
        Creates a new SQLAlchemy Session using the given engine.

        Args:
            engine (sqlalchemy.engine.Engine): The engine connected to the database.

        Returns:
            sqlalchemy.orm.session.Session: The new Session.
        """
        Session = sessionmaker(bind=engine)
        return Session()

    @staticmethod
    def query_tasks(session):
        """
        Queries all tasks from the database.

        Args:
            session (sqlalchemy.orm.session.Session): The Session connected to the database.

        Returns:
            list: A list of all tasks in the database.
        """
        return session.query(tasks).all()

    @staticmethod
    def query_plans(session):
        """
        Queries all plans from the database.

        Args:
            session (sqlalchemy.orm.session.Session): The Session connected to the database.

        Returns:
            list: A list of all plans in the database.
        """
        return session.query(Plan).all()

    @staticmethod
    def update_task(session, task_id, completed):
        """
        Updates the completed status of a task in the database.

        Args:
            session (sqlalchemy.orm.session.Session): The Session connected to the database.
            task_id (int): The ID of the task to be updated.
            completed (bool): The new completed status of the task.

        Returns:
            None
        """
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.completed = completed
            session.commit()

    @staticmethod
    def update_plan(session, plan_id, completed):
        """
        Updates the completed status of a plan in the database.

        Args:
            session (sqlalchemy.orm.session.Session): The Session connected to the database.
            plan_id (int): The ID of the plan to be updated.
            completed (bool): The new completed status of the plan.

        Returns:
            None
        """
        plan = session.query(Plan).filter(Plan.id == plan_id).first()
        if plan:
            plan.completed = completed
            session.commit()
