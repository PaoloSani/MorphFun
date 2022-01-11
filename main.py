
from ddsp_functions.transform_audio import transform_audio
import time
from audio_utilities.record import record
from audio_utilities.convert_to_mixer_sounds import convert_to_mixer_sounds
from audio_utilities.play_sd_audio import play_sd_audio
import pygame
import pygame.mixer
from audio_utilities.start_playing import start_playing



recorded_audio = record(duration=5)
start_time = time.time()
play_sd_audio(recorded_audio)
new_audios = transform_audio(recorded_audio)
print('Total time:  %.1f seconds' % (time.time() - start_time))
pygame.mixer.init(frequency=22050, size=32)
sounds = convert_to_mixer_sounds(new_audios, pygame.mixer)
start_playing(sounds, loops=20)








        
    
    
    
    
    
    





