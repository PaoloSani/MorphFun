import sounddevice as sd
import numpy as np
import time
from OSC_utilities.get_OSC_msg_value import get_OSC_msg_value



RECORDING_SR = 44100


def handle_record(max_duration, socket):
    i = 0
    recorded_audio = np.zeros((RECORDING_SR * max_duration, 1), np.float32)
    while i < 2:
        OSC_msg_value = get_OSC_msg_value(socket)

        isRecord = (OSC_msg_value == 0)
        if (isRecord and i == 0):  # if OSC message is record message for the first time: --> Record the audio
            start_time = time.time()
            sd.rec(samplerate=RECORDING_SR, channels=1, dtype=np.float32,
                   out=recorded_audio)  # recording at sr=16000
            print("RECORDING")
            i += 1
        elif (isRecord and i == 1):  # if OSC message is record message or the second time--> Stop Recording
            sd.stop()
            print("FINISHED")
            total_time = time.time() - start_time
            i += 1

    if (total_time > max_duration):
        recorded_audio = recorded_audio[:int(max_duration * RECORDING_SR), :]
    else:
        recorded_audio = recorded_audio[:int(total_time * RECORDING_SR), :]
        
    return recorded_audio
    

    
   