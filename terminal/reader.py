import logging
import os
import sys
import time

import coloredlogs
import requests
import RPi.GPIO as GPIO
from dotenv import find_dotenv, load_dotenv
from mfrc522 import SimpleMFRC522

import Keypad
from LCD import LCD

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG")

SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

p = GPIO.PWM(SERVO_PIN, 50)

READER_TIMEOUT = 15
DOOR_TIMEOUT = 5

reader = SimpleMFRC522()

# Keypad setup
ROWS = 4  # number of rows of the Keypad
COLS = 4  # number of columns of the Keypad
keys = [
    "1",
    "2",
    "3",
    "A",  # key code
    "4",
    "5",
    "6",
    "B",
    "7",
    "8",
    "9",
    "C",
    "*",
    "0",
    "#",
    "D",
]
rowsPins = [12, 16, 20, 21]  # connect to the row pinouts of the keypad
colsPins = [6, 13, 19, 26]  # connect to the column pinouts of the keypad

load_dotenv(find_dotenv())

if __name__ == "__main__":
    base_url = f"http://{os.getenv('SERVER_HOST')}:{os.getenv('SERVER_PORT')}"
    logger.info(f"Using base_url `{base_url}`")
    if len(sys.argv) == 1:
        logging.error("No terminal registration token specified")
        sys.exit(0)
    registration_token = sys.argv[1]
    response = requests.get(f"{base_url}/api/v1/terminals/{registration_token}")
    if response.status_code == 404:
        logging.error("Terminal not found")
        sys.exit(0)
    logging.debug(f"Started terminal with registration token `{registration_token}`")
    lcd = LCD(2, 0x27, True)
    keypad = Keypad.Keypad(keys, rowsPins, colsPins, ROWS, COLS)  # create Keypad object
    keypad.setDebounceTime(50)  # set the debounce time
    p = GPIO.PWM(SERVO_PIN, 50)
    p.start(2.5)
    try:
        while True:
            logger.info("Hold a tag near the reader")
            lcd.message("WFRNFC RFID", 1)
            lcd.message("Access Control", 2)
            id, data = reader.read()
            logger.info("Tag read successfully")
            logger.debug(f"id `{id}` data `{data}`")
            data = data.strip()
            response = requests.post(
                f"{base_url}/api/v1/tags/verify", data={"content": data}
            )
            if response.status_code == 200:
                logger.info("Authentication successful, requesting TAN key")
                lcd.message("Enter TAN key", 1)
                lcd.message("# to confirm", 2)
                tan_key = ""
                while True:
                    key = keypad.getKey()
                    if key != keypad.NULL:
                        logging.debug(f"Key {key} pressed")
                        if key == "#":
                            break
                        tan_key += key
                        lcd.message(tan_key, 2)
                logging.info(f"Verifying TAN Key {tan_key}")
                response = requests.post(
                    f"{base_url}/api/v1/tags/verify/tan",
                    data={"content": data, "tan_key": tan_key},
                )
                if response.status_code == 200:
                    logging.debug("Door unlocked")
                    lcd.message("Welcome!", 1)
                    lcd.message("Door unlocked", 2)
                    p.start(2.5)
                    p.ChangeDutyCycle(7.5)
                    time.sleep(DOOR_TIMEOUT)
                    p.ChangeDutyCycle(2.5)
                    p.stop()
                else:
                    logging.error("TAN verification unsuccessful")
                    lcd.message("TAN verification", 1)
                    lcd.message("unsuccessful", 2)
            else:
                logger.error("Authentication unsuccessful")
                lcd.message("Authentication", 1)
                lcd.message("unsuccessful", 2)
            time.sleep(READER_TIMEOUT)
    except KeyboardInterrupt:
        logger.debug("Clear LCD")
        lcd.clear()
        logger.debug("Cleanup GPIO")
        GPIO.cleanup()
        p.stop()
        raise
