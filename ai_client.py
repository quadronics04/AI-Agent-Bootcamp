import time

from google import genai
from google.genai.errors import ClientError, ServerError

from config import GEMINI_API_KEY, MODEL_NAME, validate_config
from memory import (
    add_assistant_message,
    add_user_message,
    get_context,
)


# Check the API key before creating the client
validate_config()

client = genai.Client(api_key=GEMINI_API_KEY)


def build_prompt_with_memory(prompt: str) -> str:
    """
    Combine the current prompt with previous conversation context.
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
- Respond mainly to the current user request.
- Use previous conversation only when it is relevant.
- Do not mention the memory system.
- Do not repeat old answers unnecessarily.
""".strip()


def ask_ai(prompt: str, max_attempts: int = 3) -> str:
    """
    Send a prompt to Gemini and return the response text.

    The function:
    - includes relevant conversation memory,
    - retries when Gemini is temporarily unavailable,
    - stores successful user and assistant messages.
    """

    combined_prompt = build_prompt_with_memory(prompt)

    for attempt in range(1, max_attempts + 1):
        try:
            print("\nThinking...\n")

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=combined_prompt
            )

            if not response.text:
                return "The AI returned an empty response."

            answer = response.text.strip()

            # Save only a successful conversation
            add_user_message(prompt)
            add_assistant_message(answer)

            return answer

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