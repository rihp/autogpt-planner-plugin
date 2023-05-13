import datetime

from .planner_protocol import PlannerProtocol
from .planner_task import PlannerTask


class Planner:
    def __init__(self, planner: PlannerProtocol, name: str = "PlannerGPT"):
        self.planner = planner
        self.name = name

    def run_planning_cycle(self) -> str:
        """run a planning cycle"""
        return self.planner.run_planning_cycle(name=self.name)

    def get_current_task(self) -> str:
        task = self.planner.get_current_task(name=self.name);
        return f"Current task with\ntask_id: '{task.task_id}'\n is:\n{task.description}\n\n"

    def get_task_for_id(self, task_id: str) -> str:
        task = self.planner.get_task_for_id(task_id=task_id, name=self.name)
        return f"Found Task with task_id: '{task.task_id}'\ndescription:\n{task.description}\n" \
               f"completed: {task.completed}\nreoccuring: {task.reoccuring}\n" \
               f"scheduled for: {task.timestamp.isoformat()}"

    def add_task(self, description: str, reoccuring: bool = False, timestamp=None) -> str:
        if timestamp is None:
            timestamp = datetime.datetime.now()
        else:
            timestamp = datetime.datetime.fromisoformat(timestamp)

        task = PlannerTask(
            description=description,
            task_id=None,
            completed=False,
            reoccuring=reoccuring,
            timestamp=timestamp
        )
        task_id = self.planner.add_task(task=task, name=self.name)

        return f"Task with task_id: '{task_id}' has been added"

    def complete_task(self, task_id: str) -> str:
        self.planner.complete_task(self.planner.get_task_for_id(task_id=task_id, name=self.name))
        return f"The Task with task_id: '{task_id}' has been marked as completed"

    def optimize_schedule(self) -> str:
        self.planner.optimize_schedule(self.name)
        return f"Schedule has been optimized"
