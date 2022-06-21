from ddsp_functions.transform_audio import transform_audio
import numpy as np
import os
from utils import CONFIG_PATH, load_config

def generate_morphed_audios(audio=None):
    # recorded_audio = np.load(file_path, allow_pickle=True)
    config = load_config(CONFIG_PATH)
    audio_folder = config['files']['audio']
    sounds = transform_audio(audio)
    
    filenames = []
    for index, file in enumerate(sounds):
        path = os.path.join(audio_folder, f'{index}.npy')
        np.save(path, file)

        filenames.append(path)
