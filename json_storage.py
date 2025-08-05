import json
import os


def load_json_file(filename, default=None):
    # use empty list if no default is provided
    if default is None:
        default = []

    # print message if file doesn't exist and return default
    if not os.path.exists(filename):
        print(f"File '{filename}' not found. Returning default value.")
        return default

    # attempt to load and parse JSON file; print error message and return default on failure
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{filename}'. Returning default value.")
        return default
    except Exception as e:
        print(f"Error loading '{filename}': {e}")
        return default


def save_json_file(filename, data):
    # attempt to save data as JSON to file; return status (True if successful, otherwise return False and print message)
    file_exists = os.path.exists(filename)

    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        if not file_exists:
            print(f"Created new file: {filename}")
        else:
            print(f"Updated file: {filename}")

        return True

    except Exception as e:
        print(f"Error saving '{filename}': {e}")
        return False
