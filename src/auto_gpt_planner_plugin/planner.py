import os
import openai
from .task_manager import TaskManager
from .utils import process_response

class Planner:
    """This class handles the planning functionality."""

    def __init__(self):
        self.MODEL = os.getenv('PLANNER_MODEL', os.getenv('FAST_LLM_MODEL', 'gpt-3.5-turbo'))
        self.MAX_TOKENS = int(os.getenv('PLANNER_TOKEN_LIMIT', '4096'))
        self.task_manager = TaskManager()

    def check_plan(self):
        """
        Check if the plan.md file exists in the specified directory, 
        if it doesn't exist, a new one is created with a default content.
        """
        current_working_directory = os.getcwd()
        workdir = os.path.join(current_working_directory, "autogpt", "auto_gpt_workspace", "plan.md")
        file_name = workdir

        if not os.path.exists(file_name):
            # Create and write the default content to the plan.md file if it does not exist
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

        # Read the existing or newly created plan.md file
        with open(file_name, "r") as file:
            return file.read()

    def update_plan(self):
        """
        Update the existing plan based on task status and generate an improved plan.
        """
        current_working_directory = os.getcwd()
        workdir = os.path.join(current_working_directory, 'autogpt', 'auto_gpt_workspace', 'plan.md')
        file_name = workdir

        # Read the existing plan.md file
        with open(file_name, 'r') as file:
            data = file.read()

        # Generate an improved plan
        response = self.generate_improved_plan(data)

        # Write the improved plan to the plan.md file
        with open(file_name, "w") as file:
            file.write(response)
        print(f"{file_name} updated.")

        return response

    def generate_improved_plan(self, prompt: str) -> str:
        """
        Generate an improved plan using OpenAI's ChatCompletion functionality.
        This function takes the existing plan and tasks as inputs and returns an improved plan.
        """
        # Load the current tasks
        tasks = self.task_manager.get_tasks()

        # Call the OpenAI API for chat completion
        response = openai.ChatCompletion.create(
            model=self.MODEL,
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
            max_tokens=self.MAX_TOKENS,
            n=1,
            temperature=0.5,
        )

        # Process the OpenAI
