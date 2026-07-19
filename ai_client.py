import time

from google import genai
from google.genai.errors import ClientError, ServerError

from config import GEMINI_API_KEY, MODEL_NAME, validate_config
from memory import (
    add_assistant_message,
    add_user_message,
    get_context,
)


# Check configuration before creating the Gemini client
validate_config()

client = genai.Client(api_key=GEMINI_API_KEY)


def _send_request(prompt: str, max_attempts: int = 3) -> str:
    """
    Send a prompt to Gemini.

    This private helper:
    - handles the API request,
    - retries temporary server errors,
    - does not use conversation memory,
    - does not save conversation memory.
    """

    for attempt in range(1, max_attempts + 1):
        try:
            print("\nThinking...\n")

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


def ask_ai(prompt: str, max_attempts: int = 3) -> str:
    """
    Handle normal user-to-assistant conversation.

    This function:
    - reads previous conversation memory,
    - sends the request to Gemini,
    - saves the successful exchange.
    """

    combined_prompt = build_prompt_with_memory(prompt)

    answer = _send_request(
        combined_prompt,
        max_attempts=max_attempts
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
    Handle private agent operations.

    This function:
    - does not read conversation memory,
    - does not save anything to memory,
    - is used by planners, tools, critics, and other internal components.
    """

    return _send_request(
        prompt,
        max_attempts=max_attempts
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