import sounddevice as sd
import librosa

SR = 16000
TARGET_SR = 44100

def play_sd_audio(audio):
    myrecording_hq = librosa.resample(audio.ravel(), SR, TARGET_SR, res_type='kaiser_best') #resampling at 44100 just to playback what we just recorded at higher quality
    sd.play(myrecording_hq, TARGET_SR) #playing back the recording
    return