import time
from datetime import datetime, timedelta
import json
from json_storage import save_json_file

# store how early reminder alert should be sent
REMINDER_LEAD_TIME = timedelta(minutes=1)


def reminder_loop(tasks, pub_socket, task_file):
    """
    Background loop to monitor task deadlines and send reminders via ZeroMQ PUB socket.

    :param tasks: list of task dictionaries
    :param pub_socket: zmq pub socket used to send reminders
    :param task_file: path to the json file with updated task data

    :return: None
    """
    while True:
        # get current time
        now = datetime.now()

        for item in tasks:
            # only monitor deadline for tasks where a reminder has not been sent
            if not item.get("reminder_sent"):
                try:
                    due_time = datetime.fromisoformat(item["due"])
                    # check if current time is within the 1-hour reminder alert window
                    if now >= due_time - REMINDER_LEAD_TIME and now < due_time:
                        # format the reminder message
                        alert_msg = {
                            "type": "reminder",
                            "task": {
                                "id": item["id"],
                                "title": item["title"],
                                "due": item["due"]
                            }
                        }

                        # send reminder via PUB socket
                        pub_socket.send_string(json.dumps(alert_msg))

                        # format lead time into readable string
                        lead_minutes = int(REMINDER_LEAD_TIME.total_seconds() // 60)
                        if lead_minutes >= 60:
                            hours = lead_minutes // 60
                            minutes = lead_minutes % 60
                            if minutes > 0:
                                lead_str = f"{hours} hour{'s' if hours!= 1 else ''} {minutes} minute{'s' if minutes!= 1 
                                else ''}"
                            else:
                                lead_str = f"{hours} hour{'s' if hours != 1 else ''}"
                        else:
                            lead_str = f"{lead_minutes} minute{'s' if lead_minutes != 1 else ''}"

                        # print colored reminder alert in the terminal
                        print(f"\033[91m[Reminder]:\033[0m '{item['title']}' is due in {lead_str}.")

                        # flag the reminder as sent
                        item["reminder_sent"] = True

                        # update the JSON task list
                        save_json_file(task_file, tasks)

                except Exception as e:
                    # show any errors that occur
                    print(f"Reminder error for task '{item.get('title', 'unknown')}': {e}")

        # wait for 'sleep_time' amount of seconds before running loop again
        sleep_time = 10
        time.sleep(sleep_time)
