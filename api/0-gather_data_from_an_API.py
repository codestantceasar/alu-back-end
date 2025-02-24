#!/usr/bin/python3
"""
Gather data from an API and display TODO list progress for a given employee ID.
"""

import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]

    # Validate that employee_id is an integer
    if not employee_id.isdigit():
        print("Error: Employee ID must be an integer")
        sys.exit(1)

    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch employee details
    user_url = "{}/users/{}".format(base_url, employee_id)
    user_response = requests.get(user_url)

    if user_response.status_code != 200:
        print("Error: Employee ID not found")
        sys.exit(1)

    user_data = user_response.json()
    employee_name = user_data.get("name")

    # Fetch TODO list for the employee
    tasks_url = "{}/todos".format(base_url)
    todos_response = requests.get(tasks_url, params={"userId": employee_id})

    if todos_response.status_code != 200:
        print("Error: Failed to retrieve tasks")
        sys.exit(1)

    todos = todos_response.json()

    # Filter completed tasks
    completed_tasks = [task["title"] for task in todos if task["completed"]]

    # Display output
    total_tasks = len(todos)
    completed_count = len(completed_tasks)

    print("Employee {} is done with tasks({}/{}):".format(
        employee_name, completed_count, total_tasks))

    for task in completed_tasks:
        print("\t {}".format(task))
