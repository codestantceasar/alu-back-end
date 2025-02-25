#!/usr/bin/python3
"""Script to use a REST API for a given employee ID, returns
information about his/her TODO list progress and export in JSON"""
import json
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("UsageError: python3 {} employee_id(int)".format(__file__))
        sys.exit(1)

    API_URL = "https://jsonplaceholder.typicode.com"
    EMPLOYEE_ID = sys.argv[1]

    response = requests.get(
        "{}/users/{}/todos".format(API_URL, EMPLOYEE_ID),
        params={"_expand": "user"}
    )
    data = response.json()

    if not len(data):
        print("RequestError:", 404)
        sys.exit(1)

    user_tasks = {EMPLOYEE_ID: []}
    for task in data:
        task_dict = {
            "task": task["title"],
            "completed": task["completed"],
            "username": task["user"]["username"]
        }
        user_tasks[EMPLOYEE_ID].append(task_dict)

    with open("{}.json".format(EMPLOYEE_ID), "w") as file:
        json.dump(user_tasks, file)
