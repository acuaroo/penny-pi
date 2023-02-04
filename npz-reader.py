import numpy as np
from PIL import Image

data_header = 'data'
data_address = '20230129085106'
data_index = 0

data = np.load(data_header+'_'+data_address+'.npz')


img = Image.open(data_header+'/'+data_address+'/'+str(data['ticks'][data_index])+'.png')
img.show()

print("command: "+str(data['commands'][data_index]))
print("speed: "+str(data['speed'][data_index]))
print("tick: "+str(data['ticks'][data_index]))
print("step interval: "+str(data['step_interval'][data_index]))