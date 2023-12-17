# Simple sandbox project for Locust. :)

- Use PyCharm
- Install locust (file requirements)
- If you want to run this script from company laptop you need to extract certificate. To do this please follow the cert/howTo.txt instructions.

> [!NOTE]
>- to run locust test please use "locust" in terminal while standing in project directory.
>- To define specific test from our test library use standing in main directory of our project:
>  - locust -f ./tests/one/locusttest.py
>- remember to change in browser address for locust test from 0.0.0.0 to localhost.