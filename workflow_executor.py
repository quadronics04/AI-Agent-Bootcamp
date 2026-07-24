from typing import Any

from ai_client import ask_ai_internal
from calculator import calculate
from math_parser import extract_math_expression

def execute_step(
    tool: str,
    instruction: str,
    user_request: str,
    previous_outputs: list[str],
) -> str:
    """
    Execute one workflow step.
    """

    context = _format_previous_outputs(previous_outputs)

    if tool == "calculator":
        return _execute_calculator_step(
            instruction=instruction,
            context=context,
        )

    if tool == "gemini":
        return _execute_gemini_step(
            instruction=instruction,
            user_request=user_request,
            context=context,
        )

    return f"Unsupported tool: {tool}"

def _execute_calculator_step(
    instruction: str,
    context: str,
) -> str:
    """
    Convert the instruction into an expression and calculate it.
    """

    parser_input = instruction

    if context:
        parser_input += f"\n\nPrevious step outputs:\n{context}"

    expression = extract_math_expression(parser_input)

    result = calculate(expression)

    return (
        f"Expression: {expression}\n"
        f"Result: {result}"
    )

def _execute_gemini_step(
    instruction: str,
    user_request: str,
    context: str,
) -> str:
    """
    Execute an internal Gemini workflow step.
    """

    prompt = f"""
You are executing one step inside an AI workflow.

Original user request:

{user_request}

Current instruction:

{instruction}
""".strip()

    if context:
        prompt += f"""

Previous step outputs:

{context}
"""

    prompt += """

Complete only the current instruction.

Use previous outputs when relevant.
Do not discuss the internal workflow.
Return a clear user-facing response.
"""

    return ask_ai_internal(prompt)

def _format_previous_outputs(
    previous_outputs: list[str],
) -> str:
    """
    Combine previous workflow outputs into one context block.
    """

    if not previous_outputs:
        return ""

    return "\n\n".join(previous_outputs)

def execute_workflow(
    user_request: str,
    workflow: dict[str, Any],
) -> str:
    """
    Execute workflow steps sequentially.

    The output of each completed step becomes available
    to later steps.
    """

    previous_outputs: list[str] = []

    for step_number, step in enumerate(
        workflow["steps"],
        start=1,
    ):
        tool = step["tool"]
        instruction = step["instruction"]

        result = execute_step(
            tool=tool,
            instruction=instruction,
            user_request=user_request,
            previous_outputs=previous_outputs,
        )

        previous_outputs.append(
            f"Step {step_number} output:\n{result}"
        )

    return previous_outputs[-1]

