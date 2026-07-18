from config import APP_NAME
from features import (
    ask_general_question,
    create_study_plan,
    explain_concept,
    explain_python_code,
    generate_quiz,
    summarize_text,
    use_agent_planner,
)
from memory import clear_memory, show_memory
from utils import print_heading


def show_menu() -> None:
    """Display the main application menu."""

    print_heading(APP_NAME)

    print("1. Explain a concept")
    print("2. Summarise text")
    print("3. Generate a quiz")
    print("4. Explain Python code")
    print("5. Ask a general question")
    print("6. Create a study plan")
    print("7. Use AI agent planner")
    print("8. Show conversation memory")
    print("9. Clear conversation memory")
    print("10. Exit")


def main() -> None:
    """Run the main application loop."""

    while True:
        show_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            explain_concept()

        elif choice == "2":
            summarize_text()

        elif choice == "3":
            generate_quiz()

        elif choice == "4":
            explain_python_code()

        elif choice == "5":
            ask_general_question()

        elif choice == "6":
            create_study_plan()

        elif choice == "7":
            use_agent_planner()

        elif choice == "8":
            show_memory()

        elif choice == "9":
            confirm = input(
                "\nAre you sure you want to clear memory? "
                "(yes/no): "
            ).strip().lower()

            if confirm == "yes":
                clear_memory()
            else:
                print("\nMemory was not cleared.")

        elif choice == "10":
            print("\nThank you for using Study AI Assistant.")
            break

        else:
            print(
                "\nInvalid choice. "
                "Enter a number from 1 to 10."
            )


if __name__ == "__main__":
    main()