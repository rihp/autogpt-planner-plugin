import os
import openai
from .task_manager import TaskManager
from .utils import process_response
from .tree_of_thoughts import TreeOfThoughts

class Planner:
    """This class handles the planning functionality."""

    def __init__(self):
        # Set the model and maximum tokens for the OpenAI API
        self.MODEL = self.get_env_var('PLANNER_MODEL', self.get_env_var('FAST_LLM_MODEL', 'gpt-3.5-turbo'))
        self.MAX_TOKENS = int(self.get_env_var('PLANNER_TOKEN_LIMIT', '4096'))
        # Initialize the task manager
        self.task_manager = TaskManager()

    def get_env_var(self, var_name, default_value):
        """Get the value of an environment variable or return a default value if it is not set."""
        return os.getenv(var_name, default_value)

    def get_plan_file_path(self):
        """Get the path of the plan.md file."""
        current_working_directory = os.getcwd()
        return os.path.join(current_working_directory, "autogpt", "auto_gpt_workspace", "plan.md")

    def check_plan(self):
        """
        Check if the plan.md file exists in the specified directory, 
        if it doesn't exist, a new one is created with a default content.
        """
        file_name = self.get_plan_file_path()

        if not os.path.exists(file_name):
            # Create and write the default content to the plan.md file if it does not exist
            try:
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
            except Exception as e:
                print(f"Failed to create {file_name}: {e}")
                return None

        # Read the existing or newly created plan.md file
        try:
            with open(file_name, "r") as file:
                return file.read()
        except Exception as e:
            print(f"Failed to read {file_name}: {e}")
            return None

    def update_plan(self):
        """
        Update the existing plan based on task status and generate an improved plan.
        Incorporate the best solution from the Tree of Thoughts of each task into the plan.
        """
        file_name = self.get_plan_file_path()

        # Read the existing plan.md file
        try:
            with open(file_name, 'r') as file:
                data = file.read()
        except Exception as e:
            print(f"Failed to read {file_name}: {e}")
            return None

        # Generate an improved plan
        response = self.generate_improved_plan(data)

        # Incorporate the best solution from the Tree of Thoughts of each task into the plan
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            problem = task["task_description"]
            tree_of_thoughts = self.generate_tree_of_thoughts(problem)
            best_solution = self.evaluate_tree_of_thoughts(tree_of_thoughts)
            response += f"\nBest solution for task '{task['task_id']}': {best_solution}"

        # Write the improved plan to the plan.md file
        try:
            with open(file_name, "w") as file:
                file.write(response)
            print(f"{file_name} updated.")
        except Exception as        e:
            print(f"Failed to update {file_name}: {e}")
            return None

        return response

    def generate_improved_plan(self, prompt: str) -> str:
        """
        Generate an improved plan using OpenAI's ChatCompletion functionality.
        This function takes the existing plan and tasks as inputs and returns an improved plan.
        """
         # Load the current tasks
        tasks = self.task_manager.get_tasks()

        # Call the OpenAI API for chat completion
        try:
            response = openai.ChatCompletion.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "system","content": "You are an assistant that improves and adds crucial points to plans in .md format.",
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
        except Exception as e:
            print(f"Failed to generate improved plan: {e}")
            return None

        # Process the OpenAI response
        try:
            processed_response = process_response(response)
        except Exception as e:
            print(f"Failed to process response: {e}")
            return None

        return processed_response
    
    def generate_tree_of_thoughts(self, problem):
        """
        Generate a Tree of Thoughts for a given problem using the GPT-4 model.
        """
        tree_of_thoughts = TreeOfThoughts(problem, self.MODEL, self.MAX_TOKENS)
        return tree_of_thoughts.generate()

    def evaluate_tree_of_thoughts(self, tree_of_thoughts):
        """
        Evaluate a Tree of Thoughts using the GPT-4 model and select the best solution.
        """
        best_solution = tree_of_thoughts.evaluate()
        return best_solution

