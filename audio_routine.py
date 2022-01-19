import multiprocessing
from ddsp_functions.transform_audio import transform_audio
from audio_utilities.convert_to_mixer_sounds import convert_to_mixer_sounds
from audio_utilities.play_sd_audio import play_sd_audio
from audio_utilities.handle_record import handle_record
from audio_utilities.start_morphing import start_morphing
import pygame
import pygame.mixer


class AudioProcessingTask:
      
    def __init__(self, sock):
        self._sock = sock
        self._process = multiprocessing.Process(target=self.routine)

    def start(self):
        self._process.start()

    def terminate(self):
        self._process.terminate()
        
    def routine(sock):
        recorded_audio = handle_record(max_duration=14, socket=sock)
        play_sd_audio(recorded_audio)
        new_audios = transform_audio(recorded_audio)
        pygame.mixer.init(frequency=22050, size=32) # Initializing pygame.mixer for routing and syncing audio
        sounds = convert_to_mixer_sounds(new_audios, pygame.mixer) # convert our audios into pygame Sound objects
        start_morphing(sounds, loops= 20, socket = sock)
