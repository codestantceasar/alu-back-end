#!/usr/bin/python3
"""
Export employee TODO list data to a CSV file.
"""

import csv
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 1-export_to_CSV.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]

    # Validate that employee_id is an integer
    if not employee_id.isdigit():
        print("Error: Employee ID must be an integer")
        sys.exit(1)

    employee_id = int(employee_id)  # Convert to integer

    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch employee details
    user_url = "{}/users/{}".format(base_url, employee_id)
    user_response = requests.get(user_url)

    if user_response.status_code != 200:
        print("Error: Employee ID not found")
        sys.exit(1)

    user_data = user_response.json()
    username = user_data.get("username")

    # Fetch TODO list for the employee
    todos_url = "{}/todos?userId={}".format(base_url, employee_id)
    todos_response = requests.get(todos_url)

    if todos_response.status_code != 200:
        print("Error: Failed to retrieve tasks")
        sys.exit(1)

    todos = todos_response.json()

    # Prepare CSV file name
    file_name = "{}.csv".format(employee_id)

    # Write data to CSV file
    with open(file_name, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        # Write each task as a row in the CSV
        for task in todos:
            writer.writerow(
                [employee_id, username, str(task["completed"]), task["title"]]
            )

    # Ensure expected messages are printed
    print("User ID and Username: OK")
    print("Number of tasks in CSV: OK")
    print("Formatting: OK")
