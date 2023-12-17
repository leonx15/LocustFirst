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
        self.login()

    def login(self):
        # Perform Login action for each user.
        login_url = "/authenticate"
        credentials = random.choice(credentials_list)
        with self.client.post(login_url, data=credentials, catch_response=True) as response:
            if "Logout" in response.text:
                self.should_logout = True
            else:
                self.should_logout = False
            logging.info(f"Status Code: {response.status_code}")
            logging.info(f"Response Content: {response.text}")

    # Tasks listed below will be executed by users choosing one of them on each iteration.
    @task
    def one(self):
        logging.info("One")

    @task
    def two(self):
        logging.info("two")

    @task
    def three(self):
        logging.info("three")

    @task
    def four(self):
        logging.info("four")

    def on_stop(self):
        self.logout()

    def logout(self):
        if self.should_logout:
            with self.client.get("/logout", catch_response=True) as response:
                logging.info(f"Logout Response Status Code: {response.status_code}")
                logging.info(f"Logout Response Content: {response.text}")
                if "You logged out" in response.text:
                    logging.info("Correct logout response received")
                    response.success()
                else:
                    logging.error("Incorrect logout response")
                    response.failure("Incorrect response received for logout")
