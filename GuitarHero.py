##############################################################
# Name: April Gauthreaux, Whitney Wallace, Gabe Thompson
# Description: Guitar Hero Game
##############################################################
###Breadboard Coding (Guitar Hero)###

import RPi.GPIO as GPIO
from time import sleep
from random import randint

switches = [ 20, 16, 12, 26 ]
leds = [6, 13, 19, 21 ]

GPIO.setmode(GPIO.BCM)
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leds, GPIO.OUT)

#Turns the LEDs on
def all_on():
	for i in leds:
		GPIO.output(leds, True)

#Turns the LEDs off
def all_off():
	for i in leds:
		GPIO.output(leds, False)
