def print_heading(title: str) -> None:
    """Print a formatted heading."""

    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)


def read_multiline_input(
    instruction: str,
    end_marker: str = "END"
) -> str:
    """
    Read multiple lines from the user.

    Input stops when the user enters the selected end marker.
    """

    print(f"\n{instruction}")
    print(f"Type {end_marker} on a new line when finished.\n")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == end_marker.upper():
            break

        lines.append(line)

    return "\n".join(lines).strip()


def get_positive_integer(message: str) -> int | None:
    """Read and validate a positive integer."""

    value = input(message).strip()

    try:
        number = int(value)

        if number <= 0:
            print("Please enter a number greater than zero.")
            return None

        return number

    except ValueError:
        print("Please enter a valid whole number.")
        return None


def get_positive_number(message: str) -> float | None:
    """Read and validate a positive decimal or whole number."""

    value = input(message).strip()

    try:
        number = float(value)

        if number <= 0:
            print("Please enter a number greater than zero.")
            return None

        return number

    except ValueError:
        print("Please enter a valid number.")
        return None