from memory import (
    add_assistant_message,
    add_user_message,
    clear_memory,
    get_context,
)


add_user_message(
    "My name is Shivansh."
)

add_assistant_message(
    "Nice to meet you, Shivansh."
)

add_user_message(
    "I am preparing for an AI agent competition."
)

print(get_context())