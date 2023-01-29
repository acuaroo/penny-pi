from picamera import PiCamera 
from time import sleep
from multiprocessing import Process
import os
import bluetooth
import controller
import numpy as np
from datetime import datetime

CAMERA_SIZE = 128
PORT = 1
DEFAULT_SPEED = 40

camera = PiCamera()
camera.resolution = (CAMERA_SIZE, CAMERA_SIZE)
camera.rotation = -90

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", PORT))
server_socket.listen(PORT)

print("python server waiting on port: "+str(PORT))

client_socket, address = server_socket.accept()

print("python server connected to: "+str(address))

p_ena, p_enb = controller.gpio_init()

p_ena.start(DEFAULT_SPEED)
p_enb.start(DEFAULT_SPEED)

current_speed = DEFAULT_SPEED

data = ''
tick = 0
wait_time = 0.5

command_array = []
tick_array = []
speed_array = []
step_array = []

on = True
recording = False
session_id = datetime.now()

def camera_step(current_motion):
    global tick
    global current_speed 
    global wait_time

    if recording and current_motion != '':
        tick_array.append(tick)
        command_array.append(current_motion)
        speed_array.append(current_speed)
        step_array.append(wait_time)
        camera.capture('penny-pi/data/'+str(session_id)+'/'+str(tick)+'.png')


os.system("cd penny-pi/data | mkdir "+str(session_id))

print("session id created ("+str(session_id)+")")

while on:
    tick += 1
    data = client_socket.recv(1024)
    current_motion = ''

    if b'L' in data or b'G' in data:
        current_motion = 'L'
    elif b'R' in data or b'I' in data:
        current_motion = 'R'
    elif b'F' in data:
        current_motion = 'F'
    elif b'B' in data:
        controller.change_speed(current_speed, p_ena, p_enb)
        controller.go_backwards()
        current_motion = ''
    elif b'S' in data:
        controller.stop()
        current_motion = ''
        
    if b'W' in data:
        controller.stop()
        on = False
        recording = False
        break
    
    if b'1' in data:
        current_speed = DEFAULT_SPEED+(6*1)
        controller.change_speed(DEFAULT_SPEED+(6*1), p_ena, p_enb)
    elif b'2' in data:
        current_speed = DEFAULT_SPEED+(6*2)
        controller.change_speed(DEFAULT_SPEED+(6*2), p_ena, p_enb)
    elif b'3' in data:
        current_speed = DEFAULT_SPEED+(6*3)
        controller.change_speed(DEFAULT_SPEED+(6*3), p_ena, p_enb)
    elif b'4' in data:
        current_speed = DEFAULT_SPEED+(6*4)
        controller.change_speed(DEFAULT_SPEED+(6*4), p_ena, p_enb)
    elif b'5' in data:
        current_speed = DEFAULT_SPEED+(6*5)
        controller.change_speed(DEFAULT_SPEED+(6*5), p_ena, p_enb)
    elif b'6' in data:
        current_speed = DEFAULT_SPEED+(6*6)
        controller.change_speed(DEFAULT_SPEED+(6*6), p_ena, p_enb)
    elif b'7' in data:
        current_speed = DEFAULT_SPEED+(6*7)
        controller.change_speed(DEFAULT_SPEED+(6*7), p_ena, p_enb)
    elif b'8' in data:
        current_speed = DEFAULT_SPEED+(6*8)
        controller.change_speed(DEFAULT_SPEED+(6*8), p_ena, p_enb)
    elif b'9' in data:
        current_speed = DEFAULT_SPEED+(6*9)
        controller.change_speed(DEFAULT_SPEED+(6*9), p_ena, p_enb)
    elif b'q' in data:
        current_speed = DEFAULT_SPEED+(6*10)
        controller.change_speed(DEFAULT_SPEED+(6*10), p_ena, p_enb)

    
    if b'U' in data:
        recording = True
    elif b'u' in data:
        recording = False

#    if recording and tick % 10 == 0:
#        #prevent any delay from screwing up the driving
#        
#        #Process(target=camera_step, args=(current_motion,)).start()
#    
    if current_motion == 'L':
        #camera_step(current_motion)
        controller.change_speed(current_speed-(6*2), p_ena, p_enb)
        controller.turn_left()
        wait_time = 0.1
    if current_motion == 'R':
        #camera_step(current_motion)
        controller.change_speed(current_speed-(6*2), p_ena, p_enb)
        controller.turn_right()
        wait_time = 0.1
    if current_motion == 'F':
        controller.change_speed(current_speed, p_ena, p_enb)
        controller.go_forwards()
        wait_time = 0.5

    sleep(wait_time)
    controller.stop()
    #new "stutter" recording system
    if recording:
        camera_step(current_motion)

client_socket.close()
server_socket.close()

np.savez('penny-pi/data_'+str(session_id)+'.npz', commands=command_array, ticks=tick_array, speed=speed_array, step_interval=step_array)

print("python server closing")
