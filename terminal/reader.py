import logging
import os
import sys
import time
from pathlib import Path

import coloredlogs
import dht11
import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from mfrc522 import SimpleMFRC522

import Keypad
from LCD import LCD

env_path = Path(".") / ("..") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG")
# Load env variables
LED_PIN = int(os.getenv("LED_PIN"))
SERVO_PIN = int(os.getenv("SERVO_PIN"))
DHT11_PIN = int(os.getenv("DHT11_PIN"))
KEYPAD_COL_PINS = os.getenv("KEYPAD_COL_PINS").split(",")
KEYPAD_ROW_PINS = os.getenv("KEYPAD_ROW_PINS").split(",")
# Use BCM Mode
GPIO.setmode(GPIO.BCM)
# Setup pins
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

READER_TIMEOUT = int(os.getenv("READER_TIMEOUT", 7))
DOOR_TIMEOUT = int(os.getenv("DOOR_TIMEOUT", 3))

# Load reader
reader = SimpleMFRC522()

# DHT11 Module Setup
dht11 = dht11.DHT11(pin=DHT11_PIN)

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
    keypad = Keypad.Keypad(
        keys, KEYPAD_ROW_PINS, KEYPAD_COL_PINS, ROWS, COLS
    )  # create Keypad object
    keypad.setDebounceTime(50)  # set the debounce time
    servo = GPIO.PWM(SERVO_PIN, 50)
    try:
        while True:
            dht11_result = dht11.read()
            logger.info("Hold a tag near the reader")
            lcd.message("WFRNFC DEMO", 1)
            if dht11_result.is_valid():
                temperature = "%-3.1f C" % dht11_result.temperature
                humidity = "%-3.1f %%" % dht11_result.humidity
                lcd.message(f"{temperature} {humidity}", 2)
            else:
                lcd.message(f"DHT11 Module Error", 2)
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
                    lcd.message("Unlocking door", 2)
                    # Status LED ON
                    logger.debug("Turning status LED ON")
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    servo.start(2.5)
                    time.sleep(1)
                    servo.ChangeDutyCycle(7.5)
                    time.sleep(1)
                    servo.ChangeDutyCycle(12.5)
                    time.sleep(DOOR_TIMEOUT)
                    # Status LED OFF
                    GPIO.output(LED_PIN, GPIO.LOW)
                    logger.debug("Turning status LED OFF")
                    logging.debug("Locking door")
                    lcd.message("Locking door", 2)
                    servo.ChangeDutyCycle(2.5)
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
        servo.stop()
        raise
