from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .planner import Planner

class PlannerPlugin(AutoGPTPluginTemplate):
    """
    This class extends the AutoGPTPluginTemplate to create a task planner plugin for Auto-GPT.
    It adds task planning commands to the prompt and manages the task planning cycle.
    """

    def __init__(self):
        """
        Initialize the PlannerPlugin with a name, version, description, and a Planner instance.
        """
        super().__init__()
        self._name = "AutoGPT-Planner-Plugin"
        self._version = "0.1.1"
        self._description = "This is a simple task planner module for Auto-GPT. It adds the run_planning_cycle " \
                            "command along with other task related commands. Creates a plan.md file and tasks.json " \
                            "to manage the workloads. For help and discussion: " \
                            "https://discord.com/channels/1092243196446249134/1098737397094694922/threads/1102780261604790393"
        self.planner = Planner()  # Create a Planner instance

    def post_prompt(self, prompt):
        """
        This method is called just after the generate_prompt is called,
        but actually before the prompt is generated. It adds commands to the prompt.
        Args:
            prompt: The prompt generator.
        Returns:
            The prompt generator.
        """
        # Add commands to the prompt
        prompt.add_command("check_plan", "Read the plan.md with the next goals to achieve", {}, self.planner.check_plan)
        prompt.add_command("run_planning_cycle", "Improves the current plan.md and updates it with progress", {}, self.planner.run_planning_cycle)
        prompt.add_command("create_task", "Creates a task with a task id, description and a completed status of False ", {"task_id": "<int>", "task_description": "<The task that must be performed>"}, self.planner.task_manager.create_task)
        prompt.add_command("load_tasks", "Checks out the task ids, their descriptions and a completed status", {}, self.planner.task_manager.load_tasks)
        prompt.add_command("mark_task_completed", "Updates the status of a task and marks it as completed", {"task_id": "<int>"}, self.planner.task_manager.execute_task)

        return prompt

    # The following methods are placeholders and do not perform any actions. They are meant to be overridden by subclasses if needed.

    def can_handle_on_response(self):
        """
        Determines if the plugin can handle the on_response event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def on_response(self, response, *args, **kwargs):
        """
        Placeholder method for handling the on_response event.
        Args:
            response: The response from the model.
            *args, **kwargs: Additional arguments and keyword arguments.
        """
        pass

    def can_handle_on_planning(self):
        """
        Determines if the plugin can handle the on_planning event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def on_planning(self,prompt, messages):
        """
        Placeholder method for handling the on_planning event.
        Args:
            prompt: The prompt generator.
            messages: The messages from the user.
        """
        pass

    def can_handle_post_planning(self):
        """
        Determines if the plugin can handle the post_planning event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def post_planning(self, response):
        """
        Placeholder method for handling the post_planning event.
        Args:
            response: The response from the model.
        """
        pass

    def can_handle_pre_instruction(self):
        """
        Determines if the plugin can handle the pre_instruction event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def pre_instruction(self, messages):
        """
        Placeholder method for handling the pre_instruction event.
        Args:
            messages: The messages from the user.
        """
        pass

    def can_handle_on_instruction(self):
        """
        Determines if the plugin can handle the on_instruction event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def on_instruction(self, messages):
        """
        Placeholder method for handling the on_instruction event.
        Args:
            messages: The messages from the user.
        """
        pass

    def can_handle_post_instruction(self):
        """
        Determines if the plugin can handle the post_instruction event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def post_instruction(self, response):
        """
        Placeholder method for handling the post_instruction event.
        Args:
            response: The response from the model.
        """
        pass

    def can_handle_pre_command(self):
        """
        Determines if the plugin can handle the pre_command event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def pre_command(self, command_name, arguments):
        """
        Placeholder method for handling the pre_command event.
        Args:
            command_name: The name of the command.
            arguments: The arguments for the command.
        """
        pass

    def can_handle_post_command(self):
        """
        Determines if the plugin can handle the post_command event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def post_command(self, command_name, response):
        """
        Placeholder method for handling the post_command event.
        Args:
            command_name: The name of the command.
            response: The response from the model
        """

    def can_handle_chat_completion(self, messages, model, temperature, max_tokens):
        """
        Determines if the plugin can handle the chat completion event.
        Args:
            messages: The messages from the user.
            model: The model used for generating responses.
            temperature: The temperature parameter used for response generation.
            max_tokens: The maximum number of tokens allowed in the response.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False

    def handle_chat_completion(self, messages, model, temperature, max_tokens):
        """
        Placeholder method for handling the chat completion event.
        Args:
            messages: The messages from the user.
            model: The model used for generating responses.
            temperature: The temperature parameter used for response generation.
            max_tokens: The maximum number of tokens allowed in the response.
        """
        pass

    def can_handle_post_prompt(self):
        """
        Determines if the plugin can handle the post_prompt event.
        Returns:
            False, as this method is a placeholder and does not perform any actions.
        """
        return False
