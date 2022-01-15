import asyncio
from ddsp_functions.transform_audio import transform_audio
from audio_utilities.convert_to_mixer_sounds import convert_to_mixer_sounds
from audio_utilities.play_sd_audio import play_sd_audio
import pygame
import pygame.mixer
import OSC_utilities.initialize_server as initialize_server
from OSC_utilities.get_socket import get_socket
from audio_utilities.handle_record import handle_record
from audio_utilities.start_morphing import start_morphing


    

async def main():

    transport = await initialize_server.initialize_server() 
    sock = get_socket(transport)
    print("Ready to Record")
    recorded_audio = handle_record(max_duration=14, socket=sock)
    play_sd_audio(recorded_audio)
    new_audios = transform_audio(recorded_audio)
    pygame.mixer.init(frequency=22050, size=32) #Initializing pygame.mixer for routing and syncing audio
    sounds = convert_to_mixer_sounds(new_audios, pygame.mixer) #convert our audios into pygame Sound objects
    start_morphing(sounds, loops= 20, socket = sock)
    transport.close()


asyncio.run(main())


