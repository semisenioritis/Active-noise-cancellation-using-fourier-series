

import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError



seg_size = 1024 * 2
form_shape = pyaudio.paInt16
channel = 1
rate = 44100

fig, ax = plt.subplots(1, figsize=(15, 7))


p = pyaudio.PyAudio()


stream = p.open(format=form_shape,channels=channel,rate=rate,input=True,output=True,frames_per_buffer=seg_size)


x = np.arange(0, 2 * seg_size, 2)


line, = ax.plot(x, np.random.rand(seg_size), '-', lw=2)


ax.set_title('WAVEFORM')
ax.set_xlabel('Samples')
ax.set_ylabel('Vol')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * seg_size)
plt.setp(ax, xticks=[0, seg_size, 2 * seg_size], yticks=[0, 128, 255])


plt.show(block=False)

print('stream started')


frame_count = 0
start_time = time.time()

while True:


    data = stream.read(seg_size)


    data_int = struct.unpack(str(2 * seg_size) + 'B', data)


    data_np = np.array(data_int, dtype='b')[::2] + 128

    line.set_ydata(data_np)


    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1

    except TclError:


        frame_rate = frame_count / (time.time() - start_time)

        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break