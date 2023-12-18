import logging
import random
import csv


def read_credentials_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)


credentials_list = read_credentials_from_csv('./tests/one/credentials_only2.csv')


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
    else:
        logging.info("Logout not needed.")