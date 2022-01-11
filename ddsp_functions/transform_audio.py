import warnings
from common_pipeline import common_pipeline
from specific_model_pipeline import specific_model_pipeline
from resynthesize import resynthesize
from initial_path_setup import get_useful_model_paths
warnings.filterwarnings("ignore")
from scipy.io.wavfile import write
import numpy as np
import os
import librosa
import soundfile

sr = 16000
target_sr = 44100


def transform_audio(audio):
    audio = np.swapaxes(audio, 0, 1)
    model_names = ['Violin', 'Flute', 'Trumpet', 'Tenor_Saxophone']

    #getting all the useful paths for the models 
    models_paths = get_useful_model_paths(model_names)

    #common_pipeline
    audio_features= common_pipeline(audio)

    new_audios = []

    #For each model i generate the predicted audio
    for model_name in model_names:
        #specific moodel pipeline
        model, audio_features = specific_model_pipeline(models_paths[model_name], audio, audio_features)
        new_audio = resynthesize(audio_features, model)
        new_audio = librosa.resample(new_audio, sr, target_sr, res_type='kaiser_best')
        soundfile.write(os.path.join(os.getcwd(), 'generated_wav',f"{model_name}.wav"), new_audio, target_sr, subtype='PCM_16')
        new_audios.append(np.asarray(new_audio))
        

    return new_audios





    






    
    


    


    
 

