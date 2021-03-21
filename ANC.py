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
#streams['inEar'] = audio.open(format=audioFormat, channels = 2, rate=sampRate, input=True, frames_per_buffer=chunk, input_device_index = devices['inEar'])
#Open the output streams
streams['output'] = audio.open(format=audioFormat, channels = 2, rate=sampRate, output=True, frames_per_buffer=chunk, input_device_index = devices['output'])

#Main feedback loop
#Break on Ctrl-C input. TODO: Change this to not be an exception. 
n=0
inEarData=np.ndarray([2, chunk*2])
inEarFFT=np.ndarray([2, chunk*2])
try:
    while(n<1):
        #Read and unpack all data
        #Ambient
        ambientRead = streams['ambient'].read(chunk)
        ambientData = np.array(struct.unpack(str(2 * chunk) + 'B', ambientRead), dtype='b')
        #In-Ear
        #Deinterleave the stereo data
        """
        deinterleaved=[streams['inEar'].read(chunk)[idx::2] for idx in range(2)]
        for c in range(2):
            #Unpack both channels
            inEarData[c,:] = np.array(struct.unpack(str(2*chunk) + 'B', deinterleaved[c]), dtype='b')
            #FFT both channels
            inEarFFT[c,:] = np.fft.fft(inEarData[c,:])
            inEarFreqs= np.fft.fftfreq(len(inEarData[c,:]))
            freqIdx = np.argmax(np.abs(inEarFFT[c,:]))

            print(str(c) + " peak freq: " + str(abs(inEarFreqs[freqIdx]*sampRate*2)))
        """
        #FFT the ambient audio the find primary frequencies to block
        ambientFreqs = np.fft.fftfreq(len(ambientData))
        ambientFFT=np.fft.fft(ambientData)
        #Find the peak frequency
        #TODO - find more than one frequency.
        freqIdx = np.argmax(np.abs(ambientFFT))
        peakFreq = ambientFreqs[freqIdx]
        print("Peak frequency: {0}".format(str(abs(peakFreq*sampRate*2))))

        #frames.append(ambientData)
except KeyboardInterrupt:
    print("KB Interrupt")
