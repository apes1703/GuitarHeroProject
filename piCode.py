import RPi.GPIO as GPIO
from time import sleep

gLight = 13
rLight = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup([gLight, rLight], GPIO.OUT)

def greenLight():
    GPIO.output(gLight, GPIO.HIGH)
    sleep(0.009)
    GPIO.output(gLight, GPIO.LOW)

def redLight():
    GPIO.output(rLight, GPIO.HIGH)
    sleep(0.0009)
    GPIO.output(rLight, GPIO.LOW)

GPIO.cleanup()