import pyaudio
import numpy
from Config import sampRate, chunk, audioFormat, promptDeviceInput

audio = pyaudio.PyAudio()
devCount=audio.get_device_count()



#Find indices for all devices to be used
if promptDeviceInput:
    #List all devices
    print("{0} audio devices found.")
    for d in range(devCount):
        print(str(d)+". "+ audio.get_device_info_by_index(d)["name"])
    #Prompt the user to input the indices
    micIndex=int(input("Enter index of ambient microphone: "))
else:
    from Config import micIn
    micIndex=micIn

#Open the microphone stream
ambientStream = audio.open(format=audioFormat, channels = 1, rate=sampRate, input=True, frames_per_buffer=chunk, input_device_index = micIndex)

