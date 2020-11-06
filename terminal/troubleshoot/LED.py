import os
import time

import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()

LED_PIN = int(os.getenv("LED_PIN"))
assert LED_PIN is not None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
print("LED on")
GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(1)
print("LED off")
GPIO.output(18, GPIO.LOW)
