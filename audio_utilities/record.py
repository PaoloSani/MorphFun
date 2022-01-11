import sounddevice as sd
import numpy as np



SR = 16000

def record(duration):

    myrecording = sd.rec(int(duration * SR), samplerate=SR, channels=1, dtype=np.float32) #recording at sr=16000
    print("RECORDING")
    sd.wait()
    print("FINISHED")
    return myrecording 

