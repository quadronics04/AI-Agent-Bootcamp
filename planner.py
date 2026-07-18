from ai_client import ask_ai


def create_plan(user_goal: str) -> str:
    """
    Create a step-by-step plan for completing the user's goal.

    The planner does not directly complete the task.
    It only decides how the task should be completed.
    """

    planning_prompt = f"""
You are the planning component of an AI agent.

User goal:
{user_goal}

Create a clear and practical execution plan.

Rules:
- Break the goal into logical steps.
- Keep the plan concise.
- Put the steps in the correct order.
- Do not complete the task yet.
- Return only the numbered plan.
""".strip()

    return ask_ai(planning_prompt)


def execute_plan(user_goal: str, plan: str) -> str:
    """
    Execute a previously created plan and produce the final result.
    """

    execution_prompt = f"""
You are the execution component of an AI agent.

User goal:
{user_goal}

Execution plan:
{plan}

Complete the user's goal by following the plan.

Rules:
- Follow the steps in the given order.
- Produce a clear and structured result.
- Do not discuss the internal planning process.
- Give practical and useful content.
""".strip()

    return ask_ai(execution_prompt)


def plan_and_execute(user_goal: str) -> str:
    """
    Create a plan and then execute it.
    """

    print("\nCreating a plan...\n")

    plan = create_plan(user_goal)

    print("\n--- Agent Plan ---\n")
    print(plan)

    print("\nExecuting the plan...\n")

    result = execute_plan(user_goal, plan)

    return result