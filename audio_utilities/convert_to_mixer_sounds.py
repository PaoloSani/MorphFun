def convert_to_mixer_sounds(audios, pg_mixer):
    sounds=[]
    for audio in audios:
        sound = pg_mixer.Sound(audio)
        sounds.append(sound)
    return sounds



