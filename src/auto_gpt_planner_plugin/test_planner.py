import json
import os
from unittest import mock
import pytest
from pathlib import Path
from .planner import get_plan_filepath, get_task_filepath, get_plan, get_tasks, create_task, mark_task_as_completed, update_task_status

def test_get_plan_filepath(tmp_path: Path):
    path = tmp_path / "tempdir"
    path.mkdir()
    os.chdir(path)
    
    # Call the function
    plan_filepath = get_plan_filepath()
    
    # Run assertions
    assert plan_filepath.exists(), "The plan.md file does not exist."
    assert plan_filepath.parent.exists(), "The autogpt/auto_gpt_workspace directory does not exist."
    assert (plan_filepath.parent / "plan.md") == plan_filepath, "The returned path does not correspond to the plan.md file."

    # Teardown/cleanup
    plan_filepath.unlink()
    plan_filepath.parent.rmdir()
    

def test_get_task_filepath(tmp_path: Path):
    path = tmp_path / "tempdir"
    path.mkdir()
    os.chdir(path)
    
    # Call the function
    task_filepath = get_task_filepath()
    
    # Run assertions
    assert task_filepath.exists(), "The tasks.json file does not exist."
    assert task_filepath.parent.exists(), "The autogpt/auto_gpt_workspace directory does not exist."
    assert (task_filepath.parent / "tasks.json") == task_filepath, "The returned tasks do not correspond to the tasks.json file."

    # Teardown/cleanup
    task_filepath.unlink()
    task_filepath.parent.rmdir()
    
def test_get_plan_returns_existing_plan(tmp_path: Path):
    path = tmp_path / "tempdir"
    path.mkdir()
    os.chdir(path)
    
    # Setup
    existing_plan = """# Task List and status:\n
- [x] 1: Task One
"""
    plan_filepath = get_plan_filepath()
    plan_filepath.write_text(existing_plan)

    # Call the function
    plan = get_plan()

    # Run assertion
    assert plan == existing_plan, "The existing plan was not returned."

    # Teardown/cleanup
    plan_filepath.unlink()
    plan_filepath.parent.rmdir()

def test_get_plan_generates_new_plan(tmp_path: Path):
    path = tmp_path / "tempdir"
    path.mkdir()
    os.chdir(path)
    
    # Ensure plan.md does not exist
    plan_filepath = get_plan_filepath()
    if plan_filepath.exists():
        plan_filepath.unlink()

    with mock.patch("auto_gpt_planner_plugin.planner.get_tasks") as mock_get_tasks:
        mock_get_tasks.return_value = {"1": ["Task One", True], "2": ["Task Two", False]}

        # Call the function
        plan = get_plan()

        # Run assertions
        expected_plan = (
"""
# Task List and status:
- [x] 1: Task One
- [ ] 2: Task Two

## Notes:
- Use the run_planning_cycle command frequently to keep this plan up to date."""
    )
        assert plan_filepath.exists(), "The plan.md file does not exist."
        assert plan == expected_plan, "The generated plan does not match the expected plan."

        # Restore get_tasks and cleanup
        plan_filepath.unlink()
        plan_filepath.parent.rmdir()
        
def test_get_tasks(tmp_path):
    os.chdir(tmp_path)
    
    sample_tasks = {
        "0": ["Create a detailed checklist for the current plan and goals", False],
        "1": ["Review that every new task is completed", False]
    }
    tasks_file = tmp_path / "tasks.json"
    json.dump(sample_tasks, tasks_file.open("w"))

    tasks = get_tasks()

    assert tasks == sample_tasks
    # Teardown/cleanup
    tasks_file.unlink()
    
def test_create_task(tmp_path): 
    tasks_file = tmp_path / "tasks.json" 
    json.dump({"0": ["Old Task", False]}, tasks_file.open("w"))
    with mock.patch("auto_gpt_planner_plugin.planner.get_task_filepath", return_value=tasks_file): 
        tasks = create_task(task_description="New Task", status=False) 
        assert tasks == {
            "0": ["Old Task", False],
            "1": ["New Task", False]
        }

def test_mark_task_as_completed(tmp_path): 
    tasks_file = tmp_path / "tasks.json" 
    json.dump({"0": ["Task 1", True]}, tasks_file.open("w"))
    with mock.patch("auto_gpt_planner_plugin.planner.get_task_filepath", return_value=tasks_file): 
        result = mark_task_as_completed(0) 
        tasks = get_tasks() 
        assert tasks == {"0": ["Task 1", True]}
        assert result == "Task with ID 0 has been marked as completed."

def test_mark_task_as_completed_task_not_found(capsys):
    with mock.patch("auto_gpt_planner_plugin.planner.get_tasks", return_value={"0": ["Task 1", False]}):
        result = mark_task_as_completed(1) 
        assert "Task with ID 1 not found." in capsys.readouterr().out
        assert result is None

def test_update_task_status(tmp_path): 
    tasks_file = tmp_path / "tasks.json" 
    json.dump({"0": ["Task 1", False]}, tasks_file.open("w"))
    with mock.patch("auto_gpt_planner_plugin.planner.get_task_filepath", return_value=tasks_file): 
        result = update_task_status(0)
        tasks = get_tasks() 
        assert tasks == {"0": ["Task 1", True]} 
        assert result == "Task with ID 0 has been marked as completed."