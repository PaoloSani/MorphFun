



def change_instrument(sounds, sound_idx_to_mute, sound_idx_to_activate):
    sound = sounds[sound_idx_to_mute]
    sound.set_volume(0.0)
    sounds[sound_idx_to_activate].set_volume(1.0)
    return sound_idx_to_activate


