# Task Reminder Scheduler Microservices

A Python microservice that receives tasks with due dates over ZeroMQ,
validates them, stores them, and sends reminders at a desired interval before each task is due.

## Features
- Accepts task list in JSON format
- Validates each task's title and due date
- Sends reminders 1 hour before due time (configurable to desired lead time)
- Stores valid tasks in JSON file

## Running the Microservice
Start the microservice:
```bash
python main_service.py
```

## Sending tasks
Use the included 'test_client.py':
```bash
python test_client.py
```

Or use your own ZeroMQ REQ client to send tasks in this required format:
```json
[
  {
    "title": "Submit assignment",
    "due": "2025-08-04T15:00:00"
  }
]
```

## Reminder Behavior
- A reminder is triggerred at 1 hour before the due time (lead time is configurable in reminder_loop.py)
- The reminder is printed in the console and sent over PUB socket as JSON.

Example output:
```json
[Reminder]: 'Submit assignment' is due in 1 hour.
```

## Validation Rules
- 'title' - Must be a non-empty string
- 'due' - Must be an ISO 8601 formatted string representing a date in the future

If a task fails validation, an error summary will be printed.

## Response Format
```json
{
  "status": "partial_success",
  "added": 1,
  "rejected": [
    {
      "title": "",
      "due": "invalid-date",
      "errors": [
        "Missing or invalid task title",
        "Invalid due date format. Date must be in ISO 8601 format."
      ]
    }
  ],
  "total": 3
}
```