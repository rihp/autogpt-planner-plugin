# Planner Plugin
Simple planning commands for planning leveraged with chatgpt3.5

### Getting started

After you clone the template from the original repo (https://github.com/rihp/autogpt-planner-plugin)

# New commands
```
prompt.add_command(
    "check_plan",
    "Read the plan.md with the next goals to achieve",
    {},
    check_plan,
)

prompt.add_command(
    "run_planning_cycle",
    "Improves the current plan.md and updates it with progress",
    {},
    update_plan,
)

prompt.add_command(
    "create_task",
    "creates a task with a task id, description and a completed status of False ",
    {
        "task_id": "<int>",
        "task_description": "<The task that must be performed>",
    },
    create_task,
)

prompt.add_command(
    "load_tasks",
    "Checks out the task ids, their descriptionsand a completed status",
    {},
    load_tasks,
)

prompt.add_command(
    "mark_task_completed",
    "Updates the status of a task and marks it as completed",
    {"task_id": "<int>"},
    update_task_status,
)
```

## CODE SAMPLES

Example of generating an improved plan
```python
def generate_improved_plan(prompt: str) -> str:
    """Generate an improved plan using OpenAI's ChatCompletion functionality"""

    import openai

    tasks = load_tasks()

    # Call the OpenAI API for chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that improves and adds crucial points to plans in .md format.",
            },
            {
                "role": "user",
                "content": f"Update the following plan given the task status below, keep the .md format:\n{prompt}\nInclude the current tasks in the improved plan, keep mind of their status and track them with a checklist:\n{tasks}\Revised version should comply with the contests of the tasks at hand:",
            },
        ],
        max_tokens=1500,
        n=1,
        temperature=0.5,
    )
```


Example of loading the .env
```python

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        def read_secrets(prompt):
            """
            Use this function to read a secret from the .env file
            """
            return os.getenv("MY_SECRET")

        prompt.add_command(
            "read_secrets", "Read something from the .env", {
                "read_secrets": "Something will be printed here"}, read_secrets
        )

        return prompt
```




## Testing workflow

Create something like this and run it through the CLI
```
cd ../Auto-GPT-Plugins && zip -ru ../Auto-GPT/plugins/Auto-GPT-Plugins.zip . ; ../Auto-GPT && python3 -m autogpt --debug
```