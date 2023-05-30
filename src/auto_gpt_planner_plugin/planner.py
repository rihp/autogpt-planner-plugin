"""
This class handles the planning functionality.

Args:
    --backend: The name of the OpenAI API backend to use.
    --temperature: The temperature of the OpenAI API.
    --task: The name of the task to solve.
    --task_file_path: The path to the file that contains the task description.
    --task_start_index: The index of the first task to solve.
    --task_end_index: The index of the last task to solve.
    --naive_run: If True, the planner will run in a naive mode. This mode is not as efficient as the non-naive mode, but it is easier to understand.
    --prompt_sample: The prompt to use when generating samples.
    --method_generate: The method to use for generating samples.
    --method_evaluate: The method to use for evaluating samples.
    --method_select: The method to use for selecting samples.
    --n_generate_sample: The number of samples to generate.
    --n_evaluate_sample: The number of samples to evaluate.
    --n_select_sample: The number of samples to select.

Returns:
    - The list of solutions to the tasks.
"""

import os
import argparse
import numpy as np
from .task_manager import TaskManager
from .utils import gpt, gpt_usage
from .tasks import get_task
import itertools


class Planner:
    """This class handles the planning functionality."""

    def __init__(self, args):
        # Set the model and maximum tokens for the OpenAI API
        self.MODEL = self.get_env_var('PLANNER_MODEL', self.get_env_var('FAST_LLM_MODEL', 'gpt-3.5-turbo'))
        self.MAX_TOKENS = int(self.get_env_var('PLANNER_TOKEN_LIMIT', '4096'))
        # Initialize the task manager
        self.task_manager = TaskManager()

    def get_env_var(self, var_name, default_value):
        """Get the value of an environment variable or return a default value if it is not set."""
        return os.getenv(var_name, default_value)

    def run_planning_cycle(self):
        # Generate a plan
        plan = self.generate_plan()

        # Create tasks based on the plan
        tasks = self.create_tasks_from_plan(plan)

        # Execute the tasks
        for task in tasks:
            self.task_manager.create_task(task)
            self.task_manager.execute_task(task)

    def generate_plan(self):
        # For this example, let's say a plan is just a list of task descriptions
        plan = ["Task 1", "Task 2", "Task 3"]
        return plan

    def create_tasks_from_plan(self, plan):
        # For this example, let's say a task is just a dictionary with a task_id and a task_description
        tasks = []
        for i, task_description in enumerate(plan):
            task = {
                "task_id": str(i),
                "task_description": task_description
            }
            tasks.append(task)
        return tasks

    def solve_task(self, task_id, task_file_path, i):
        """
        Solve a task using the solve function from the first script.
        This function takes a task ID and a task file path as inputs.
        """
        # Parse the arguments for the solve function
        args = self.parse_args()
        args.task = task_id
        args.task_file_path = task_file_path

        # Get the task
        task = get_task(args.task, args.task_file_path)

        # Use the solve function to solve the task
        ys, info = self.solve(args, task, i)

        # Update the plan with the solution
        self.update_plan(ys)

        return ys, info

    def solve(self, args, task, idx, to_print=True):
        print(gpt)
        x = task.get_inputx  # input
        ys = ['']  # current output candidates
        infos = []
        for step in range(task.steps):
            # generation
            if args.method_generate == 'sample':
                new_ys = [self.get_samples(task, x, y, args.n_generate_sample, prompt_sample=args.prompt_sample, stop=task.stops[step]) for y in ys]
            elif args.method_generate == 'propose':
                new_ys = [self.get_proposals(task, x, y) for y in ys]
            new_ys = list(itertools.chain(*new_ys))
            ids = list(range(len(new_ys)))
            # evaluation
            if args.method_evaluate == 'vote':
                values = self.get_votes(task, x, new_ys, args.n_evaluate_sample)
            elif args.method_evaluate == 'value':
                values = self.get_values(task, x, new_ys, args.n_evaluate_sample)

            # selection
            if args.method_select == 'sample':
                ps = np.array(values) / sum(values)
                select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
            elif args.method_select == 'greedy':
                select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
            select_new_ys = [new_ys[select_id] for select_id in select_ids]

            # log
            if to_print:
                sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
                print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')

            infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
            ys = select_new_ys

        if to_print:
            print(ys)
        return ys, {'steps': infos}

def parse_args():
    """Parse the arguments for the planner."""
    args = argparse.ArgumentParser()
    args.add_argument('--backend', type=str, choices=['gpt-4', 'gpt-3.5-turbo'], default='gpt-4')
    args.add_argument('--temperature', type=float, default=0.7)

    args.add_argument('--task', type=str, required=True, choices=['game24', 'text', 'crosswords'])
    args.add_argument('--task_file_path', type=str, required=True)
    args.add_argument('--task_start_index', type=int, default=900)
    args.add_argument('--task_end_index', type=int, default=1000)

    args.add_argument('--naive_run', action='store_true')
    args.add_argument('--prompt_sample', type=str, choices=['standard', 'cot'])  # only used when method_generate = sample, or naive_run

    args.add_argument('--method_generate', type=str, choices=['sample', 'propose'])
    args.add_argument('--method_evaluate', type=str, choices=['value', 'vote'])
    args.add_argument('--method_select', type=str, choices=['sample', 'greedy'])
    args.add_argument('--n_generate_sample', type=int, default=1)  # only thing needed if naive_run
    args.add_argument('--n_evaluate_sample', type=int, default=1)
    args.add_argument('--n_select_sample', type=int, default=1)

    args = args.parse_args()
    return args

if __name__ == '__main__':
    planner = Planner()
    planner.run_planning_cycle()

