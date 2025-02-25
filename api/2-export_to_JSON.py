#!/usr/bin/python3
"""Script to use a REST API for a given employee ID, returns
information about his/her TODO list progress and export in JSON"""
import json
import requests
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "UsageError: python3 {} employee_id(int)".format(__file__)
        )
        sys.exit(1)

    API_URL = "https://jsonplaceholder.typicode.com"
    EMPLOYEE_ID = sys.argv[1]

    # Checking if the employee ID is a valid integer
    if not EMPLOYEE_ID.isdigit():
        print(
            "Invalid employee ID: {}. It must be an integer."
            .format(EMPLOYEE_ID)
        )
        sys.exit(1)

    # Make the API request
    url = "{}/users/{}/todos".format(API_URL, EMPLOYEE_ID)
    response = requests.get(url, params={"_expand": "user"})

    # Check for HTTP errors
    if response.status_code != 200:
        print(
            "Error fetching data from API. Status code: {}"
            .format(response.status_code)
        )
        sys.exit(1)

    # Check if response contains any tasks
    data = response.json()
    if not data:
        print("No tasks found for employee ID: {}".format(EMPLOYEE_ID))
        sys.exit(1)

    # Build the user tasks dictionary
    user_tasks = {EMPLOYEE_ID: []}
    for task in data:
        task_dict = {
            "task": task["title"],
            "completed": task["completed"],
            "username": task["user"]["username"]
        }
        user_tasks[EMPLOYEE_ID].append(task_dict)

    # Save data to a JSON file
    output_filename = "{}.json".format(EMPLOYEE_ID)
    with open(output_filename, "w") as file:
        json.dump(user_tasks, file)

    print(
        "Tasks for employee ID {} have been successfully saved to {}."
        .format(EMPLOYEE_ID, output_filename)
    )
