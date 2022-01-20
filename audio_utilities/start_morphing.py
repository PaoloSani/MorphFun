from audio_utilities.start_playing_ import start_playing_
from audio_utilities.change_instrument import change_instrument


def start_morphing(sounds, loops, socket):
    start_playing_(sounds, loops=loops)

    sound_idx_to_mute = 0

    i = 0
    while i < 200:
        if OSC_msg_value == 0:
            pass

        else:
            which_sound = OSC_msg_value - 1
            sound_idx_to_activate = which_sound
            if (sound_idx_to_mute != sound_idx_to_activate):
                sound_idx_to_mute = change_instrument(
                    sounds, sound_idx_to_mute, sound_idx_to_activate=sound_idx_to_activate)
            i += 1
            
    return
    