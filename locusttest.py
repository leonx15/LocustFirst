from locust import HttpUser, task, between
import logging
from utils import login, logout


class UserBehavior(HttpUser):
    host = "https://the-internet.herokuapp.com"
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_logout = False

    def on_start(self):
        # In this place we set a path to our certificate to allow https requests.
        # if not needed please comment line below.
        # self.client.verify = './cert/certific.pem'
        login(self)



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
        logout(self)


