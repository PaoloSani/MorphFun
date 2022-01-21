from audio_utilities.start_morphing import start_morphing
from ddsp_functions.transform_audio import transform_audio
from audio_utilities.convert_to_mixer_sounds import convert_to_mixer_sounds
import pygame
import pygame.mixer
from multiprocessing.pool import ThreadPool
import threading
import ctypes

def audio_function(recorded_audio=None):
    # new_audios_thread = audio_processing_thread('Transform Thread', transform_audio, (recorded_audio,))
    # new_audios_thread.start()
    init_mixer = pygame.mixer.init
    new_audios = transform_audio(recorded_audio)
    init_mixer(frequency=22050, size=32)
    sounds = convert_to_mixer_sounds(new_audios, pygame.mixer) # convert our audios into pygame Sound objects
    
    return sounds
    
class audio_processing_thread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=()):
        threading.Thread.__init__(self)
        self._name = name
        self._target = target
        self._args = args
        self.isDaemon = True
        self._return = None

        
    def run(self):
 
        # target function of the thread class
        try:
            print('Running ' + (self._target).__name__)
            if self._target is not None:
                self._return = self._target(self._args)

        finally:
            print('Ended ' + (self._target).__name__)
            return False

    def join(self):
        threading.Thread.join(self)
        return self._return 
          
    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')