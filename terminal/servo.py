import RPi.GPIO as GPIO
import time

SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

p = GPIO.PWM(SERVO_PIN, 50)
p.start(2.5)
try:
    while True:
        p.ChangeDutyCycle(7.5)
        time.sleep(1)
        # p.ChangeDutyCycle(12.5)
        # time.sleep(1)
        p.ChangeDutyCycle(2.5)
        time.sleep(1)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
