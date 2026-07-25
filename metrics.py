from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from time import perf_counter

@dataclass
class ExecutionMetrics:
    """
    Stores performance information for one agent request.

    NOTE:
    This implementation assumes a synchronous, single-user CLI.

    For concurrent environments (FastAPI, async workers, etc.),
    replace the module-level metrics state with ContextVar.
    """

    request_start_time: float = field(default_factory=perf_counter)
    request_end_time: float | None = None

    planning_time: float = 0.0
    classification_time: float = 0.0
    execution_time: float = 0.0
    memory_time: float = 0.0

    llm_calls: int = 0
    retries: int = 0
    cache_hits: int = 0

    planner_used: bool = False
    memory_updated: bool = False

    tools_used: Counter[str] = field(default_factory=Counter)

    def record_llm_call(self) -> None:
        """Record one LLM API request."""
        self.llm_calls += 1

    def record_retry(self) -> None:
        """Record one retry."""
        self.retries += 1

    def record_cache_hit(self) -> None:
        """Record one cache hit."""
        self.cache_hits += 1

    def record_tool(self, tool_name: str) -> None:
        """Record execution of one tool."""

        tool_name = tool_name.strip().lower()

        if tool_name:
            self.tools_used[tool_name] += 1

    def add_stage_time(
        self,
        stage_name: str,
        duration: float,
    ) -> None:
        """
        Add elapsed time to one execution stage.
        """

        if duration < 0:
            return

        stage_name = stage_name.lower()

        if stage_name == "planning":
            self.planning_time += duration

        elif stage_name == "classification":
            self.classification_time += duration

        elif stage_name == "execution":
            self.execution_time += duration

        elif stage_name == "memory":
            self.memory_time += duration

    def finish(self) -> None:
        """Mark request completion."""

        if self.request_end_time is None:
            self.request_end_time = perf_counter()

    @property
    def total_time(self) -> float:
        """
        Total request duration.
        """

        end_time = (
            self.request_end_time
            if self.request_end_time is not None
            else perf_counter()
        )

        return end_time - self.request_start_time

    @property
    def measured_stage_time(self) -> float:
        """
        Time accounted for by measured stages.
        """

        return (
            self.planning_time
            + self.classification_time
            + self.execution_time
            + self.memory_time
        )

    @property
    def other_time(self) -> float:
        """
        Time not attributed to a measured stage.
        """

        return max(
            0.0,
            self.total_time - self.measured_stage_time,
        )

# Active metrics object for the current CLI request.
_current_metrics: ExecutionMetrics | None = None

def start_metrics() -> ExecutionMetrics:
    """
    Start metrics collection for a new request.

    Any previously active metrics object is replaced.
    """

    global _current_metrics

    _current_metrics = ExecutionMetrics()

    return _current_metrics

def get_metrics() -> ExecutionMetrics | None:
    """
    Return the active metrics object.

    Returns None when metrics collection has not been started.
    """

    return _current_metrics

def finish_metrics() -> ExecutionMetrics | None:
    """
    Finish and return the active metrics object.

    The active metrics reference is cleared after completion.
    """

    global _current_metrics

    if _current_metrics is None:
        return None

    _current_metrics.finish()

    completed_metrics = _current_metrics
    _current_metrics = None

    return completed_metrics

@contextmanager
def measure_stage(stage_name: str) -> Iterator[None]:
    """
    Measure the duration of one processing stage.

    Supported stage names:
    - planning
    - classification
    - execution
    - memory

    Example:

        with measure_stage("planning"):
            workflow = create_workflow(user_request)
    """

    start_time = perf_counter()

    try:
        yield

    finally:
        elapsed_time = perf_counter() - start_time
        metrics = get_metrics()

        if metrics is not None:
            metrics.add_stage_time(
                stage_name=stage_name,
                duration=elapsed_time,
            )

def _format_tools(
    tools_used: Counter[str],
) -> str:
    """
    Format tool usage counts for terminal display.

    Example output:
    calculator ×1 → gemini ×2
    """

    if not tools_used:
        return "None"

    entries = [
        f"{tool_name} ×{count}"
        for tool_name, count in tools_used.items()
    ]

    return " → ".join(entries)

def format_metrics_report(
    metrics: ExecutionMetrics,
) -> str:
    """
    Create a readable execution report for terminal output.
    """

    tools = _format_tools(metrics.tools_used)

    planner_used = (
        "Yes"
        if metrics.planner_used
        else "No"
    )

    memory_updated = (
        "Yes"
        if metrics.memory_updated
        else "No"
    )

    return (
        "\n"
        "========================================\n"
        "Agent Execution Report\n"
        "========================================\n"
        f"Planning Time       : "
        f"{metrics.planning_time:.4f} seconds\n"
        f"Classification Time : "
        f"{metrics.classification_time:.4f} seconds\n"
        f"Execution Time      : "
        f"{metrics.execution_time:.4f} seconds\n"
        f"Memory Time         : "
        f"{metrics.memory_time:.4f} seconds\n"
        f"Other Time          : "
        f"{metrics.other_time:.4f} seconds\n"
        f"Total Time          : "
        f"{metrics.total_time:.4f} seconds\n"
        "----------------------------------------\n"
        f"LLM Calls           : {metrics.llm_calls}\n"
        f"Retries             : {metrics.retries}\n"
        f"Cache Hits          : {metrics.cache_hits}\n"
        f"Planner Used        : {planner_used}\n"
        f"Tools Used          : {tools}\n"
        f"Memory Updated      : {memory_updated}\n"
        "========================================"
    )