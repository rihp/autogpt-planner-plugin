from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .planner import Planner
from .tree_of_thoughts import TreeOfThoughts


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
        self.planner = Planner()  # Assuming you have a Planner instance here
        self.tree_of_thoughts = TreeOfThoughts(problem="Define the problem here", model="gpt-3.5-turbo", max_tokens=4096)  # Initialize the TreeOfThoughts instance with required arguments


    def post_prompt(self, prompt):
        """This method is called just after the generate_prompt is called,
        but actually before the prompt is generated.
        Args:
            prompt: The prompt generator.
        Returns:
            The prompt generator.
        """
        # Ensure the planner and tree_of_thoughts have the required methods
        assert hasattr(self.planner, "check_plan"), "Planner object must have a check_plan method"
        assert hasattr(self.planner, "update_plan"), "Planner object must have an update_plan method"
        assert hasattr(self.planner.task_manager, "add_task"), "TaskManager object must have an add_task method"
        assert hasattr(self.planner.task_manager, "load_tasks"), "TaskManager object must have a load_tasks method"
        assert hasattr(self.planner.task_manager, "update_task_status"), "TaskManager object must have an update_task_status method"
        assert hasattr(self.tree_of_thoughts, "add_thought"), "TreeOfThoughts object must have an add_thought method"
        assert hasattr(self.tree_of_thoughts, "remove_thought"), "TreeOfThoughts object must have a remove_thought method"
        assert hasattr(self.tree_of_thoughts, "get_thoughts"), "TreeOfThoughts object must have a get_thoughts method"

        # Add commands to the prompt
        prompt.add_command("check_plan", "Read the plan.md with the next goals to achieve", {}, self.planner.check_plan)
        prompt.add_command("run_planning_cycle", "Improves the current plan.md and updates it with progress", {}, self.planner.update_plan)
        prompt.add_command("create_task", "creates a task with a task id, description and a completed status of False ", {"task_id": "<int>", "task_description": "<The task that must be performed>"}, self.planner.task_manager.add_task)
        prompt.add_command("load_tasks", "Checks out the task ids, their descriptions and a completed status", {}, self.planner.task_manager.load_tasks)
        prompt.add_command("mark_task_completed", "Updates the status of a task and marks it as completed", {"task_id": "<int>"}, self.planner.task_manager.update_task_status)
        prompt.add_command("add_thought", "Adds a thought to the Tree of Thoughts", {"parent_thought": "<The parent thought>", "thought": "<The thought to add>"}, self.tree_of_thoughts.add_thought)
        prompt.add_command("remove_thought", "Removes a thought from the Tree of Thoughts", {"thought": "<The thought to remove>"}, self.tree_of_thoughts.remove_thought)
        prompt.add_command("get_thoughts", "Gets all thoughts from the Tree of Thoughts", {}, self.tree_of_thoughts.get_thoughts)

        return prompt

    def can_handle_on_response(self):
        return False

    def on_response(self, response, *args, **kwargs):
        pass

    def can_handle_on_planning(self):
        return False

    def on_planning(self,prompt, messages):
        pass

    def can_handle_post_planning(self):
        return False

    def post_planning(self, response):
        pass

    def can_handle_pre_instruction(self):
        return False

    def pre_instruction(self, messages):
        pass

    def can_handle_on_instruction(self):
        return False

    def on_instruction(self, messages):
        pass

    def can_handle_post_instruction(self):
        return False

    def post_instruction(self, response):
        pass

    def can_handle_pre_command(self):
        return False

    def pre_command(self, command_name, arguments):
        pass

    def can_handle_post_command(self):
        return False

    def post_command(self, command_name, response):
        pass

    def can_handle_chat_completion(self, messages, model, temperature, max_tokens):
        return False

    def handle_chat_completion(self, messages, model, temperature, max_tokens):
        pass
    
    def can_handle_post_prompt(self):
        return False
