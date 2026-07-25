import csv
from pathlib import Path
from time import perf_counter

from agent import process_request
from metrics import (
    finish_metrics,
    start_metrics,
)

DEFAULT_INPUT_PATH = Path("input/requests.csv")
DEFAULT_OUTPUT_PATH = Path("output/results.csv")

def ensure_parent_directory(
    file_path: Path,
) -> None:
    """
    Create the parent directory of a file
    when it does not already exist.
    """

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

def read_input_rows(
    input_path: Path,
) -> list[dict[str, str]]:
    """
    Read request rows from a CSV file.

    Required columns:
    - request_id
    - user_request

    Returns:
        A list of validated CSV rows.

    Raises:
        FileNotFoundError:
            When the input CSV does not exist.

        ValueError:
            When required columns are missing
            or when the file contains no valid rows.
    """

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    with input_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError(
                "The input CSV does not contain a header row."
            )

        required_columns = {
            "request_id",
            "user_request",
        }

        available_columns = {
            column.strip()
            for column in reader.fieldnames
            if column is not None
        }

        missing_columns = (
            required_columns - available_columns
        )

        if missing_columns:
            missing_text = ", ".join(
                sorted(missing_columns)
            )

            raise ValueError(
                "The input CSV is missing required "
                f"column(s): {missing_text}"
            )

        rows: list[dict[str, str]] = []

        for row_number, row in enumerate(
            reader,
            start=2,
        ):
            request_id = (
                row.get("request_id") or ""
            ).strip()

            user_request = (
                row.get("user_request") or ""
            ).strip()

            if not request_id and not user_request:
                continue

            if not request_id:
                request_id = (
                    f"ROW_{row_number:04d}"
                )

            rows.append(
                {
                    "request_id": request_id,
                    "user_request": user_request,
                }
            )

    if not rows:
        raise ValueError(
            "The input CSV does not contain any valid rows."
        )

    return rows

def process_batch_row(
    row: dict[str, str],
) -> dict[str, str]:
    """
    Process one CSV request independently.

    Each row receives:
    - execution status
    - response or error
    - total latency
    - LLM call count
    - retry count
    - tool usage
    """

    request_id = row["request_id"]
    user_request = row["user_request"]

    if not user_request:
        return {
            "request_id": request_id,
            "user_request": user_request,
            "status": "error",
            "response": "",
            "error": "User request is empty.",
            "latency_seconds": "0.0000",
            "llm_calls": "0",
            "retries": "0",
            "tools_used": "",
        }

    start_metrics()
    row_start_time = perf_counter()

    try:
        response = process_request(
            user_request
        )

        status = "success"
        error_message = ""

    except Exception as error:
        response = ""
        status = "error"
        error_message = str(error)

    finally:
        elapsed_time = (
            perf_counter() - row_start_time
        )

        completed_metrics = finish_metrics()

    if completed_metrics is None:
        llm_calls = 0
        retries = 0
        tools_used = ""

    else:
        llm_calls = completed_metrics.llm_calls
        retries = completed_metrics.retries

        tools_used = ", ".join(
            f"{tool_name}:{count}"
            for tool_name, count
            in completed_metrics.tools_used.items()
        )

    return {
        "request_id": request_id,
        "user_request": user_request,
        "status": status,
        "response": str(response),
        "error": error_message,
        "latency_seconds": f"{elapsed_time:.4f}",
        "llm_calls": str(llm_calls),
        "retries": str(retries),
        "tools_used": tools_used,
    }

def write_output_rows(
    output_path: Path,
    rows: list[dict[str, str]],
) -> None:
    """
    Write processed results to an output CSV file.
    """

    ensure_parent_directory(output_path)

    fieldnames = [
        "request_id",
        "user_request",
        "status",
        "response",
        "error",
        "latency_seconds",
        "llm_calls",
        "retries",
        "tools_used",
    ]

    with output_path.open(
        mode="w",
        encoding="utf-8",
        newline="",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()

        writer.writerows(rows)

def print_batch_summary(
    results: list[dict[str, str]],
) -> None:
    """
    Display a summary of the completed batch.
    """

    total = len(results)

    successful = sum(
        1
        for row in results
        if row["status"] == "success"
    )

    failed = total - successful

    print("\n===================================")
    print("Batch Processing Summary")
    print("===================================")

    print(f"Total Requests : {total}")
    print(f"Successful     : {successful}")
    print(f"Failed         : {failed}")

    print("===================================\n")

def process_csv_batch(
    input_path: Path = DEFAULT_INPUT_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> None:
    """
    Process every request in an input CSV file.

    Workflow:
        1. Read input CSV
        2. Process each request
        3. Save output CSV
        4. Print processing summary
    """

    print("\n========== Batch Processing ==========\n")

    rows = read_input_rows(input_path)

    results: list[dict[str, str]] = []

    total_requests = len(rows)

    for index, row in enumerate(rows, start=1):

        print(
            f"[{index}/{total_requests}] "
            f"Processing {row['request_id']}..."
        )

        result = process_batch_row(row)

        results.append(result)

    write_output_rows(
        output_path=output_path,
        rows=results,
    )

    print_batch_summary(results)

    print(
        f"Results saved to:\n{output_path.resolve()}"
    )