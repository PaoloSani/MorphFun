from utils import CONFIG_PATH, load_config
import os
import numpy as np
import pygame
import sounddevice as sd

class AudioClass:
    def __init__(self, mixer):
        config = load_config(CONFIG_PATH)
        self.loops = config['morphing']['loops']
        self.audio_folder = config['files']['audio']
        self.mixer = mixer
        self.sounds = []
        self.sound_idx_to_mute = 0
    
    def load_sounds(self):
        file_names = [os.path.join(self.audio_folder, path) for path in os.listdir(self.audio_folder)]
        sounds = [np.load(file) for file in file_names]
        self.sounds = self.convert_to_mixer_sounds(sounds) # convert our audios into pygame Sound objects  

    def play_sd_audio(self, audio):
        sd.play(audio, 44100) #playing back the recording
        return
        
    def convert_to_mixer_sounds(self, audios):
        sounds=[]
        for audio in audios:
            sound = self.mixer.Sound(audio)
            sounds.append(sound)
        return sounds

    def start_playing_(self):
        for sound in self.sounds:
            sound.play(loops=self.loops)
            sound.set_volume(0.0)
            
        self.sounds[0].set_volume(1.0)
        self.sound_idx_to_mute = 0
        
    def pause_playing(self):
        if self.sounds != []:
            self.mixer.pause()

    def unpause_playing(self):
        if self.sounds != []:
            self.mixer.unpause()

    def stop_playing(self):
        if self.sounds != []:
            self.mixer.stop()

    def clear_playing(self):
        if self.sounds != []:
            for sound in self.sounds:
                sound.set_volume(0.0)
                
            self.sounds[4].set_volume(1.0)
            self.sound_idx_to_mute = 4

    def start_morphing(self, queue):
        
        self.start_playing_()

        while True:
            message = queue.get()
            if message == 4:
                continue
            elif message != -1:
                sound_idx_to_activate = message
                if (self.sound_idx_to_mute != sound_idx_to_activate):
                    sound = self.sounds[self.sound_idx_to_mute]
                    sound.set_volume(0.0)
                    self.sounds[sound_idx_to_activate].set_volume(1.0)
                    self.sound_idx_to_mute = sound_idx_to_activate

            else:
                break  
        
        self.stop_playing()

        return 
        