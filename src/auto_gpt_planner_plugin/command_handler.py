import json
from task_manager import TaskManager

class CommandHandler:
    def __init__(self, commands_file):
        with open(commands_file, 'r') as f:
            self.commands = json.load(f)
        self.task_manager = TaskManager()

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
