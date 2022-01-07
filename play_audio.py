import sounddevice as sd

def play_audio(audio):
    sd.play(audio, 48000)
    sd.wait()
    return