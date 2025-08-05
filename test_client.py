import zmq
import json
from datetime import datetime, timedelta

# connect to task reminder scheduler microservice
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Generate a due date 61 minutes from now (so the 1-hour reminder is triggerred)
future_due = (datetime.now() + timedelta(minutes=1)).isoformat()

# example data
task_data = [
    {
        "title": "Submit CS361 Assignment 3",       # valid title
        "due": future_due                           # valid due date
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