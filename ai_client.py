import time

from google import genai
from google.genai.errors import ClientError, ServerError

from config import GEMINI_API_KEY, MODEL_NAME, validate_config


# Check the API key before creating the client
validate_config()

client = genai.Client(api_key=GEMINI_API_KEY)


def ask_ai(prompt: str, max_attempts: int = 3) -> str:
    """
    Send a prompt to Gemini and return the response text.

    The function retries when Gemini is temporarily unavailable.
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