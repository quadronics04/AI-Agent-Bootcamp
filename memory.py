import json
from pathlib import Path
from typing import Any


# Path of the JSON memory file
MEMORY_FILE = Path(__file__).parent / "memory_conversation.json"

# Maximum number of stored messages
MAX_MESSAGES = 20


def create_empty_memory() -> dict[str, Any]:
    """
    Return the default structure used by the memory system.
    """

    return {
        "version": "1.0",
        "messages": []
    }


def load_memory() -> dict[str, Any]:
    """
    Load conversation memory from the JSON file.

    If the file is missing, empty, damaged, or has an invalid structure,
    a new empty memory structure is returned.
    """

    if not MEMORY_FILE.exists():
        empty_memory = create_empty_memory()
        save_memory(empty_memory)
        return empty_memory

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            memory = json.load(file)

    except json.JSONDecodeError:
        print(
            "Memory file is empty or contains invalid JSON. "
            "Starting with empty memory."
        )

        empty_memory = create_empty_memory()
        save_memory(empty_memory)
        return empty_memory

    except OSError as error:
        print(f"Could not read memory file: {error}")
        return create_empty_memory()

    if not isinstance(memory, dict):
        print("Memory file has an invalid structure.")
        return create_empty_memory()

    if "messages" not in memory or not isinstance(
        memory["messages"], list
    ):
        memory["messages"] = []

    if "version" not in memory:
        memory["version"] = "1.0"

    return memory


def save_memory(memory: dict[str, Any]) -> bool:
    """
    Save memory to the JSON file.

    Returns True if saving succeeds and False if it fails.
    """

    try:
        with MEMORY_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError as error:
        print(f"Could not save memory: {error}")
        return False


# Load memory once when this module is imported
memory_data = load_memory()


def add_message(role: str, content: str) -> None:
    """
    Add one message to conversation memory.

    Allowed roles:
    - user
    - assistant
    """

    role = role.strip().lower()
    content = content.strip()

    if role not in {"user", "assistant"}:
        raise ValueError(
            "Role must be either 'user' or 'assistant'."
        )

    if not content:
        return

    message = {
        "role": role,
        "content": content
    }

    memory_data["messages"].append(message)

    # Keep only the most recent messages
    if len(memory_data["messages"]) > MAX_MESSAGES:
        memory_data["messages"] = memory_data["messages"][
            -MAX_MESSAGES:
        ]

    save_memory(memory_data)


def add_user_message(content: str) -> None:
    """
    Store a user message.
    """

    add_message("user", content)


def add_assistant_message(content: str) -> None:
    """
    Store an assistant message.
    """

    add_message("assistant", content)


def get_messages() -> list[dict[str, str]]:
    """
    Return a copy of all stored messages.
    """

    return memory_data["messages"].copy()


def get_context() -> str:
    """
    Convert stored messages into readable conversation context.
    """

    messages = memory_data["messages"]

    if not messages:
        return ""

    formatted_messages = []

    for message in messages:
        role = message["role"].capitalize()
        content = message["content"]

        formatted_messages.append(
            f"{role}: {content}"
        )

    return "\n\n".join(formatted_messages)

def clear_memory() -> None:
    """
    Remove all stored conversation messages.
    """

    memory_data["messages"].clear()

    if save_memory(memory_data):
        print("Conversation memory cleared successfully.")


def show_memory() -> None:
    """
    Display the current stored conversation.
    """

    print("\n--- Conversation Memory ---\n")
    print(get_context())