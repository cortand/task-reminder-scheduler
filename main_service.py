"""
This microservice receives a list of task dictionaries over a ZeroMQ REQ socket, validates each task, stores valid ones
in a JSON file, and sends reminders 1 hour before each task's due date via a ZeroMQ PUB socket.

Expected task format:
{"title": "string", "due": "YYYY-MM-DDTHH:MM:SS"  # ISO 8601 format, must be in the future}
"""
import zmq
import json
import threading

from task_validation import validate_task                   # validates task titles and deadlines
from json_storage import load_json_file, save_json_file     # loads and saves JSON task data
from reminder_loop import reminder_loop                     # background loop for task alert triggers

# load tasks from json file
TASK_FILE = "tasks.json"
tasks = load_json_file(TASK_FILE)

# initialize ZeroMQ context and sockets
context = zmq.Context()

# REP socket to receive task data
rep_socket = context.socket(zmq.REP)
rep_socket.bind("tcp://*:5555")

# PUB socket to send reminders
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:5556")

# run reminder loop in a daemon thread
threading.Thread(target=reminder_loop, args=(tasks, pub_socket, TASK_FILE), daemon=True).start()
print("Task Reminder Service is running...")

# main loop to handle task scheduling
while True:
    incoming_json = rep_socket.recv_string()     # wait for request
    try:
        data = json.loads(incoming_json)
        # ensure input is a list of task dictionaries
        if not isinstance(data, list):
            raise ValueError("Error: Expected a list of tasks")

        # validate each task
        accepted, rejected = [], []
        for item in data:
            valid, error = validate_task(item)
            if valid:
                accepted.append(valid)
            elif error:
                rejected.append(error)

        # add valid tasks to list and save to JSON file
        tasks.extend(accepted)
        save_json_file(TASK_FILE, tasks)

        # send back response with status
        status = "success" if not rejected else "partial_success"
        rep_socket.send_string(json.dumps({
            "status": status,
            "added": len(accepted),
            "rejected": rejected,
            "total": len(tasks)
        }, indent=2))

    except Exception as e:
        # respond with error status for unexpected errors
        rep_socket.send_string(json.dumps({
            "status": "error",
            "message": str(e)
        }))
