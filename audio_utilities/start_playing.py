from take_user_input import take_user_input



def start_playing(sounds, loops):
    for sound in sounds:
        sound.play(loops=loops)
        sound.set_volume(0.0)
        
    sounds[0].set_volume(1.0)
    sound = sounds[0]
    
    i=0
    while i<30:
        which_sound = take_user_input()
        sound.set_volume(0.0)
        sounds[which_sound].set_volume(1.0)
        sound = sounds[which_sound]
        i=i+1
    return

