from locust import HttpUser, task, between
import logging
import random
import csv

def read_credentials_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

credentials_list = read_credentials_from_csv('./tests/one/credentials.csv')

class UserBehavior(HttpUser):
    host = "https://the-internet.herokuapp.com"
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_logout = False

    def on_start(self):
        # In this place we set a path to our certificate to allow https requests.
        # if not needed please comment line below.
        self.client.verify = './cert/certific.pem'

    @task(1)
    def login(self):
        login_url = "/authenticate"
        credentials = random.choice(credentials_list)

        with self.client.post(login_url, data=credentials, catch_response=True) as response:
            logging.info(f"Status Code: {response.status_code}")
            logging.info(f"Response Content: {response.text}")

            # Check for specific content in the response
            if "Logout" in response.text:
                logging.info("Logout found in the response")
                self.should_logout = True
            else:
                logging.info("Logout not found in the response")
                self.should_logout = False

            response.success()

    @task(2)
    def logout(self):
        if self.should_logout:
            # Sending a request to the logout URL
            with self.client.get("/logout", catch_response=True) as response:
                logging.info(f"Logout Response Status Code: {response.status_code}")
                logging.info(f"Logout Response Content: {response.text}")

                # Check if the response contains the expected text
                if "You logged out" in response.text:
                    logging.info("Correct logout response received")
                    response.success()
                else:
                    logging.error("Incorrect logout response")
                    response.failure("Incorrect response received for logout")

