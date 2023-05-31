import uuid
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Define the base class for SQLAlchemy declarative base model. 
# The Base is the base class which maintains a catalog of classes and tables relative to that base.
Base = declarative_base()

class Task(Base):
    """
    This class represents a Task table in the database. 
    It inherits from the SQLAlchemy Base class and includes columns for id, description, deadline, priority, assignee, dependencies, and completed status.
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)  # Unique identifier for each task
    description = Column(String)  # Description of the task
    deadline = Column(DateTime)  # Deadline for the task
    priority = Column(Enum('low', 'medium', 'high'))  # Priority level of the task
    assignee = Column(String)  # Person assigned to the task
    dependencies = Column(String)  # Dependencies of the task
    completed = Column(Boolean, default=False)  # Whether the task has been completed

    def __init__(self, id=None, description=None, deadline=None, priority=None, assignee=None, dependencies=None):
        """
        Initializes a new instance of the Task class.
        """
        self.id = id
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assignee = assignee
        self.dependencies = dependencies
        self.completed = False

    def __repr__(self):
        """
        Returns a string representation of the Task instance.
        """
        return f"<Task(id={self.id}, description={self.description}, deadline={self.deadline}, priority={self.priority}, assignee={self.assignee}, completed={self.completed})>"

# Generate a unique identifier
uuid_str = str(uuid.uuid4())

# Use the UUID to create a unique database name
db_name = f"tasks_{uuid_str}.db"

# Create the engine. The engine is the starting point for any SQLAlchemy application. It’s “home base” for the actual database and its DBAPI.
engine = create_engine(f'sqlite:///{db_name}')
