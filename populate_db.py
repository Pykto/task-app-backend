from flask import Flask
import requests
import random
from datetime import datetime, timedelta
import json

app = Flask(__name__)

BASE_URL = "http://localhost:5000/tareas"

priorities = ["LOW", "MEDIUM", "HIGH"]
states = ["PENDING", "IN_PROGRESS", "COMPLETED", "CANCELLED"]

def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.isoformat()

def populate_database(num_tasks=20):
    start_date = datetime(2025, 4, 1)
    end_date = datetime(2025, 4, 30)

    for i in range(1, num_tasks + 1):
        title = f"Title {i}"
        description = f"Description {i}"
        priority = random.choice(priorities)
        state = random.choice(states)
        creation_date = datetime.now().isoformat()
        expiration_date = generate_random_date(start_date, end_date) if random.random() < 0.8 else None # 80% chance of having an expiration date

        task_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "state": state,
            "creation_date": creation_date,
            "expiration_date": expiration_date
        }

        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(BASE_URL, headers=headers, data=json.dumps(task_data))
            response.raise_for_status()
            print(f"Sucessful creation of task {i}. ID: {response.json().get('id')}")
        except requests.exceptions.RequestException as e:
            print(f"Error at task creation {i}: {e}")
            if response is not None:
                print(f"Server response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    num_tasks_to_create = 40
    print(f"Populating {num_tasks_to_create} random tasks to DataBase...")
    populate_database(num_tasks_to_create)
    print("Population completed")