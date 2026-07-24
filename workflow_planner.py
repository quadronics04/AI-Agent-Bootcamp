import json
from typing import Any

from ai_client import ask_ai_internal


ALLOWED_TOOLS = {
    "calculator",
    "gemini",
}


def _build_workflow_prompt(user_request: str) -> str:
    """
    Build the internal prompt used to create a structured workflow.
    """

    return f"""
You are the workflow planner for an AI agent.

Available tools:

calculator
- Performs arithmetic calculations.
- Input should be a valid mathematical expression.

gemini
- Explains, summarizes, writes, reasons, and interprets results.

Create the smallest useful sequence of steps needed to complete
the user's request.

Return only valid JSON in this exact structure:

{{
  "steps": [
    {{
      "tool": "calculator",
      "instruction": "A precise instruction"
    }},
    {{
      "tool": "gemini",
      "instruction": "A precise instruction"
    }}
  ]
}}

Rules:

1. Use only calculator or gemini.
2. Include only necessary steps.
3. Preserve the correct execution order.
4. Do not answer the user's request.
5. Do not include markdown code fences.
6. Return valid JSON only.
7. For a calculation followed by explanation, calculate first.
8. For an explanation followed by calculation, explain first.
9. A workflow may contain only one step.
10. Each instruction must be self-contained.

User request:

{user_request}
""".strip()

def validate_workflow(workflow: object) -> bool:
    """
    Validate the structure and contents of a workflow.
    """

    if not isinstance(workflow, dict):
        return False

    steps = workflow.get("steps")

    if not isinstance(steps, list):
        return False

    if not steps:
        return False

    if len(steps) > 5:
        return False

    for step in steps:
        if not isinstance(step, dict):
            return False

        tool = step.get("tool")
        instruction = step.get("instruction")

        if tool not in ALLOWED_TOOLS:
            return False

        if not isinstance(instruction, str):
            return False

        if not instruction.strip():
            return False

    return True

def _fallback_workflow(user_request: str) -> dict[str, Any]:
    """
    Return a safe default workflow when planning fails.
    """

    return {
        "steps": [
            {
                "tool": "gemini",
                "instruction": user_request,
            }
        ]
    }

def create_workflow(user_request: str) -> dict[str, Any]:
    """
    Generate and validate a structured workflow.
    """

    prompt = _build_workflow_prompt(user_request)

    raw_response = ask_ai_internal(prompt)

    try:
        workflow = json.loads(raw_response)
    except json.JSONDecodeError:
        return _fallback_workflow(user_request)

    if not validate_workflow(workflow):
        return _fallback_workflow(user_request)

    return workflow