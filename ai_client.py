import time

from google import genai
from google.genai.errors import ClientError, ServerError

from config import GEMINI_API_KEY, MODEL_NAME, validate_config
from memory import (
    add_assistant_message,
    add_user_message,
    get_context,
)


validate_config()

client = genai.Client(api_key=GEMINI_API_KEY)


def _send_request(
    prompt: str,
    max_attempts: int = 3,
    show_status: bool = False,
    status_message: str = "Thinking..."
) -> str:
    """
    Send a prompt to Gemini.

    This helper:
    - handles retries,
    - optionally displays a status message,
    - does not directly manage conversation memory.
    """

    if show_status:
        print(f"\n{status_message}\n")

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if response.text:
                return response.text.strip()

            return "The AI returned an empty response."

        except ServerError:
            if attempt == max_attempts:
                return (
                    "Gemini is currently busy or unavailable. "
                    "Please try again later."
                )

            wait_time = 2 ** (attempt - 1)

            print(
                f"Gemini is busy. Retrying in "
                f"{wait_time} second(s)..."
            )

            time.sleep(wait_time)

        except ClientError as error:
            return f"Gemini request failed:\n{error}"

        except Exception as error:
            return f"Unexpected error:\n{error}"

    return "The request could not be completed."


def build_prompt_with_memory(prompt: str) -> str:
    """
    Combine the current user prompt with previous conversation memory.
    """

    previous_context = get_context()

    if not previous_context:
        return prompt

    return f"""
Previous conversation:

{previous_context}

Current user request:

{prompt}

Instructions:
- Answer the current request directly.
- Use previous conversation only when relevant.
- Do not mention the memory system.
- Do not repeat previous answers unnecessarily.
""".strip()


def ask_ai(
    prompt: str,
    max_attempts: int = 3,
    show_status: bool = True,
    status_message: str = "Thinking..."
) -> str:
    """
    Handle normal user conversation with memory.
    """

    combined_prompt = build_prompt_with_memory(prompt)

    answer = _send_request(
        combined_prompt,
        max_attempts=max_attempts,
        show_status=show_status,
        status_message=status_message
    )

    if not is_error_response(answer):
        add_user_message(prompt)
        add_assistant_message(answer)

    return answer


def ask_ai_internal(
    prompt: str,
    max_attempts: int = 3
) -> str:
    """
    Handle private agent operations silently.
    """

    return _send_request(
        prompt,
        max_attempts=max_attempts,
        show_status=False
    )


def is_error_response(response: str) -> bool:
    """
    Check whether the returned text represents an API failure.
    """

    error_starts = (
        "Gemini is currently busy",
        "Gemini request failed",
        "Unexpected error",
        "The request could not be completed",
        "The AI returned an empty response",
    )

    return response.startswith(error_starts)