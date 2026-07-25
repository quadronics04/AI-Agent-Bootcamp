from ai_client import ask_ai
from calculator import calculate
from math_parser import extract_math_expression
from tool_selector import (
    choose_tool,
    is_direct_math_expression,
)
from utils import print_status
from metrics import get_metrics, measure_stage

TOOL_STATUS_MESSAGES = {
    "calculator": "Using the calculator...",
    "gemini": "Generating a response...",
}

def process_request(user_input: str) -> str:
    """
    Select and execute the appropriate tool.
    """

    print_status("Understanding your request...")

    with measure_stage("classification"):
        selected_tool = choose_tool(user_input)

    metrics = get_metrics()

    if metrics is not None:
        metrics.record_tool(selected_tool)

    status_message = TOOL_STATUS_MESSAGES.get(
        selected_tool,
        "Processing your request...",
    )

    print_status(status_message)

    with measure_stage("execution"):

        if selected_tool == "calculator":

            if is_direct_math_expression(user_input):
                expression = user_input

            else:
                expression = extract_math_expression(
                    user_input
                )

            result = calculate(expression)

            return (
                f"Expression: {expression}\n"
                f"Result: {result}"
            )

        return ask_ai(
            user_input,
            show_status=False,
        )