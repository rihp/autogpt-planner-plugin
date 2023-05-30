from sqlalchemy.orm import Session
from .models import Task, Base, engine
from .task_manager import TaskManager
from .utils import gpt
import itertools
import numpy as np
import argparse


class Planner:
    """
    This class handles the planning functionality.
    """

    def __init__(self):
        """
        Initializes the Planner class and creates a new instance of the TaskManager.
        """
        self.task_manager = TaskManager()

    def run_planning_cycle(self):
        """
        Runs a planning cycle which includes generating a plan, creating tasks from the plan, and executing the tasks.
        """
        plan = self.generate_plan()

        # Create tasks based on the plan
        tasks = self.create_tasks_from_plan(plan)

        # Execute the tasks
        for task in tasks:
            self.task_manager.execute_task(task)

    def generate_plan(self):
        """
        Generates a plan. In this example, a plan is a list of task descriptions.
        Returns:
            plan (list): A list of task descriptions.
        """
        plan = ["Task 1", "Task 2", "Task 3"]
        return plan

    def create_tasks_from_plan(self, plan):
        """
        Creates tasks based on the provided plan.
        Args:
            plan (list): A list of task descriptions.
        Returns:
            tasks (list): A list of Task objects.
        """
        tasks = []
        for i, task_description in enumerate(plan):
            task = Task(
                task_id=str(i),
                description=task_description,
                deadline=None,
                priority=None,
                assignee=None,
                dependencies=None
            )
            tasks.append(task)
            self.task_manager.create_task(task)
        return tasks

    def solve_task(self, task_id):
        """
        Solves a task using the solve function.
        Args:
            task_id (int): The ID of the task to be solved.
        Returns:
            ys (list): The solution to the task.
            info (dict): Information about the steps taken to solve the task.
        """
        # Get the task
        task = self.session.query(Task).filter_by(task_id=task_id).first()

        # Use the solve function to solve the task
        ys, info = self.solve(task)

        # Update the plan with the solution
        self.update_plan(ys)

        return ys, info

    def solve(self, args, task, idx, to_print=True):
        """
        Solves a task.
        Args:
            args (argparse.Namespace): The arguments for the planner.
            task (Task): The task to be solved.
            idx (int): The index of the task.
            to_print (bool, optional): Whether to print the steps taken to solve the task. Defaults to True.
        Returns:
            ys (list): The solution to the task.
            info (dict): Information about the steps taken to solve the task.
        """      
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
    """
    Parses the arguments for the planner.
    Returns:
        args (argparse.Namespace): The arguments for the planner.
    """
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
    """
    If this script is run as the main script, it creates a new Planner and runs a planning cycle.
    """
    planner = Planner()
    planner.run_planning_cycle()

