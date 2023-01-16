from picamera import PiCamera 
from time import sleep
import bluetooth
import controller

CAMERA_SIZE = 128
PORT = 1
DEFAULT_SPEED = 40

camera = PiCamera()
camera.resolution = (CAMERA_SIZE, CAMERA_SIZE)

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

on = True
recording = False

def camera_step(current_motion):
    global tick

    if recording and current_motion != '':
        camera.capture('data/'+current_motion+'/'+str(tick)+'.png')

while on:
    tick += 1
    data = client_socket.recv(1024)
    current_motion = ''

    if b'L' in data:
        controller.change_speed(current_speed-(6*2), p_ena, p_enb)
        controller.turn_left()
        current_motion = 'L'
    elif b'R' in data:
        controller.change_speed(current_speed-(6*2), p_ena, p_enb)
        controller.turn_right()
        current_motion = 'R'
    elif b'F' in data:
        controller.change_speed(current_speed, p_ena, p_enb)
        controller.go_forwards()
        current_motion = 'F'
    elif b'B' in data:
        controller.change_speed(current_speed, p_ena, p_enb)
        controller.go_backwards()
        current_motion = ''
    elif b'S' in data:
        controller.stop()
        current_motion = ''
    elif b'W' in data:
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

    if recording:
        camera_step(current_motion)


client_socket.close()
server_socket.close()

print("python server")