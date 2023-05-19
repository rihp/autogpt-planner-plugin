import datetime
import sqlite3

from ..planner_protocol import PlannerProtocol
from ..planner_task import PlannerTask


class SqlitePlanner(PlannerProtocol):
    plan = ""

    def __init__(self, db_path: str = "autogpt-planner.db"):
        self.db_con = sqlite3.connect(db_path)
        self.db_cur = self.db_con.cursor()
        self.db_cur.execute(
            '''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, 
                instance VARCHAR, 
                description TEXT,
                reoccuring INTEGER,
                timestamp DATE, 
                completed INTEGER);
                ''')

        self.db_cur.execute('''
            CREATE INDEX IF NOT EXISTS idx_tasks_itc ON tasks (instance, timestamp, completed);
            ''')

    def run_planning_cycle(self, name: str = "PlannerGPT") -> str:
        # TODO implement this method to return a plan
        self.plan = "This is the plan: get current task will return the task to work on, once the task is done, get a new one."
        return self.plan

    def get_current_task(self, name: str = "PlannerGPT") -> PlannerTask:
        res = self.db_cur.execute('''
            SELECT 
                id, description, reoccuring, timestamp, completed 
            FROM tasks
            WHERE instance = ? AND completed = 0 ORDER BY timestamp LIMIT 1;
        ''', (name,))
        task_data = res.fetchone()
        if task_data is None:
            raise Exception("No tasks found, query: " + res)

        return PlannerTask(
            task_id=task_data[0],
            description=task_data[1],
            reoccuring=bool(task_data[2]),
            timestamp=datetime.datetime.fromtimestamp(float(task_data[3])),
            completed=bool(task_data[4])
        )

    def get_task_for_id(self, task_id: str, name: str = "PlannerGPT") -> PlannerTask:
        res = self.db_cur.execute('''
            SELECT 
                id, description, reoccuring, timestamp, completed 
            FROM tasks
            WHERE id = ?;
        ''', (task_id,))

        task_data = res.fetchone()

        if task_data is None:
            raise Exception("No tasks found.")

        return PlannerTask(
            task_id=task_data[0],
            description=task_data[1],
            reoccuring=bool(task_data[2]),
            timestamp=datetime.datetime.fromtimestamp(float(task_data[3])),
            completed=bool(task_data[4])
        )

    def add_task(self, task: PlannerTask, name: str = "PlannerGPT") -> str:
        if task.task_id is None:
            self.db_cur.execute('''
                INSERT INTO tasks (instance, description, reoccuring, timestamp, completed) 
                VALUES (?, ?, ?, ?, ?);
            ''', (name, task.description, task.reoccuring, datetime.datetime.timestamp(task.timestamp), 0))
            self.db_con.commit()
            return str(self.db_cur.lastrowid)
        raise Exception("let's not add tasks with an id set")

    def complete_task(self, task: PlannerTask, name: str = "PlannerGPT"):
        self.db_cur.execute('''
            UPDATE tasks
            SET completed = 1
            WHERE id = ?;
        ''', (str(task.task_id),))
        self.db_con.commit()

    def optimize_schedule(self, name: str = "PlannerGPT"):
        return "the schedule was successfully optimized."
