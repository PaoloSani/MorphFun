import sounddevice as sd
import time
import numpy as np

RECORDING_SR = 44100
 
def start_recording(recorded_audio=None):  
    start_time = time.time()
    sd.rec(samplerate=RECORDING_SR, channels=1, dtype=np.float32,out=recorded_audio)  # recording at sr=16000
    print("RECORDING ON")

    return start_time

def stop_recording():
    sd.stop()
    print("RECORDING STOPPED")

def handle_recorded_audio(recorded_audio=None, start_time=None, max_duration=14):
    total_time = time.time() - start_time
    if (total_time > max_duration):
        recorded_audio = recorded_audio[:int(max_duration * RECORDING_SR), :]
    else:
        recorded_audio = recorded_audio[:int(total_time * RECORDING_SR), :]
        
    return recorded_audio
