def start_playing_(sounds, loops):
    for sound in sounds:
        sound.play(loops=loops)
        sound.set_volume(0.0)
        
    sounds[0].set_volume(1.0)
    return 
    