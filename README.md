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

## REQUEST: Sending tasks
Send a list of task disctionaries using a ZeroMQ REQ socket on port 5555.

### Address
`tcp://<host>:5555`

### Required message format:
```json
[
  {
    "title": "Submit CS361 Assignment 3",
    "due": "2025-08-05T15:00:00"
  }
]
```
### Validation Rules
- 'title' - Must be a non-empty string
- 'due' - Must be an ISO 8601 formatted string representing a date in the future

### Example (Python)
```python
# example data
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

task_data = [
    {
        "title": "Submit CS361 Assignment 3",       # valid title
        "due": "2025-08-05T15:00:00"                # valid due date
    },
    {
        "title": "",                                # invalid title (empty)
        "due": "2025-08-01T23:15:00"                # invalid due date (past)
    }
]

# send request
print("Sending tasks...")
socket.send_string(json.dumps(task_data))

# wait for reply
response = socket.recv_string()
print("Response from server:")
print(response)
```

### Expected Response: Task Scheduling Summary
After sending tasks, a JSON formatted response will be received indicating which task reminders were accpeted or rejected.
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

## RECEIVE: Reminder Alert Data
Subscribe to receive reminder notification using a ZeroMQ SUB socket

### Address
`tcp://<host>:5556`

### Format
- A reminder is triggerred at 1 hour before the due time (lead time is configurable in reminder_loop.py)
- The reminder is printed in the console and sent over the PUB socket as JSON message.
```json
{
  "type": "reminder",
  "task": {
    "id": "12345678",
    "title": "Submit CS361 Assignment 3",
    "due": "2025-08-05T15:00:00"
  }
}
```

### Example (Python)
```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, "") 

while True:
    message = socket.recv_string()
    print("Reminder received:", message)
```
### Console Output:
When a reminder is triggered, the microservice logs a message to the terminal:
```
[Reminder]: 'Submit CS361 Assignment 3' is due in 1 hour.
```
Note: This is for visbility. It does not get sent over ZeroMQ.

## UML Sequence Diagram
![UML Diagram] (UML_Sequence_Diagram.png)