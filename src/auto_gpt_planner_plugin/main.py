from database import DatabaseManager
from planner import Planner
from tasks import TaskManager
from utils import Utils

def main():
    """
    The main function of the AutoGPT Planner Plugin.
    """

    # Create a new database
    db_name = "autogpt_planner"
    engine = Utils.create_database(db_name)

    # Create a new Session
    session = Utils.create_session(engine)

    # Create a new DatabaseManager
    db_manager = DatabaseManager(session)

    # Create a new Planner
    planner = Planner(db_manager)

    # Create a new TaskManager
    task_manager = TaskManager(db_manager)

    # Start up and run the initial planning cycle
    planner.initial_planning_cycle()

    # Generate a new plan SQL database to use for future use
    db_manager.generate_plan_database()

    # Generate task SQL database that contains all task available to the plugin
    db_manager.generate_task_database()

    # Generate a new plan based on the goals given to AutoGPT
    planner.generate_plan()

    # Generate unique task based on the new plan
    task_manager.generate_tasks()

    # Solve the first task with the highest priority using the solve method
    task_manager.solve_highest_priority_task()

    # Mark the task complete
    task_manager.mark_task_complete()

    # Update the unique task SQL database
    db_manager.update_task_database()

    # Complete tasks until done with a single goal
    task_manager.complete_tasks()

    # Once all tasks are complete, it marks the goal done
    planner.mark_goal_done()

    # Once a goal is done, it updates the goals to complete the overall goal
    planner.update_goals()

if __name__ == "__main__":
    main()
