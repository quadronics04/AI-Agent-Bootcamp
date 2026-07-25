from ai_client import is_error_response
from memory import add_assistant_message, add_user_message
from metrics import get_metrics, measure_stage
from utils import print_status
from workflow_executor import execute_workflow
from workflow_planner import create_workflow


def process_workflow_request(
    user_request: str,
) -> str:
    """
    Plan and execute a multi-step workflow.

    Only the original user request and final answer are
    stored in conversation memory.
    """

    metrics = get_metrics()

    if metrics is not None:
        metrics.planner_used = True

    print_status("Creating a workflow...")

    with measure_stage("planning"):
        workflow = create_workflow(user_request)

    print_status("Executing the workflow...")

    with measure_stage("execution"):
        final_answer = execute_workflow(
            user_request=user_request,
            workflow=workflow,
        )

    if not is_error_response(final_answer):

        with measure_stage("memory"):
            add_user_message(user_request)
            add_assistant_message(final_answer)

        if metrics is not None:
            metrics.memory_updated = True

    return final_answer