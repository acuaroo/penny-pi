from picamera import PiCamera 
from picamera.array import PiRGBArray
from time import sleep
from multiprocessing import Process
import os
import bluetooth
import controller
import numpy as np
import tflite_runtime.interpreter as tflite
from datetime import datetime

CAMERA_SIZE = 128
PORT = 1
DEFAULT_SPEED = 75

interpreter = tflite.Interpreter(model_path='penny-pi/machine-learning/car-23-2-4-ta79.tflite')
interpreter.allocate_tensors()

output = interpreter.get_output_details()[0]
input = interpreter.get_input_details()[0]

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
predictions_array = []

on = True
self_driving = False
recording = False
session_id = datetime.now().strftime("%Y%m%d%H%M%S")

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


os.system("mkdir penny-pi/data/"+str(session_id))

print("session id created ("+str(session_id)+")")

controller.change_speed(current_speed, p_ena, p_enb)
    
while on:
    current_motion = ''
    tick += 1
    data = client_socket.recv(1024)
    wait_time = 0.5

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
    elif b'X' in data:
        self_driving = True
    elif b'x' in data:
        self_driving = False

    if self_driving:
        rawCapture = PiRGBArray(camera, size=(CAMERA_SIZE, CAMERA_SIZE))
        camera.capture(rawCapture, format="rgb")

        img_array = rawCapture.array
        img_array = img_array.reshape(1, CAMERA_SIZE, CAMERA_SIZE, 3)
        img_array = np.float32(img_array)
        #img_array = img_array / 255
        
        interpreter.set_tensor(input['index'], img_array)
        interpreter.invoke()

        predictions = interpreter.get_tensor(output['index'])
        #np.set_printoptions(precision=2, suppress=True)
        print(predictions)
        
        f = interpreter.get_tensor(output['index'])[0][0]
        l = interpreter.get_tensor(output['index'])[0][1]
        r = interpreter.get_tensor(output['index'])[0][2]

        if f > r and f > l:
            current_motion = 'F'
        elif r > f and r > l:
            current_motion = 'R'
        elif l > f and l > r:
            current_motion = 'L'

        predictions_array.append(current_motion)

        if len(predictions_array) >= 5:
            last_five = predictions_array[(len(predictions_array) - 5):]

            if last_five.count('R') == 5 or last_five.count('L') == 5:
                current_motion = 'F'
            
    else:
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

    if recording and not self_driving:
            camera_step(current_motion)

client_socket.close()
server_socket.close()

if recording:
    np.savez('penny-pi/data/'+str(session_id)+'/data.npz', commands=command_array, ticks=tick_array, speed=speed_array, step_interval=step_array)

print("python server closing")
