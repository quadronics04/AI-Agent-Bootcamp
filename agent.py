from ai_client import ask_ai
from calculator import calculate
from tool_selector import choose_tool


def process_request(user_input: str) -> str:
    """
    Select and execute the correct tool for a user request.
    """

    selected_tool = choose_tool(user_input)

    if selected_tool == "calculator":
        return calculate(user_input)

    return ask_ai(user_input)