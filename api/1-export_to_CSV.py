#!/usr/bin/python3 
"""
Export employee TODO list data to a CSV file.

This script fetches and exports an employee's TODO list from the 
'jsonplaceholder.typicode.com' API based on the given employee ID 
to a CSV file. The file includes employee ID, username, task 
completion status, and task title.

Usage:
    python3 1-export_to_CSV.py <employee_id>

Dependencies:
    - `requests`: To fetch data from the API.
    - `csv`: To write data to a CSV file.

Errors:
    - Invalid employee ID or missing tasks.
"""

import csv
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 1-export_to_CSV.py <employee_id>")
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

    # Write data to CSV
    file_name = "{}.csv".format(employee_id)
    with open(file_name, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for task in todos:
            writer.writerow([employee_id, username, str(task["completed"]), task["title"]])

    print("Data exported successfully to {}".format(file_name))
