import RPi.GPIO as GPIO

GREEN = 4
RED = 2
YELLOW = 3

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GREEN, GPIO.OUT)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(YELLOW, GPIO.OUT)

def green():
    GPIO.output(GREEN, GPIO.HIGH)

def red():
    GPIO.output(RED, GPIO.HIGH)

def yellow():
    GPIO.output(YELLOW, GPIO.HIGH)

def stop():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.LOW)