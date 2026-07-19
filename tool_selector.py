import re


MATH_PATTERN = re.compile(
    r"^[\d\s\+\-\*\/\%\(\)\.]+$"
)


def choose_tool(user_input: str) -> str:
    """
    Decide which tool should handle the request.

    Returns:
    - calculator
    - gemini
    """

    cleaned_input = user_input.strip()

    if not cleaned_input:
        return "gemini"

    if MATH_PATTERN.fullmatch(cleaned_input):
        return "calculator"

    return "gemini"