import json
import os

from ..planner_protocol import PlannerProtocol
from ..planner_task import PlannerTask


def check_plan():
    """this function checks if the file plan.md exists, if it doesn't exist it gets created"""

    current_working_directory = os.getcwd()
    workdir = os.path.join(
        current_working_directory, "autogpt", "auto_gpt_workspace", "plan.md"
    )

    file_name = workdir

    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            file.write(
                """
                # Task List and status:
                - [ ] Create a detailed checklist for the current plan and goals
                - [ ] Finally, review that every new task is completed
                
                ## Notes:
                - Use the run_planning_cycle command frequently to keep this plan up to date.
                        """
            )
        print(f"{file_name} created.")

    with open(file_name, "r") as file:
        return file.read()


def update_plan():
    """this function checks if the file plan.md exists, if it doesn't exist it gets created"""

    current_working_directory = os.getcwd()
    workdir = os.path.join(current_working_directory, 'autogpt', 'auto_gpt_workspace', 'plan.md')

    file_name = workdir

    with open(file_name, 'r') as file:
        data = file.read()

    response = generate_improved_plan(data)

    with open(file_name, "w") as file:
        file.write(response)
    print(f"{file_name} updated.")

    return response


def generate_improved_plan(prompt: str) -> str:
    """Generate an improved plan using OpenAI's ChatCompletion functionality"""

    import openai

    tasks = load_tasks()

    model = os.getenv('PLANNER_MODEL', os.getenv('FAST_LLM_MODEL', 'gpt-3.5-turbo'))
    max_tokens = os.getenv('PLANNER_TOKEN_LIMIT', os.getenv('FAST_TOKEN_LIMIT', 1500))
    temperature = os.getenv('PLANNER_TEMPERATURE', os.getenv('TEMPERATURE', 0.5))

    # Call the OpenAI API for chat completion
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that improves and adds crucial points to plans in .md format.",
            },
            {
                "role": "user",
                "content": f"Update the following plan given the task status below, keep the .md format:\n{prompt}\n"
                           f"Include the current tasks in the improved plan, keep mind of their status and track them "
                           f"with a checklist:\n{tasks}\n Revised version should comply with the contents of the "
                           f"tasks at hand:",
            },
        ],
        max_tokens=int(max_tokens),
        n=1,
        temperature=float(temperature),
    )

    # Extract the improved plan from the response
    improved_plan = response.choices[0].message.content.strip()
    return improved_plan


def create_task(task_id=None, task_description: str = None, status=False):
    task = {"description": task_description, "completed": status}
    tasks = load_tasks()
    tasks[str(task_id)] = task

    current_working_directory = os.getcwd()
    workdir = os.path.join(
        current_working_directory, "autogpt", "auto_gpt_workspace", "tasks.json"
    )
    file_name = workdir

    with open(file_name, "w") as f:
        json.dump(tasks, f)

    return tasks


def load_tasks() -> dict:
    current_working_directory = os.getcwd()
    workdir = os.path.join(
        current_working_directory, "autogpt", "auto_gpt_workspace", "tasks.json"
    )
    file_name = workdir

    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            f.write("{}")

    with open(file_name) as f:
        try:
            tasks = json.load(f)
            if isinstance(tasks, list):
                tasks = {}
        except json.JSONDecodeError:
            tasks = {}

    return tasks


def update_task_status(task_id):
    tasks = load_tasks()

    if str(task_id) not in tasks:
        print(f"Task with ID {task_id} not found.")
        return

    tasks[str(task_id)]["completed"] = True

    current_working_directory = os.getcwd()
    workdir = os.path.join(
        current_working_directory, "autogpt", "auto_gpt_workspace", "tasks.json"
    )
    file_name = workdir

    with open(file_name, "w") as f:
        json.dump(tasks, f)

    return f"Task with ID {task_id} has been marked as completed."


class FilePlanner(PlannerProtocol):
    def __init__(self):
        self.plan = check_plan()

    def run_planning_cycle(self, name: str = "PlannerGPT") -> str:
        self.plan = update_plan()
        return self.plan

    def get_current_task(self, name: str = "PlannerGPT") -> PlannerTask:
        tasks = load_tasks()
        for task_id, task in tasks.items():
            if not task["completed"]:
                return PlannerTask(description=task["description"], task_id=task_id)
        raise Exception("No tasks found.")

    def get_task_for_id(self, task_id: str, name: str = "PlannerGPT") -> PlannerTask:
        tasks = load_tasks()

        if task_id not in tasks:
            raise Exception(f"Task with ID {task_id} not found.")

        return PlannerTask(description=tasks[task_id]["description"], task_id=task_id,
                           completed=tasks[task_id]["completed"])

    def add_task(self, task: PlannerTask, name: str = "PlannerGPT") -> str:
        if task.task_id is None:
            task_id = str(len(load_tasks()) + 1)
            create_task(task_id=task_id, task_description=task.description)
            return task_id

        raise Exception("let's not add tasks with an id set")

    def complete_task(self, task: PlannerTask, name: str = "PlannerGPT"):
        update_task_status(task.task_id)

    def optimize_schedule(self, name: str = "PlannerGPT"):
        return "the schedule was successfully optimized."
