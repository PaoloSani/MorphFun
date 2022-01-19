import asyncio
from multiprocessing.dummy import connection
from OSC_utilities.get_socket import get_socket
from audio_routine import AudioProcessingTask as ap

import OSC_utilities.initialize_server as initialize_server

from pynput import keyboard

global connectionIsActive
connectionIsActive = False


def on_press(key):
    if key == keyboard.Key.esc:
        global connectionIsActive
        connectionIsActive = False
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys


async def main():

    transport = await initialize_server.initialize_server() 
    global connectionIsActive
    connectionIsActive = True
    sock = get_socket(transport)
    audio_process = ap(sock)

    print("\nEnter 'Esc' to close the connection at any time\n")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while(connectionIsActive):
        print("\n")
        print("Ready to record audio!")
        print("\n")

        audio_process.start()
        
    print("\n\nClosing connection\n\n")
    transport.close()

asyncio.run(main())
