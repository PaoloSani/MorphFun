from utils import CONFIG_PATH, load_config
import os
import numpy as np
import pygame
import sounddevice as sd

def play_sd_audio(audio):
    sd.play(audio, 44100) #playing back the recording
    return

def change_instrument(sounds, sound_idx_to_mute, sound_idx_to_activate):
    sound = sounds[sound_idx_to_mute]
    sound.set_volume(0.0)
    sounds[sound_idx_to_activate].set_volume(1.0)
    return sound_idx_to_activate

def convert_to_mixer_sounds(audios, pg_mixer):
    sounds=[]
    for audio in audios:
        sound = pg_mixer.Sound(audio)
        sounds.append(sound)
    return sounds

def start_playing_(sounds, loops):
    for sound in sounds:
        sound.play(loops=loops)
        sound.set_volume(0.0)
        
    sounds[0].set_volume(1.0)
    return 
    

def start_morphing(queue):
    config = load_config(CONFIG_PATH)
    loops = config['morphing']['loops']
    audio_folder = config['files']['audio']
    file_names = [os.path.join(audio_folder, path) for path in os.listdir(audio_folder)]
    file_names.remove('audio/recorded_audio.npy')
    sounds = [np.load(file) for file in file_names]
    init_mixer = pygame.mixer.init
    init_mixer(frequency=22050, size=32)
    sounds = convert_to_mixer_sounds(sounds, pygame.mixer) # convert our audios into pygame Sound objects  
    start_playing_(sounds, loops=loops)

    sound_idx_to_mute = 0

    while True:
        message = queue.get()
        if message != -1:
            which_sound = message - 1
            sound_idx_to_activate = which_sound
            if (sound_idx_to_mute != sound_idx_to_activate):
                sound_idx_to_mute = change_instrument(
                    sounds, sound_idx_to_mute, sound_idx_to_activate=sound_idx_to_activate)
        else:
            break  
    return 
    