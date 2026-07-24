from config import APP_NAME
from features import (
    ask_general_question,
    create_study_plan,
    explain_concept,
    explain_python_code,
    generate_quiz,
    summarize_text,
    use_agent_planner,
    multi_step_agent
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
    print("6. Multi-Step Workflow Agent")
    print("7. Create a study plan")
    print("8. Use AI agent planner")
    print("9. Show conversation memory")
    print("10. Clear conversation memory")
    print("11. Exit")


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
            multi_step_agent()

        elif choice == "7":
            create_study_plan()

        elif choice == "8":
            use_agent_planner()

        elif choice == "9":
            show_memory()

        elif choice == "10":
            confirm = input(
                "\nAre you sure you want to clear memory? "
                "(yes/no): "
            ).strip().lower()

            if confirm == "yes":
                clear_memory()
            else:
                print("\nMemory was not cleared.")

        elif choice == "11":
            print("\nThank you for using Study AI Assistant.")
            break

        else:
            print(
                "\nInvalid choice. "
                "Enter a number from 1 to 10."
            )


if __name__ == "__main__":
    main()