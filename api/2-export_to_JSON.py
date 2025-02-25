#!/usr/bin/python3
"""Script to use a REST API for a given employee ID, returns
information about his/her TODO list progress and export in JSON."""
import json
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("UsageError: python3 {} employee_id(int)"
              .format(__file__))
        sys.exit(1)

    API_URL = "https://jsonplaceholder.typicode.com"
    EMPLOYEE_ID = sys.argv[1]

    # Validate that EMPLOYEE_ID is an integer.
    if not EMPLOYEE_ID.isdigit():
        print("Error: Employee ID must be an integer, got {}."
              .format(EMPLOYEE_ID))
        sys.exit(1)
    else:
        print("Correct USER_ID: OK")

    url = "{}/users/{}/todos".format(API_URL, EMPLOYEE_ID)
    response = requests.get(url, params={"_expand": "user"})

    if response.status_code != 200:
        print("Error: Failed to retrieve tasks (status code: {})"
              .format(response.status_code))
        sys.exit(1)

    data = response.json()
    if not data:
        print("Error: No tasks found for USER_ID {}."
              .format(EMPLOYEE_ID))
        sys.exit(1)

    # Verify that data is a list of dicts.
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        print("USER_ID's value type is a list of dicts: OK")
    else:
        print("Error: Data is not a list of dicts for USER_ID {}."
              .format(EMPLOYEE_ID))
        sys.exit(1)

    print("All tasks found: OK")

    user_tasks = {EMPLOYEE_ID: []}
    for task in data:
        task_dict = {
            "task": task["title"],
            "completed": task["completed"],
            "username": task["user"]["username"]
        }
        user_tasks[EMPLOYEE_ID].append(task_dict)

    output_filename = "{}.json".format(EMPLOYEE_ID)
    with open(output_filename, "w") as file:
        json.dump(user_tasks, file)
