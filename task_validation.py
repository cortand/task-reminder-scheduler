from datetime import datetime
import uuid


def validate_task(item):
    """
    Validates a task dictionary by checking for a valid title and date.

    :param item: Dictionary of tasks with keys 'title' and 'due',
                    - 'title' must be a non-empty string
                    - 'due' must be an ISO 8601 formatted string representing a date in the future

    :return: Tuple:
                - If valid: (task_dict, None) where task_dict includes ID, title, due date, and reminder flag
                - If invalid: contains (None, error_info) where error_info includes title, due date, and errors list
    """

    # initialize empty errors list
    errors = []

    # validate task title
    title = item.get("title")
    if not isinstance(title, str) or not title.strip():
        # add error message if the title is missing, blank, or not a string
        errors.append("Missing or invalid task title")

    # validate due date
    due_str = item.get("due")
    if not isinstance(due_str, str):
        # add error message if due_str not a string
        errors.append("Due date must be a string in ISO 8601 format")
    else:
        try:
            due = datetime.fromisoformat(due_str)
            # check if due date is in the past
            if due <= datetime.now():
                errors.append("Due date must be in the future.")
        except Exception:
            # raise error for invalid date format
            errors.append("Invalid due date format. Date must be in ISO 8601 format.")

    # run if there are any validation errors
    if errors:
        # return error details containing the original input and list of errors
        return None, {
            "title": title,
            "due": due_str,
            "errors": errors
        }

    # return a valid task dictionary and None to indicate no errors
    return {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "due": due.isoformat(),
        "reminder_sent": False
    }, None
