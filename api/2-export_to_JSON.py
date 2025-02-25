#!/usr/bin/python3
"""
Export employee TODO list data to a JSON file.

This script fetches and exports an employee's TODO list from the
'jsonplaceholder.typicode.com' API based on the given employee ID
to a JSON file. The file includes employee ID, username, task
completion status, and task title in the required JSON format.

Usage:
    python3 2-export_to_JSON.py <employee_id>

Dependencies:
    - `requests`: To fetch data from the API.
    - `json`: To write data to a JSON file.

Errors:
    - Invalid employee ID or missing tasks.
"""

import json
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 2-export_to_JSON.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]

    # Validate employee ID
    if not employee_id.isdigit():
        print("Error: Employee ID must be an integer")
        sys.exit(1)

    employee_id = int(employee_id)
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch employee details
    user_url = "{}/users/{}".format(base_url, employee_id)
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print("Error: Employee ID not found")
        sys.exit(1)

    user_data = user_response.json()
    username = user_data.get("username")

    # Fetch TODO list
    todos_url = "{}/todos?userId={}".format(base_url, employee_id)
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print("Error: Failed to retrieve tasks")
        sys.exit(1)

    todos = todos_response.json()

    # Prepare data for JSON export
    tasks = []
    for task in todos:
        task_data = {
            "task": task["title"],
            "completed": task["completed"],
            "username": username
        }
        tasks.append(task_data)

    # Write data to JSON file
    file_name = "{}.json".format(employee_id)
    with open(file_name, mode="w", encoding="utf-8") as json_file:
        json.dump({str(employee_id): tasks}, json_file)

    print("Data exported successfully to {}".format(file_name))
