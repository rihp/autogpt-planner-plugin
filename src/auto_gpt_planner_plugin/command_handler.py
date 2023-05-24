import json
from task_manager import TaskManager

class CommandHandler:
    """This class handles the command functionality."""

    def __init__(self, planner):
        # Initialize the planner
        self.planner = planner

    def execute_command(self, command_name, args):
        if command_name not in self.commands:
            print(f"Unknown command '{command_name}'")
            return

        command = self.commands[command_name]
        function_name = command['function']
        required_args = command['args']

        # Check if the provided arguments match the required arguments
        if set(args.keys()) != set(required_args):
            print(f"Invalid arguments for command '{command_name}'. Required arguments: {required_args}")
            return

        # Get the function from the task manager
        function = getattr(self.task_manager, function_name)

        # Call the function with the provided arguments
        result = function(**args)

        return result

    def handle_generate_tree_of_thoughts_command(self, task_id):
        """
        Handle the command to generate a Tree of Thoughts for a task.
        """
        task = self.planner.task_manager.get_task(task_id)
        if task is None:
            print(f"No task found with ID {task_id}")
            return

        problem = task["task_description"]
        tree_of_thoughts = self.planner.generate_tree_of_thoughts(problem)
        print(f"Generated Tree of Thoughts for task {task_id}: {tree_of_thoughts}")

    def handle_evaluate_tree_of_thoughts_command(self, task_id):
        """
        Handle the command to evaluate a Tree of Thoughts for a task.
        """
        task = self.planner.task_manager.get_task(task_id)
        if task is None:
            print(f"No task found with ID {task_id}")
            return

        problem = task["task_description"]
        tree_of_thoughts = self.planner.generate_tree_of_thoughts(problem)
        best_solution = self.planner.evaluate_tree_of_thoughts(tree_of_thoughts)
        print(f"Best solution for task {task_id}: {best_solution}")