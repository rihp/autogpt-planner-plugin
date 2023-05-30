import uuid
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    description = Column(String)
    deadline = Column(DateTime)
    priority = Column(Enum('low', 'medium', 'high'))
    assignee = Column(String)
    dependencies = relationship("Task")
    completed = Column(Boolean, default=False)

    def __init__(self, task_id=None, description=None, deadline=None, priority=None, assignee=None, dependencies=None):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.assignee = assignee
        self.dependencies = dependencies if dependencies else []
        self.completed = False

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, description={self.description}, deadline={self.deadline}, priority={self.priority}, assignee={self.assignee}, dependencies={self.dependencies}, completed={self. Completed})>"

# Generate a unique identifier
uuid_str = str(uuid.uuid4())

# Use the UUID to create a unique database name
db_name = f"tasks_{uuid_str}.db"

# Create the engine
engine = create_engine(f'sqlite:///{db_name}')
