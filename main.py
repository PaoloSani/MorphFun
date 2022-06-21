import asyncio
from multiprocessing.dummy import connection
from turtle import clear
from OSC_utilities.get_socket import get_socket
import OSC_utilities.initialize_server as initialize_server
from queue import Queue
import threading
from pynput import keyboard
from audio_routine import generate_morphed_audios
from audio_utilities.handle_record import start_recording, stop_recording, handle_recorded_audio
import numpy as np
from audio_utilities.start_morphing import play_sd_audio
import multiprocessing as mp
from audio_utilities.start_morphing import start_morphing
from pose_estimation.pose_estimation_loop import estimate_pose
from utils import CONFIG_PATH, load_config
import os
import os
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()

global connectionIsActive
connectionIsActive = False
global queue
queue = Queue()
RECORDING_SR = 44100
messages = dict(zip(range(5), ['Toggle Record', 'Violin', 'Flute', 'Trumpet', 'Sax']))


def on_press(key):
    if key == keyboard.Key.esc:
        global connectionIsActive
        connectionIsActive = False
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

def get_OSC_msg_value(sock):
    global queue
    while True:
        try:
            data, _ = sock.recvfrom(4096)
            value  = data[-1]
            queue.put(value)
        except OSError:
            break
        

async def main():
    global connectionIsActive
    global queue 
    init = True
    global stop_threads
    startRecording = True
    config = load_config(CONFIG_PATH)
    max_duration = config['main']['max_duration']
    model_path = config['files']['model_path']
    audio_folder = config['files']['audio']
    os.makedirs(audio_folder, exist_ok=True)
    morphingOn = True
    morphingQueue = Queue()
    initMorphing = True
    recorded_audio =  np.zeros((RECORDING_SR* max_duration, 1), np.float32)
    

    transport = await initialize_server.initialize_server() 
    connectionIsActive = True
    sock = get_socket(transport)


    print("\nEnter 'Esc' to close the connection at any time\n")

    exitListener = keyboard.Listener(on_press=on_press, daemon=True)
    exitListener.start()

    messageReader = threading.Thread(target=get_OSC_msg_value, args=(sock,), daemon=True)
    messageReader.start()


    pose_estimation = threading.Thread(target=estimate_pose, args=(model_path,), daemon=True)

    morphing_thread = threading.Thread(target=start_morphing, args=(morphingQueue,), daemon=True) # , sounds, loop=20
    
    while(connectionIsActive):
        if ( init ):
            print("\n")
            print("Ready to record audio!")
            print("\n")   
            init = False     
        else:
            if ( not queue.empty() ):
                message = queue.get()
                print(f"Message received \"{messages.get(message)}\"")
                if (message == 0):
                    if ( morphing_thread.is_alive() ):
                        morphingQueue.put(-1)
                        morphing_thread.join()
                        morphing_thread = threading.Thread(target=start_morphing, args=(morphingQueue,), daemon=True)
                        initMorphing = True

                    morphingOn = False
                    if ( startRecording ):
                        startRecording = False
                        start_time = start_recording(recorded_audio)
                    else:
                        startRecording = True
                        stop_recording()
                        recorded_audio = handle_recorded_audio(recorded_audio=recorded_audio, start_time=start_time, max_duration=max_duration)
                        play_sd_audio(recorded_audio)
                        morphingOn = True
                        print("\n!!! M0RPH!NG B3G!N$ !!!\n")
                        recorded_audio_path = os.path.join(audio_folder, 'recorded_audio.npy')
                        np.save(recorded_audio_path, recorded_audio)
                        print(recorded_audio_path)

                        morphing_process = threading.Thread(target=generate_morphed_audios, args=(recorded_audio,), daemon=True)

                        morphing_process.start()
                        morphing_process.join()   
                        print('Audios were generated.')

                else:
                    if ( morphingOn ):
                        if initMorphing:
                            morphing_thread.start()
                            pose_estimation.start()

                        morphingQueue.put(message)




    
    print("\n\nClosing connection\n\n")
    if ( morphing_process.is_alive() ):
        morphing_process.raise_exception()
        morphing_process.join()

    transport.close()

asyncio.run(main())


