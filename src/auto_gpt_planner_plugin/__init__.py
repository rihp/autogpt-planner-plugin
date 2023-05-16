"""This is a task planning system plugin for Auto-GPT. It is able to create tasks, elaborate a plan, improve upon it
and check it again to keep on track.

built by @rihp on github"""

from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar

from auto_gpt_plugin_template import AutoGPTPluginTemplate

from .planner import Planner
from .implementations.file_planner import FilePlanner
from .implementation_factory import ImplementationFactory

from autogpt.config.config import Config
from autogpt.config.ai_config import AIConfig

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class PlannerPlugin(AutoGPTPluginTemplate):
    """
    This is a task planner system plugin for Auto-GPT which 
    adds the task planning commands to the prompt.
    """

    def __init__(self):
        super().__init__()
        self._name = "AutoGPT-Planner-Plugin"
        self._version = "0.1.1"
        self._description = "This is a simple task planner module for Auto-GPT. It adds the run_planning_cycle " \
                            "command along with other task related commands. Creates a plan.md file and tasks.json " \
                            "to manage the workloads. For help and discussion: " \
                            "https://discord.com/channels/1092243196446249134/1098737397094694922/threads/1102780261604790393"

        settings = AIConfig.load(Config().ai_settings_file)

        self.planner = Planner(ImplementationFactory().get_planner(
            agent_id=settings.ai_name,
            implementation_name="FilePlanner"
        ))

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        def run_planning_cycle():
            return self.planner.run_planning_cycle()

        def add_task(description: str):
            # TODO: more params
            return self.planner.add_task(description=description)

        def complete_task(task_id: str):
            return self.planner.complete_task(task_id=task_id)

        def get_current_task():
            return self.planner.get_current_task()

        prompt.add_command(
            "run_planning_cycle",
            "Improves the current plan.md and updates it with progress",
            {},
            run_planning_cycle,
        )

        prompt.add_command(
            "create_task",
            "creates a task with a description",
            {
                "description": "<The task that must be performed>",
            },
            add_task,
        )

        prompt.add_command(
            "mark_task_completed",
            "Updates the status of a task and marks it as completed",
            {"task_id": "<the id of the task to mark completed>"},
            complete_task,
        )

        prompt.add_command(
            "get_current_task",
            "Returns the task you are currently supposed to work on",
            {},
            get_current_task
        )

        # Todo see if there is a better way of aliasing commands, if not consider contribution
        prompt.add_command(
            "get_next_task",
            "Returns the task you are supposed to work on",
            {},
            get_current_task
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
