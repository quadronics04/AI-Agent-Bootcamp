import os

from dotenv import load_dotenv


# Load variables from the .env file
load_dotenv()

APP_NAME = "STUDY AI ASSISTANT"

MODEL_NAME = "gemini-3.1-flash-lite-preview"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def validate_config() -> None:
    """Check whether all required configuration values are available."""

    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY was not found.\n"
            "Check that your .env file exists and contains:\n"
            "GEMINI_API_KEY=your_api_key"
        )