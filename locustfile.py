from locust import HttpUser, task, between
import logging
import random
import csv

def read_credentials_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

credentials_list = read_credentials_from_csv('credentials.csv')

class UserBehavior(HttpUser):
    wait_time = between(1, 5)

    @task
    def login(self):
        login_url = "/authenticate"
        credentials = random.choice(credentials_list)

        with self.client.post(login_url, data=credentials, catch_response=True) as response:
            logging.info(f"Status Code: {response.status_code}")
            logging.info(f"Response Content: {response.text}")

            # Check for specific content in the response
            if "Logout" in response.text:
                logging.info("Logout found in the response")
                response.success()
            else:
                logging.info("Logout not found in the response")
                response.failure("Expected content not found in the response")
