import re

from ai_client import ask_ai

from tools import calculator

def process_request(user_input):

    """
    Decide which tool should answer.
    """

    pattern = r"^[0-9+\-*/(). ]+$"

    if re.fullmatch(pattern, user_input):

        answer = calculator(user_input)

        return f"Calculator Answer:\n{answer}"

    else:

        return ask_ai(user_input)