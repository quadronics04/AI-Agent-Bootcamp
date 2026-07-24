from ai_client import ask_ai_internal


ALLOWED_TOOLS = {
    "calculator",
    "gemini",
}


def classify_tool(user_input: str) -> str:
    """
    Use Gemini internally to decide which tool should handle
    the user's request.
    """

    classifier_prompt = f"""
You are the tool-routing component of an AI agent.

Available tools:

calculator
- Use for arithmetic, percentages, interest, averages,
  ratios, conversions, and other numerical calculations.

gemini
- Use for explanations, writing, advice, reasoning,
  general knowledge, and requests that are not primarily
  calculations.

User request:
{user_input}

Return exactly one tool name:

calculator

or

gemini

Do not answer the user's request.
Do not explain your decision.
""".strip()

    result = ask_ai_internal(classifier_prompt)

    selected_tool = result.strip().lower()

    if selected_tool in ALLOWED_TOOLS:
        return selected_tool

    # Safe fallback
    return "gemini"