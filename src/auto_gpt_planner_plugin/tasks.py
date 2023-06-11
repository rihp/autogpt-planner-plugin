from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean)

# TaskManager class
class TaskManager:
    """
    The TaskManager class is responsible for managing tasks. It interacts with the tasks database,
    allowing for tasks to be created, updated, and retrieved.
    """

    def __init__(self, db_path):
        """
        Initialize a new TaskManager instance.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.engine = create_engine('sqlite:///' + db_path)
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def create_task(self, task):
        """
        Create a new task in the database.

        Args:
            task (Task): The task to be added to the database.
        """
        session = self.Session()
        session.add(task)
        session.commit()

    def mark_task_complete(self, task_id):
        """
        Mark a task as complete in the database.

        Args:
            task_id (int): The ID of the task to be marked as complete.
        """
        session = self.Session()
        task = session.query(Task).filter_by(id=task_id).first()
        task.completed = True
        session.commit()

    def get_highest_priority_task(self):
        """
        Retrieve the highest priority task from the database.

        Returns:
            Task: The highest priority task.
        """
        session = self.Session()
        task = session.query(Task).filter_by(completed=False).order_by(Task.priority.desc()).first()
        return task

    def complete_tasks_for_goal(self, goal_id):
        """
        Complete all tasks associated with a single goal.

        Args:
            goal_id (int): The ID of the goal.
        """
        session = self.Session()
        tasks = session.query(Task).filter_by(goal_id=goal_id).all()
        for task in tasks:
            task.completed = True
        session.commit()

    def update_goals_for_overall_goal(self, overall_goal_id):
        """
        Update the goals in the plan database to complete the overall goal.

        Args:
            overall_goal_id (int): The ID of the overall goal.
        """
        # This method will depend on how your goals are structured in your database.
        # You'll need to implement this method based on your specific requirements.
        pass
