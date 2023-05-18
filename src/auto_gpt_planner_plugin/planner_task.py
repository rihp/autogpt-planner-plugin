from datetime import date


class PlannerTask:
    def __init__(self,
                 description: str,
                 task_id=None,
                 completed: bool = False,
                 reoccuring: bool = False,
                 timestamp=None):

        self.task_id = task_id
        self.description = description
        self.completed = completed
        self.reoccuring = reoccuring
        if timestamp is None:
            self.timestamp = date.today()
        else:
            self.timestamp = timestamp
