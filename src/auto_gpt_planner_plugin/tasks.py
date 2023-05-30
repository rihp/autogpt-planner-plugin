from models import Task
from database import Session
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class TaskService:
    def __init__(self):
        self.session = Session()

    def get_task(self, task_id):
        try:
            task = self.session.query(Task).filter_by(task_id=task_id).first()
            logger.info(f"Retrieved task with ID {task_id}")
            return task
        except Exception as e:
            logger.error(f"Failed to retrieve task with ID {task_id}: {e}")
            return None

    def save_task(self, task):
        try:
            self.session.add(task)
            self.session.commit()
            logger.info(f"Saved task with ID {task.task_id}")
        except Exception as e:
            logger.error(f"Failed to save task with ID {task.task_id}: {e}")

    def create_task(self, task_id, description, deadline, priority, assignee, dependencies):
        new_task = Task(task_id=task_id, description=description, deadline=deadline, priority=priority, assignee=assignee, dependencies=dependencies)
        self.save_task(new_task)

    def mark_task_completed(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.mark_completed()
            self.save_task(task)

    def __del__(self):
        self.session.close()
