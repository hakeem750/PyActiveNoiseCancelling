import pyaudio
import numpy as np
import struct
import time
from Config import sampRate, chunk, audioFormat, promptDeviceInput

audio = pyaudio.PyAudio()
devCount=audio.get_device_count()

devices = {}

#Find indices for all devices to be used
if promptDeviceInput:
    #List all devices
    print("{0} audio devices found.")
    for d in range(devCount):
        print(str(d)+". "+ audio.get_device_info_by_index(d)["name"])
    #Prompt the user to input the indices
    devices['ambient'] = int(input("Enter index of ambient microphone: "))
    devices['inEar'] = int(input("Enter index of in-ear microphone: "))
    devices['output'] = int(input("Enter index of output speakers: "))

else:
    from Config import configDevices
    devices = configDevices

#Print selected devices
for dev in devices:
    print("{0} device: {1}".format(dev, audio.get_device_info_by_index(devices[dev])["name"]))
#time.sleep(5)

streams = {}
#Open the microphone stream
streams['ambient'] = audio.open(format=audioFormat, channels = 1, rate=sampRate, input=True, frames_per_buffer=chunk, input_device_index = devices['ambient'])
#Open the feedback microphone streams
streams['inEar'] = audio.open(format=audioFormat, channels = 2, rate=sampRate, input=True, frames_per_buffer=chunk, input_device_index = devices['inEar'])
#Open the output streams
streams['output'] = audio.open(format=audioFormat, channels = 2, rate=sampRate, output=True, frames_per_buffer=chunk, input_device_index = devices['output'])

#Main feedback loop
#Break on Ctrl-C input. TODO: Change this to not be an exception. 
try:
    while(1):
        #Read and unpack all data
        ambientData = streams['ambient'].read(chunk)
        ambientData = np.array(struct.unpack(str(2 * chunk) + 'B', ambientData), dtype='b')
        #TODO add the other two input streams
        
        #FFT the ambient audio the find primary frequencies to block
        freqs = np.fft.fftfreq(len(ambientData))
        ambientFFT=np.fft.fft(ambientData)
        #Find the peak frequency
        #TODO - find more than one frequency.
        freqIdx = np.argmax(np.abs(ambientFFT))
        peakFreq = freqs[freqIdx]
        print("Peak frequency: {0}".format(str(abs(peakFreq*sampRate))))

        #frames.append(ambientData)
except KeyboardInterrupt:
    print("KB Interrupt")
