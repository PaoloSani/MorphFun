from transform_audio import transform_audio
import numpy as np
import time
from record import record_and_listen
from play_audio import play_audio


def main():
    
    start_time = time.time()
    audio = record_and_listen()
    new_audios = transform_audio(audio)
    print('Total time:  %.1f seconds' % (time.time() - start_time))
    for new_audio in new_audios:
        play_audio(new_audio)
    
    
    return

main()