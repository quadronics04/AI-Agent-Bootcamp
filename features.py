from agent import process_request
from ai_client import ask_ai
from memory import (
    clear_memory,
    show_memory,
)
from metrics import (
    finish_metrics,
    format_metrics_report,
    measure_stage,
    start_metrics,
)
from planner import plan_and_execute
from workflow_agent import process_workflow_request

def _print_execution_report() -> None:
    """
    Finish the active metrics session
    and display the execution report.
    """

    completed_metrics = finish_metrics()

    if completed_metrics is not None:
        print(
            format_metrics_report(
                completed_metrics
            )
        )

def _read_multiline_input(
    instruction: str,
) -> str:
    """
    Read multiline input from the terminal.

    The user types END on a new line to finish.
    """

    print(instruction)
    print("\nType END on a new line to finish.\n")

    lines: list[str] = []

    while True:

        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    return "\n".join(lines).strip()

def _run_ai_feature(
    prompt: str,
    answer_heading: str,
) -> None:
    """
    Execute one AI-powered feature
    with metrics collection.
    """

    start_metrics()

    try:

        with measure_stage("execution"):

            answer = ask_ai(
                prompt,
                show_status=True,
            )

        print(f"\n--- {answer_heading} ---\n")
        print(answer)

    except Exception as error:

        print("\nThe request could not be completed.")
        print(f"Error: {error}")

    finally:

        _print_execution_report()

def summarize_text() -> None:
    """
    Summarize user-provided text.
    """

    text = _read_multiline_input(
        "\nPaste the text you want summarized."
    )

    if not text:
        print("\nText cannot be empty.")
        return

    prompt = f"""
Summarize the following text.

Requirements:
- Preserve all key ideas.
- Remove unnecessary details.
- Keep important names and facts.
- Present the summary in clear paragraphs or bullet points.
- Do not introduce new information.

Text:
{text}
""".strip()

    _run_ai_feature(
        prompt=prompt,
        answer_heading="Summary",
    )

def explain_concept() -> None:
    """
    Explain a concept at the user's preferred level.
    """

    concept = input(
        "\nEnter the concept to explain: "
    ).strip()

    if not concept:
        print("\nConcept cannot be empty.")
        return

    level = input(
        "Choose level (beginner/intermediate/advanced): "
    ).strip().lower()

    if level not in {
        "beginner",
        "intermediate",
        "advanced",
    }:
        level = "beginner"

    prompt = f"""
Explain the following concept for a {level} learner.

Concept:
{concept}

Structure the explanation using:

1. Definition
2. Why it is important
3. How it works
4. Practical example
5. Common mistakes
6. Quick recap

Keep the explanation appropriate for a {level} audience.
""".strip()

    _run_ai_feature(
        prompt=prompt,
        answer_heading="Concept Explanation",
    )

def generate_quiz() -> None:
    """
    Generate a multiple-choice quiz on a selected topic.
    """

    topic = input(
        "\nEnter the quiz topic: "
    ).strip()

    if not topic:
        print("\nTopic cannot be empty.")
        return

    number_input = input(
        "How many questions should be generated? "
        "(default 5): "
    ).strip()

    try:
        number_of_questions = int(number_input)
    except ValueError:
        number_of_questions = 5

    number_of_questions = max(
        1,
        min(number_of_questions, 20),
    )

    difficulty = input(
        "Choose difficulty "
        "(easy/medium/hard): "
    ).strip().lower()

    if difficulty not in {
        "easy",
        "medium",
        "hard",
    }:
        difficulty = "medium"

    prompt = f"""
Create a {difficulty}-difficulty quiz on the following topic:

Topic:
{topic}

Number of questions:
{number_of_questions}

Requirements:

- Use multiple-choice questions.
- Provide four options for each question.
- Include only one correct answer per question.
- Place the answer key after all questions.
- Add a one-sentence explanation for each correct answer.
- Avoid ambiguous or trick questions.
""".strip()

    _run_ai_feature(
        prompt=prompt,
        answer_heading="Quiz",
    )

def create_study_plan() -> None:
    """
    Create a structured and realistic study plan.
    """

    subject = input(
        "\nEnter the subject or skill: "
    ).strip()

    if not subject:
        print("\nSubject cannot be empty.")
        return

    goal = input(
        "What do you want to achieve? "
    ).strip()

    if not goal:
        goal = (
            f"Develop a practical understanding of {subject}"
        )

    duration = input(
        "Enter the available duration "
        "(for example, 7 days or 4 weeks): "
    ).strip()

    if not duration:
        duration = "7 days"

    daily_time = input(
        "How much time can you study each day? "
    ).strip()

    if not daily_time:
        daily_time = "60 minutes"

    current_level = input(
        "Enter your current level "
        "(beginner/intermediate/advanced): "
    ).strip().lower()

    if current_level not in {
        "beginner",
        "intermediate",
        "advanced",
    }:
        current_level = "beginner"

    prompt = f"""
Create a practical study plan using the following details:

Subject or skill:
{subject}

Learning goal:
{goal}

Duration:
{duration}

Daily study time:
{daily_time}

Current level:
{current_level}

The study plan must include:

1. Clear learning objectives
2. A day-by-day or week-by-week schedule
3. Topics arranged in logical sequence
4. Practice activities
5. Revision checkpoints
6. A small project or assessment
7. Progress indicators
8. A final revision and evaluation stage

Keep the workload realistic for the stated daily study time.
""".strip()

    _run_ai_feature(
        prompt=prompt,
        answer_heading="Study Plan",
    )

def ask_general_question() -> None:
    """
    Process a normal user request using
    the simple agent.
    """

    user_input = input(
        "\nEnter your question: "
    ).strip()

    if not user_input:
        print("\nQuestion cannot be empty.")
        return

    start_metrics()

    try:

        answer = process_request(user_input)

        print("\n--- Answer ---\n")
        print(answer)

    except Exception as error:

        print("\nThe request could not be completed.")
        print(f"Error: {error}")

    finally:

        _print_execution_report()

def use_agent_planner() -> None:
    """
    Execute a task using the original
    LLM planner.
    """

    goal = input(
        "\nEnter the goal for the planner: "
    ).strip()

    if not goal:
        print("\nGoal cannot be empty.")
        return

    metrics = start_metrics()
    metrics.planner_used = True

    try:

        with measure_stage("planning"):

            result = plan_and_execute(goal)

        print("\n--- Planner Result ---\n")
        print(result)

    except Exception as error:

        print("\nPlanner execution failed.")
        print(f"Error: {error}")

    finally:

        _print_execution_report()

def planning_assistant() -> None:
    """
    Backward-compatible wrapper around
    use_agent_planner().
    """

    use_agent_planner()

def multi_step_agent() -> None:
    """
    Process a request using the Workflow Agent.

    The Workflow Agent can:
    - generate a workflow
    - execute multiple tools
    - pass outputs between steps
    - synthesize the final answer
    """

    user_request = input(
        "\nEnter a multi-step request: "
    ).strip()

    if not user_request:
        print("\nRequest cannot be empty.")
        return

    start_metrics()

    try:

        answer = process_workflow_request(
            user_request
        )

        print("\n--- Final Answer ---\n")
        print(answer)

    except Exception as error:

        print("\nWorkflow execution failed.")
        print(f"Error: {error}")

    finally:

        _print_execution_report()

def display_memory() -> None:
    """
    Display the stored conversation memory.
    """

    print("\n========== Conversation Memory ==========\n")

    try:

        show_memory()

    except Exception as error:

        print("Unable to display memory.")
        print(f"Error: {error}")

def erase_memory() -> None:
    """
    Clear the stored conversation memory
    after user confirmation.
    """

    confirmation = input(
        "\nDelete all conversation memory? (yes/no): "
    ).strip().lower()

    if confirmation not in {"yes", "y"}:
        print("\nMemory was not cleared.")
        return

    try:

        clear_memory()

        print("\nConversation memory cleared successfully.")

    except Exception as error:

        print("\nUnable to clear memory.")
        print(f"Error: {error}")