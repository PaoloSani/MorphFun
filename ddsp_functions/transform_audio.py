import warnings
from ddsp_functions.common_pipeline import common_pipeline
from ddsp_functions.specific_model_pipeline import specific_model_pipeline
from ddsp_functions.resynthesize import resynthesize
from initial_path_setup import get_useful_model_paths
warnings.filterwarnings("ignore")
import numpy as np
import librosa
import time
from multiprocessing import Process

sr = 16000
target_sr = 44100


def transform_audio(audio):
    audio = librosa.resample(audio.ravel(), orig_sr=44100, target_sr=16000, res_type='kaiser_best')
    audio = audio.reshape((1,  np.shape(audio)[0]))
    start_process_time = time.time()
    model_names = ['Violin', 'Flute', 'Trumpet', 'Tenor_Saxophone']

    #getting all the useful paths for the models 
    models_paths = get_useful_model_paths(model_names)

    #common_pipeline
    audio_features= common_pipeline(audio)

    new_audios = []
   
    for model_name in model_names:
        model, audio_features = specific_model_pipeline(models_paths[model_name], audio, audio_features)
        new_audio = resynthesize(audio_features, model)
        new_audio = librosa.resample(new_audio, sr, target_sr, res_type='kaiser_best')
        new_audios.append(np.asarray(new_audio))
   
    print('Total time:  %.1f seconds' % (time.time() - start_process_time))
 
    return new_audios





    






    
    


    


    
 

