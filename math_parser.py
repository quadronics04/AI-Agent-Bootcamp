from ai_client import ask_ai_internal


def extract_math_expression(user_input: str) -> str:
    """
    Convert a natural-language calculation request into a
    Python-compatible mathematical expression.
    """

    extraction_prompt = f"""
Convert the following calculation request into one valid
Python arithmetic expression.

User request:
{user_input}

Rules:
- Return only the expression.
- Do not calculate the answer.
- Do not include explanations.
- Use * for multiplication.
- Use / for division.
- Use ** for powers.
- Convert percentages into decimal arithmetic when needed.

Examples:

What is 25 multiplied by 8?
25 * 8

Calculate 18 percent of 4500.
4500 * 18 / 100

Add 15 and 20, then divide by 5.
(15 + 20) / 5

User request:
{user_input}
""".strip()

    return ask_ai_internal(extraction_prompt).strip()