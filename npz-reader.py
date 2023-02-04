import numpy as np
from PIL import Image
import random
import os

data_header = 'data'
data_address = '20230129103343'
data_index = -1

#before 20230129103343 uses data_xxxx.npz format
data = np.load(data_header+'/'+data_address+'/'+'data.npz')

#make a for loop for the length of data['commands']
for i in range(len(data['commands'])):
    if i == len(data['commands'])-1:
        break

    data_index += 1

    tick = data['ticks'][data_index]
    command = data['commands'][data_index+1]

    img = Image.open(data_header+'/'+data_address+'/'+str(tick)+'.png')

    print("command: "+str(command))

    #save PIL image to folder
    img.save('training-data/'+str(command)+'/'+str(tick)+'_'+str(data_address)+'.png')

    # print("speed: "+str(data['speed'][data_index]))
    # print("tick: "+str(data['ticks'][data_index]))
    # print("step interval: "+str(data['step_interval'][data_index]))

#print the length of a directory
print("process finished")
print('forward: '+str(len(os.listdir('training-data/F'))))
print('right: '+str(len(os.listdir('training-data/R'))))
print('left: '+str(len(os.listdir('training-data/L'))))