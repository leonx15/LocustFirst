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
    """
    This class represents a user behavior for login.
    Each user will wait between 1 to 5 seconds between tasks.
    """
    wait_time = between(1, 5)

    @task
    def login(self):
        """
        A task to simulate login action. This will send a POST request
        to the login endpoint with the specified credentials.
        """
        # URL for the login action
        login_url = "/authenticate"

        # Define the login credentials
        credentials = random.choice(credentials_list)

        # Send a POST request to the login form
        with self.client.post(login_url, data=credentials, catch_response=True) as response:
            # Logging the status code and response content
            logging.info(f"Status Code: {response.status_code}")
            logging.info(f"Response Content: {response.text}")


