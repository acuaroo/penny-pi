import RPi.GPIO as GPIO

GREEN = 5
RED = 4
YELLOW = 3
light_show = False 

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

def light_show():
    light_show = True
    while light_show:
        green()
        sleep(0.5)
        yellow()
        sleep(0.5)
        red()
        sleep(0.5)
        yellow()
        sleep(0.5)

def stop_light_show():
    light_show = False