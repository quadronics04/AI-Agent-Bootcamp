from ai_client import ask_ai
from prompts import (
    create_code_explanation_prompt,
    create_concept_prompt,
    create_general_question_prompt,
    create_quiz_prompt,
    create_study_plan_prompt,
    create_summary_prompt,
)
from utils import (
    get_positive_integer,
    get_positive_number,
    print_heading,
    read_multiline_input,
)
from planner import plan_and_execute
from agent import process_request
from workflow_agent import process_workflow_request

def explain_concept() -> None:
    """Ask the AI to explain a concept."""

    print_heading("EXPLAIN A CONCEPT")

    topic = input("\nEnter the concept: ").strip()

    if not topic:
        print("The topic cannot be empty.")
        return

    prompt = create_concept_prompt(topic)
    answer = ask_ai(prompt)

    print_heading("AI EXPLANATION")
    print(answer)


def summarize_text() -> None:
    """Ask the AI to summarise user-provided text."""

    print_heading("SUMMARISE TEXT")

    text = read_multiline_input(
        instruction="Paste the text you want to summarise."
    )

    if not text:
        print("No text was entered.")
        return

    prompt = create_summary_prompt(text)
    answer = ask_ai(prompt)

    print_heading("SUMMARY")
    print(answer)


def generate_quiz() -> None:
    """Ask the AI to generate a quiz."""

    print_heading("GENERATE A QUIZ")

    topic = input("\nEnter the quiz topic: ").strip()

    if not topic:
        print("The topic cannot be empty.")
        return

    prompt = create_quiz_prompt(topic)
    answer = ask_ai(prompt)

    print_heading("GENERATED QUIZ")
    print(answer)


def explain_python_code() -> None:
    """Ask the AI to explain Python code."""

    print_heading("EXPLAIN PYTHON CODE")

    code = read_multiline_input(
        instruction="Paste the Python code."
    )

    if not code:
        print("No Python code was entered.")
        return

    prompt = create_code_explanation_prompt(code)
    answer = ask_ai(prompt)

    print_heading("CODE EXPLANATION")
    print(answer)


def ask_general_question() -> None:
    """
    Ask a general question or process a supported tool request.
    """

    print("\n--- Ask a General Question ---")

    user_input = input(
        "\nEnter your question:\n"
    ).strip()

    if not user_input:
        print("\nQuestion cannot be empty.")
        return

    response = process_request(user_input)

    print("\n--- Response ---\n")
    print(response)


def create_study_plan() -> None:
    """Ask the AI to create a personalised study plan."""

    print_heading("CREATE A STUDY PLAN")

    subject = input("\nEnter the subject: ").strip()

    if not subject:
        print("The subject cannot be empty.")
        return

    days = get_positive_integer(
        "Enter the number of days available: "
    )

    if days is None:
        return

    hours_per_day = get_positive_number(
        "Enter the number of study hours per day: "
    )

    if hours_per_day is None:
        return

    prompt = create_study_plan_prompt(
        subject=subject,
        days=days,
        hours_per_day=hours_per_day
    )

    answer = ask_ai(prompt)

    print_heading("YOUR STUDY PLAN")
    print(answer)

def use_agent_planner() -> None:
    """
    Ask the planner to break down and complete a complex goal.
    """

    print("\n--- AI Agent Planner ---")

    user_goal = input(
        "\nDescribe the goal you want the agent to complete:\n"
    ).strip()

    if not user_goal:
        print("\nThe goal cannot be empty.")
        return

    result = plan_and_execute(user_goal)

    print("\n--- Final Result ---\n")
    print(result)

def multi_step_agent() -> None:
    """
    Run the multi-step workflow agent.
    """

    user_request = input(
        "\nEnter a multi-step request: "
    ).strip()

    if not user_request:
        print("\nRequest cannot be empty.")
        return

    answer = process_workflow_request(user_request)

    print("\n--- Final Answer ---\n")
    print(answer)