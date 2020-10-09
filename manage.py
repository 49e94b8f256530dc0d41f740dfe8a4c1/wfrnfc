import argparse
import getpass
import json
import logging
import os
import select
import sys

import cowsay
import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from tabulate import tabulate

import server.utils as utils
from server import app
from terminal.writer import write_tag

load_dotenv()


class RequestManager:
    headers = {}
    base_url = f"http://{os.getenv('SERVER_HOST')}:{os.getenv('SERVER_PORT')}"

    def __init__(self):
        logging.info(f"RequestManager will use base_url `{self.base_url}`")

    def make_request(self, url: str, method: str, **kwargs):
        url = f"{self.base_url}{url}"
        logging.debug(f"Request Manager Headers {self.headers}")
        if method == "GET":
            response = requests.get(url, headers=self.headers)
            return response.status_code, response.json()
        elif method == "POST":
            response = requests.post(url, json=kwargs.get("data"), headers=self.headers)
            return response.status_code, response.json()


def runserver():
    utils.create_tables()
    app.run()


def createsuperuser(**kwargs):
    utils.create_tables()
    utils.createsuperuser(**kwargs)


if __name__ == "__main__":
    description = "RFID Access Management Admin Console"

    request_manager = RequestManager()

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--action", help="admin, createsuperuser, runserver")
    args = parser.parse_args()

    def sys_exit(code=0):
        if code > 0:
            parser.print_help()
        GPIO.cleanup()
        exit(code)

    if len(sys.argv) == 1:
        sys_exit()

    args.action = args.action.strip()
    if args.action == "":
        sys_exit(1)
    if args.action == "admin":
        logging.info("Loading admin console")
        cowsay.cow("Welcome to the \n RFID Access Management \n Admin Console")
        logging.info("Requesting authentication credentials")
        email = input("Email:")
        email = email.strip()
        if not email:
            logging.error("You need an email address to access the admin console")
            sys_exit(0)
        password = getpass.getpass()
        password = password.strip()
        logging.debug(f"Trying to authenticate superuser `{email}`")
        try:
            status_code, response = request_manager.make_request(
                "/api/v1/login", "POST", data={"email": email, "password": password}
            )
        except Exception as e:
            logging.error(e)
            sys_exit(0)
        if status_code != 200:
            logging.error("Invalid authentication credentials")
            sys_exit(0)
        request_manager.headers.update(
            {"Authorization": f"Bearer {response.get('access_token')}"}
        )
        logging.info(f"Logged in as `{email}`")
        logging.info("Enter `q` or `Ctrl+C` to quit")
        while True:
            input = select.select([sys.stdin], [], [], 1)[0]
            # TODO: Add help command
            if input:
                command = sys.stdin.readline().rstrip()
                if command == "q":
                    sys.exit(0)
                elif command == "list terminals":
                    _, response = request_manager.make_request(
                        "/api/v1/terminals", "GET"
                    )
                    logging.info("Listing terminals")
                    # TODO: Show message if terminals empty
                    print(tabulate(response, headers="keys"))
                elif command == "create terminal":
                    _, response = request_manager.make_request(
                        "/api/v1/terminals", "POST"
                    )
                    logging.info(
                        f"Created terminal {response.get('registration_token')}"
                    )
                elif command == "write tag":
                    _, response = request_manager.make_request("/api/v1/tags", "POST")
                    logging.info(f"Created tag {response.get('content')}")
                    write_tag(response.get("content"))
                else:
                    logging.info(f"Command `{command}` not found")
            else:
                pass
    elif args.action == "createsuperuser":
        logging.info("Requesting potential authentication credentials")
        email = input("Email:")
        email = email.strip()
        if not email:
            logging.error("You need an email address to access the admin console")
            sys_exit(0)
        password1 = getpass.getpass()
        password1 = password1.strip()
        password2 = getpass.getpass(prompt="Repeat password:")
        password2 = password2.strip()
        if password1 != password2:
            logging.error("Passwords do not match")
            sys_exit(0)
        createsuperuser(email=email, password=password1)
        logging.info(f"Superuser `{email}` successfully created")
    elif args.action == "runserver":
        runserver()
    else:
        sys_exit(1)
    sys_exit()
