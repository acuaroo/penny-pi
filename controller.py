import RPi.GPIO as GPIO
import lights 
from time import sleep

# stops annoying warnings
GPIO.setwarnings(False)

FRONT_LEFT = 17
REAR_LEFT = 22
FRONT_RIGHT = 23
REAR_RIGHT = 24

ENA = 25
ENB = 12

current_speed = 40

lights.init()

def change_speed(new_speed, ena, enb):
    current_speed = new_speed
    ena.ChangeDutyCycle(new_speed)
    enb.ChangeDutyCycle(new_speed)

def gpio_init():
    lights.light_show()
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(FRONT_LEFT, GPIO.OUT)
    GPIO.setup(REAR_LEFT, GPIO.OUT)
    GPIO.setup(FRONT_RIGHT, GPIO.OUT)
    GPIO.setup(REAR_RIGHT, GPIO.OUT)

    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)

    p_ena = GPIO.PWM(ENA, 1000)
    p_enb = GPIO.PWM(ENB, 1000)

    return (p_ena, p_enb)

def turn_right():
    lights.stop_light_show()
    lights.green()
    GPIO.output(FRONT_LEFT, GPIO.HIGH)
    GPIO.output(REAR_LEFT, GPIO.LOW)
    GPIO.output(FRONT_RIGHT, GPIO.LOW)
    GPIO.output(REAR_RIGHT, GPIO.HIGH)

def turn_left():
    lights.stop_light_show()
    lights.red()
    GPIO.output(FRONT_LEFT, GPIO.LOW)
    GPIO.output(REAR_LEFT, GPIO.HIGH)
    GPIO.output(FRONT_RIGHT, GPIO.HIGH)
    GPIO.output(REAR_RIGHT, GPIO.LOW)

def go_forwards():
    lights.stop_light_show()
    lights.yellow()
    GPIO.output(FRONT_LEFT, GPIO.HIGH)
    GPIO.output(REAR_LEFT, GPIO.LOW)
    GPIO.output(FRONT_RIGHT, GPIO.HIGH)
    GPIO.output(REAR_RIGHT, GPIO.LOW)

def go_backwards():
    lights.stop_light_show()
    GPIO.output(FRONT_LEFT, GPIO.LOW)
    GPIO.output(REAR_LEFT, GPIO.HIGH)
    GPIO.output(FRONT_RIGHT, GPIO.LOW)
    GPIO.output(REAR_RIGHT, GPIO.HIGH)

def stop():
    lights.stop_light_show()
    lights.stop()
    GPIO.output(FRONT_LEFT, GPIO.LOW)
    GPIO.output(REAR_LEFT, GPIO.LOW)
    GPIO.output(FRONT_RIGHT, GPIO.LOW)
    GPIO.output(REAR_RIGHT, GPIO.LOW)



