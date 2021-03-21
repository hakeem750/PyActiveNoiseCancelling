import pyaudio

sampRate = 44100
chunk = 1024
audioFormat = pyaudio.paInt16
promptDeviceInput = False
ambientMic = 1
inEarMic = 17

configDevices = {}
configDevices['ambient']=1
configDevices['inEar']=17
configDevices['output']=22

