import json
import os
from pathlib import Path


#===================================================================================================
# Centralized functions for loading plan.md and tasks.json
#===================================================================================================
def get_plan_filepath():
    """This function checks if the file plan.md exists, if it doesn't exist it gets created"""
    cwd = Path.cwd()
    plan_filepath = cwd / "autogpt" / "auto_gpt_workspace" / "plan.md"
    
    # Create the plan.md file if it doesn't exist
    plan_filepath.parent.mkdir(parents=True, exist_ok=True)
    plan_filepath.touch(exist_ok=True)
    return plan_filepath

def get_task_filepath():
    """This function checks if the file tasks.json exists, if it doesn't exist it gets created"""
    cwd = Path.cwd()
    task_filepath = cwd / "autogpt" / "auto_gpt_workspace" / "tasks.json"
    
    # Create the tasks.json file if it doesn't exist
    task_filepath.parent.mkdir(parents=True, exist_ok=True)
    task_filepath.touch(exist_ok=True)
    return task_filepath
#===================================================================================================

#===================================================================================================
#===================================================================================================
# Centralized functions for loading plan.md and tasks.json and returning the current contents
#===================================================================================================
def get_plan() -> str:
    """"This function returns the current plan in the plan.md file"""
    plan_filepath = get_plan_filepath()
    plan = plan_filepath.read_text()
    
    if not plan:
        tasks = get_tasks()
        plan = "\n# Task List and status:\n"
        
        for task_id, task in tasks.items():
            if task[1]:
                plan += f"- [x] {task_id}: {task[0]}\n"
            else:
                plan += f"- [ ] {task_id}: {task[0]}\n"
                
        plan += (
            "\n## Notes:\n"
            "- Use the run_planning_cycle command frequently to keep this plan up to date."
        )
        plan_filepath.write_text(plan)
    return plan

def check_plan() -> str:
    """(Legacy) Alias for get_plan."""
    return get_plan()

def get_tasks() -> dict[str: list[str, bool]]:
    """This function returns the current tasks in the tasks.json file"""
    task_filepath = get_task_filepath()
    try:
        tasks = json.load(task_filepath.open("r"))
    except json.JSONDecodeError:
        print(f"Error loading tasks from {task_filepath}. Resetting tasks.")
        tasks = {}
        
    if not tasks:
        tasks = {
            "0": ["Create a detailed checklist for the current plan and goals", False],
            "1": ["Review that every new task is completed", False],
        }
        json.dump(tasks, task_filepath.open("w"))
        
    return tasks

def load_tasks() -> dict[str: list[str, bool]]:
    """(Legacy) Alias for get_tasks."""
    return get_tasks()
#===================================================================================================

#===================================================================================================
#===================================================================================================
# Functions for creating tasks and marking them as completed
#===================================================================================================
def create_task(task_id: int|None =None, task_description: str=None, status=False):
    """This function creates a task in the tasks.json file."""
    if (task_id in (None, "None") or task_id not in (0, "0")) and not task_id:
        tasks = get_tasks()
        highest_task_id = max(int(key) for key in tasks.keys())
        task_id = highest_task_id + 1
    else:
        try:
            task_id = int(task_id)
        except ValueError:
            raise ValueError("task_id must be an integer.")
        
    if task_description is None:
        raise ValueError("task_description cannot be None.")
    
    tasks[str(task_id)] = [task_description, (status==True or status=="True")]
    json.dump(tasks, get_task_filepath().open("w"))
    return tasks

def mark_task_as_completed(task_id: int):
    """This function marks a task as completed in the tasks.json file"""
    tasks = get_tasks()
    
    if str(task_id) not in tasks:
        print(f"Task with ID {task_id} not found.")
        return
    
    tasks[str(task_id)] = [tasks[str(task_id)][0], True]
    json.dump(tasks, get_task_filepath().open("w"))
    return f"Task with ID {task_id} has been marked as completed."
    
def update_task_status(task_id):
    """(Legacy) Alias for mark_task_as_completed."""
    return mark_task_as_completed(task_id)
#===================================================================================================


#===================================================================================================
# Functions for updating the plan.md file
#===================================================================================================
def update_plan():
    """this function checks if the file plan.md exists, if it doesn't exist it gets created"""

    plan_filepath = get_plan_filepath()
    plan = check_plan()

    improved_plan = generate_improved_plan(plan)
    if improved_plan:
        plan_filepath.write_text(improved_plan)
        
    print(f"{plan_filepath} updated.")
    print(f"New plan:\n{improved_plan}")
    return improved_plan

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
#===================================================================================================