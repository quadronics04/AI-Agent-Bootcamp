from ai_client import ask_ai
from calculator import calculate
from math_parser import extract_math_expression
from tool_selector import (
    choose_tool,
    is_direct_math_expression,
)


def process_request(user_input: str) -> str:
    """
    Select and execute the correct tool for a user request.
    """

    selected_tool = choose_tool(user_input)

    if selected_tool == "calculator":
        if is_direct_math_expression(user_input):
            expression = user_input
        else:
            expression = extract_math_expression(user_input)

        result = calculate(expression)

        return (
            f"Expression: {expression}\n"
            f"Result: {result}"
        )

    return ask_ai(user_input)