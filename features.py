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
    """Ask the AI a general question."""

    print_heading("GENERAL QUESTION")

    question = input("\nEnter your question: ").strip()

    if not question:
        print("The question cannot be empty.")
        return

    prompt = create_general_question_prompt(question)
    answer = ask_ai(prompt)

    print_heading("AI RESPONSE")
    print(answer)


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