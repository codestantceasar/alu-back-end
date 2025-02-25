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


def fetch_employee_data(employee_id):
    """
    Fetch employee details using the given employee_id.

    Args:
        employee_id (int): The employee ID to fetch details for.

    Returns:
        str: The username of the employee.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    user_url = f"{base_url}/users/{employee_id}"

    response = requests.get(user_url)
    if response.status_code != 200:
        print("Error: Employee ID not found.")
        sys.exit(1)

    user_data = response.json()
    return user_data.get("username")


def fetch_todos(employee_id):
    """
    Fetch the TODO list for the given employee ID.

    Args:
        employee_id (int): The employee ID to fetch tasks for.

    Returns:
        list: A list of tasks (dicts) for the employee.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    todos_url = f"{base_url}/todos?userId={employee_id}"

    response = requests.get(todos_url)
    if response.status_code != 200:
        print("Error: Failed to retrieve tasks.")
        sys.exit(1)

    return response.json()


def export_to_json(employee_id, username, tasks):
    """
    Export the employee TODO list to a JSON file.

    Args:
        employee_id (int): The employee ID.
        username (str): The username of the employee.
        tasks (list): A list of tasks (dicts).
    """
    file_name = f"{employee_id}.json"
    with open(file_name, mode="w", encoding="utf-8") as json_file:
        json.dump({str(employee_id): tasks}, json_file, ensure_ascii=False, indent=4)

    print(f"Data exported successfully to {file_name}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 2-export_to_JSON.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]

    # Validate employee ID
    if not employee_id.isdigit():
        print("Error: Employee ID must be an integer.")
        sys.exit(1)

    employee_id = int(employee_id)

    # Fetch employee data and tasks
    username = fetch_employee_data(employee_id)
    todos = fetch_todos(employee_id)

    # Prepare tasks for JSON export
    tasks = [
        {"task": task["title"], "completed": task["completed"], "username": username}
        for task in todos
    ]

    # Export data to JSON file
    export_to_json(employee_id, username, tasks)


if __name__ == "__main__":
    main()
