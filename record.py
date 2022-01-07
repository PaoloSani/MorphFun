import sounddevice as sd
import numpy as np
import time
import librosa

fs = 16000
duration = 8  # seconds


def record_and_listen():

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    print("RECORDING")
    sd.wait()
    myrecording_swap = np.swapaxes(myrecording, 0, 1)
    print("FINISHED")

    myrecording_hq = librosa.resample(
        myrecording.ravel(), fs, fs*3, res_type='kaiser_best')
    sd.play(myrecording_hq, fs*3)

    return myrecording_swap

