"""This is a system information plugin for Auto-GPT."""
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar

from auto_gpt_plugin_template import AutoGPTPluginTemplate
from dotenv import load_dotenv


PromptGenerator = TypeVar("PromptGenerator")

with open(str(Path(os.getcwd()) / ".env"), "r", encoding="utf-8") as fp:
    load_dotenv(stream=fp)

class Message(TypedDict):
    role: str
    content: str


class HelloWorldPlugin(AutoGPTPluginTemplate):
    """
    This is a system information plugin for Auto-GPT which
    adds the system information to the prompt.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-Plugin-SystemInfo"
        self._version = "0.1.2"
        self._description = "This is system info plugin for Auto-GPT."

        self.execute_local_commands = (
            os.getenv("EXECUTE_LOCAL_COMMANDS", "False") == "True"
        )

        if not self.execute_local_commands:
            print(
                "WARNING:",
                "SystemInformationPlugin: EXECUTE_LOCAL_COMMANDS is false. "
                "System information will not be added to the context.",
            )


        
    


    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """This method is called just after the generate_prompt is called,
        but actually before the prompt is generated.
        Args:
            prompt (PromptGenerator): The prompt generator.
        Returns:
            PromptGenerator: The prompt generator.
        """

        def check_plan():
                """this function checks if the file plan.md exists, if it doesn't exist it gets created"""

                current_working_directory = os.getcwd()
                workdir = os.path.join(current_working_directory, 'autogpt', 'auto_gpt_workspace', 'plan.md')

                file_name = workdir

                if not os.path.exists(file_name):
                    with open(file_name, "w") as file:
                        file.write("""
                        # Task List and status:

                        - [ ] Task description here
                        - [ ] Second task description goes here
                                """)
                    print(f"{file_name} created.")
                
                with open(file_name, 'r') as file:
                    return file.read()

        prompt.add_command(
                    "check_plan", "Read the plan.md with the next goals to achieve", {}, check_plan
                )   

        def generate_improved_plan(prompt: str) -> str:
            """Generate an improved plan using OpenAI's ChatCompletion functionality"""

            import openai
            print(prompt)
            print(dir(prompt))

            tasks = load_tasks()

            # Call the OpenAI API for chat completion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an assistant that improves and adds crucial points to plans in .md format."
                    },
                    {
                        "role": "user",
                        "content": f"Update the following plan given the task status below, keep the .md format:\n{prompt}\nInclude the current tasks in the improved plan, keep mind of their status and track them with a checklist:\n{tasks}\Revised version should comply with the contests of the tasks at hand:"
                    },
                ],
                max_tokens=1500,
                n=1,
                temperature=0.5,
            )

            # Extract the improved plan from the response
            improved_plan = response.choices[0].message.content.strip()
            return improved_plan

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

        prompt.add_command(
                    "run_planning_cycle", "Improves the current plan.md and updates it with progress", {}, update_plan
                )   

        print(dir(prompt))
        print(prompt.constraints)
        print(prompt.commands)

        def create_task(task_id=None, task_description:str=None, status=False):
            task = {"description": task_description, "completed": status}
            tasks = load_tasks()
            tasks[str(task_id)] = task

            current_working_directory = os.getcwd()
            workdir = os.path.join(current_working_directory, 'autogpt', 'auto_gpt_workspace', 'tasks.json')
            file_name = workdir

            with open(file_name, "w") as f:
                json.dump(tasks, f)

            return tasks

        prompt.add_command(
            "create_task", "creates a task with a task id, description and a completed status of False ", 
            {"task_id": "<int>", "task_description":"<The task that must be performed>"}, create_task
        )   

        def load_tasks() -> dict:
            current_working_directory = os.getcwd()
            workdir = os.path.join(current_working_directory, 'autogpt', 'auto_gpt_workspace', 'tasks.json')
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

        prompt.add_command(
            "load_tasks", "Checks out the task ids, their descriptionsand a completed status", 
            {}, load_tasks
        )  

        def update_task_status(task_id):
            tasks = load_tasks()

            if str(task_id) not in tasks:
                print(f"Task with ID {task_id} not found.")
                return

            tasks[str(task_id)]['completed'] = True

            current_working_directory = os.getcwd()
            workdir = os.path.join(current_working_directory, 'autogpt', 'auto_gpt_workspace', 'tasks.json')
            file_name = workdir

            with open(file_name, "w") as f:
                json.dump(tasks, f)

            return f"Task with ID {task_id} has been marked as completed."

        
        prompt.add_command(
            "mark_task_completed", "Updates the status of a task and marks it as completed", 
            {"task_id": "<int>"}, update_task_status
        )  

        return prompt

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.
        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.
        Returns:
            bool: True if the plugin can handle the on_response method."""
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        pass

    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.
        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        """This method is called before the planning chat completion is done.
        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.
        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return False

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completion is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.
        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return False

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        """This method is called before the instruction chat is done.
        Args:
            messages (List[Message]): The list of context messages.
        Returns:
            List[Message]: The resulting list of messages.
        """
        pass

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.
        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        """This method is called when the instruction chat is done.
        Args:
            messages (List[Message]): The list of context messages.
        Returns:
            Optional[str]: The resulting message.
        """
        pass

    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.
        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return False

    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.
        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return False

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.
        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.
        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """
        pass

    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.
        Returns:
            bool: True if the plugin can handle the post_command method."""
        return False

    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.
        Args:
            command_name (str): The command name.
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """This method is called to check that the plugin can
          handle the chat_completion method.
        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
          Returns:
              bool: True if the plugin can handle the chat_completion method."""
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        """This method is called when the chat completion is done.
        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            str: The resulting response.
        """
        pass
