import re

from tool_classifier import classify_tool


MATH_PATTERN = re.compile(
    r"^[\d\s\+\-\*\/\%\(\)\.]+$"
)


def is_direct_math_expression(user_input: str) -> bool:
    """
    Return True when the input already looks like a mathematical
    expression.
    """

    return bool(
        MATH_PATTERN.fullmatch(user_input.strip())
    )


def choose_tool(user_input: str) -> str:
    """
    Select the appropriate tool using a hybrid approach.
    """

    cleaned_input = user_input.strip()

    if not cleaned_input:
        return "gemini"

    if is_direct_math_expression(cleaned_input):
        return "calculator"

    return classify_tool(cleaned_input)