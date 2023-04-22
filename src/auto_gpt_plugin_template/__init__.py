"""This is a system information plugin for Auto-GPT."""
import os
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

        def say_hello(message):
            """Use this function to return the resulting message of the chat completion """
            return f"{message}"

        prompt.add_command(
            "say_hello", "Say hello and a fact about AutoGPT", {
                "say_hello": "<A Good morning message like hello world here with a fact about AutoGPT>"}, say_hello
        )

        def get_time(message):
            """Use this function to return the current time"""
            return f"{message}"

        prompt.add_command(
            "get_time", "Return the current time", {
                "get_time": "<Current time>"}, get_time
        )

        def read_secrets():
            """
            Use this function to read a secret from the .env file
            """
            return os.getenv("MY_SECRET")

        prompt.add_command(
            "read_secrets", "Read something from the .env", {}, read_secrets
        )

        def check_plan():
                """this function checks if the file plan.md exists, if it doesn't exist it gets created"""

                current_working_directory = os.getcwd()
                workdir = os.path.join(current_working_directory, 'auto_gpt_workspace', 'plan.md')

                file_name = workdir

                if not os.path.exists(file_name):
                    with open(file_name, "w") as file:
                        file.write("""
                                Work Plan:
                                = [x] Create plan.md
                                - [ ] Ask user for input about the plan 
                                - [ ] Use the update_plan command to update it again
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

            # Call the OpenAI API for chat completion
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Improve the following plan, keep the .md format, add more crucial points:\n{prompt}\n",
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5,
            )

            # Extract the improved plan from the response
            improved_plan = response.choices[0].text.strip()

            return improved_plan

        def update_plan(prompt):
                """this function checks if the file plan.txt exists, if it doesn't exist it gets created"""


                current_working_directory = os.getcwd()
                workdir = os.path.join(current_working_directory, 'auto_gpt_workspace', 'plan.md')

                file_name = workdir

                with open(file_name, 'r') as file:
                    data = file.read()

                response = generate_improved_plan(data)

                with open(file_name, "w") as file:
                    file.write(response)
                print(f"{file_name} updated.")
                



        prompt.add_command(
                    "update_plan", "Improving the current plan.txt and updating it with progress", {
                        "consideration": "<Updated Plan here in .md format>",}, update_plan
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
