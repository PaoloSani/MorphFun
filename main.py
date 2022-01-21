import asyncio
from multiprocessing.dummy import connection
from turtle import clear
from OSC_utilities.get_socket import get_socket
import OSC_utilities.initialize_server as initialize_server
from queue import Queue
import threading
from pynput import keyboard
from audio_routine import audio_function, audio_processing_thread
from audio_utilities.handle_record import start_recording, stop_recording, handle_recorded_audio
import numpy as np
from audio_utilities.play_sd_audio import play_sd_audio
import multiprocessing as mp



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
    max_duration = 14
    startRecording = True
    morphingOn = True
    morphingQueue = Queue()
    recorded_audio =  np.zeros((RECORDING_SR* max_duration, 1), np.float32)
    

    transport = await initialize_server.initialize_server() 
    connectionIsActive = True
    sock = get_socket(transport)


    print("\nEnter 'Esc' to close the connection at any time\n")

    exitListener = keyboard.Listener(on_press=on_press, daemon=True)
    exitListener.start()

    messageReader = threading.Thread(target=get_OSC_msg_value, args=(sock,), daemon=True)
    messageReader.start()

    morphing_process = audio_processing_thread(name = 'Audio Thread', target=audio_function, args=(recorded_audio))
    
    while(connectionIsActive):
        if ( init ):
            print("\n")
            print("Ready to record audio!")
            print("\n")   
            init = False     
        else:
            if ( not queue.empty() ):
                message = queue.get()
                print("Message received \"{}\"" .format(messages.get(message)))
                if (message == 0):
                    if ( morphing_process.is_alive() ):
                        morphing_process.raise_exception()
                        morphing_process.join()
                        morphing_process = audio_processing_thread(name = 'Audio Thread', target=audio_function, args=(recorded_audio))

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
                        morphing_process.start()   

                else:
                    if ( morphingOn ):
                        morphingQueue.put(message)
                        # start_morphing(sounds, loops= 20)

    
    print("\n\nClosing connection\n\n")
    if ( morphing_process.is_alive() ):
        morphing_process.raise_exception()
        morphing_process.join()

    transport.close()

asyncio.run(main())


