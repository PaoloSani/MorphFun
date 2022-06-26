from email.mime import audio
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import librosa
import time
import numpy as np
from utils import load_config, CONFIG_PATH
import os
import tensorflow as tf
import ddsp, gin, pickle
from ddsp_functions.model_conditioning import model_conditioning


sr = 16000
target_sr = 44100

class MorpherClass:
    def __init__(self):
        config = load_config(CONFIG_PATH)
        self.model_names = config['morphing']['model_names']
        self.model_files = self.get_useful_model_paths()
        self.models = None
                

    def get_model_files_paths(self, model_dir):
        #Getting the right ckpt file
        ckpt_files = [f for f in tf.io.gfile.listdir(model_dir) if 'ckpt' in f]
        ckpt_name = ckpt_files[0].split('.')[0]
        ckpt = os.path.join(model_dir, ckpt_name)
        
        #Getting the model files path
        model_data = {"dataset_stats_file": os.path.join(
            model_dir, 'dataset_statistics.pkl'),
            "gin_file": os.path.join(model_dir, 'operative_config-0.gin'),
            "ckpt": ckpt}
        
        return model_data


    def get_useful_model_paths(self):
        model_useful_paths = {}
        for model_name in self.model_names:
            model_dir_path = os.path.join(os.getcwd(), f'Source/models/{model_name}')
            model_useful_paths[f'{model_name}'] = {**self.get_model_files_paths(model_dir_path), **{"model_dir" : model_dir_path}}
            
        return model_useful_paths

    def init_model(self, path, audio_features):
        # Set up the model just to predict audio given new conditioning
        model = ddsp.training.models.Autoencoder()
        model.restore(path['ckpt'])
        start_time = time.time()
        _ = model(audio_features, training=False)
        print('Restoring model took %.1f seconds' % (time.time() - start_time))

        return model

    def resynthesize(self, audio_features, name):
        # Run a batch of predictions.
        model = self.models[name]
        start_time = time.time()
        outputs = model(audio_features, training=False)
        audio_gen = model.get_audio_from_outputs(outputs).numpy() 
        print('Prediction took %.1f seconds' % (time.time() - start_time))
        audio_gen = audio_gen[0]
        
        return audio_gen
        
    def compute_features(self, audio):
        ddsp.spectral_ops.reset_crepe()
        
        start_time = time.time()
        audio_features = ddsp.training.metrics.compute_audio_features(audio)
        audio_features['loudness_db'] = audio_features['loudness_db'].astype(
            np.float32)
        print('Audio features took %.1f seconds' % (time.time() - start_time))
        
        return audio_features

        
    def set_model_params(self, index, audio, audio_features):
        model_files = self.model_files[self.model_names[index]]
        try:
            if tf.io.gfile.exists(model_files['dataset_stats_file']):
                with tf.io.gfile.GFile(model_files['dataset_stats_file'], 'rb') as f:
                    DATASET_STATS = pickle.load(f)
        except Exception as err:
            print('Loading dataset statistics from pickle failed: {}.'.format(err))

        # Parse gin config,
        with gin.unlock_config():
            gin.parse_config_file(model_files['gin_file'], skip_unknown=True)

        # Ensure dimensions and sampling rates are equal
        time_steps_train = gin.query_parameter('F0LoudnessPreprocessor.time_steps')
        n_samples_train = gin.query_parameter('Harmonic.n_samples')
        hop_size = int(n_samples_train / time_steps_train)

        time_steps = int(audio.shape[1] / hop_size)
        n_samples = time_steps * hop_size

        gin_params = [
            'Harmonic.n_samples = {}'.format(n_samples),
            'FilteredNoise.n_samples = {}'.format(n_samples),
            'F0LoudnessPreprocessor.time_steps = {}'.format(time_steps),
            # Avoids cumsum accumulation errors.
            'oscillator_bank.use_angular_cumsum = True',
        ]

        with gin.unlock_config():
            gin.parse_config(gin_params)

        # Trim all input vectors to correct lengths
        for key in ['f0_hz', 'f0_confidence', 'loudness_db']:
            audio_features[key] = audio_features[key][:time_steps]
        audio_features['audio'] = audio_features['audio'][:, :n_samples]
        
        if self.models == None:
            self.models = {}
            self.models[f'{self.model_names[index]}'] = self.init_model(model_files, audio_features)
        elif len(self.models) != 4 :
            self.models[f'{self.model_names[index]}'] = self.init_model(model_files, audio_features)
                        
        audio_features_mod = model_conditioning(audio_features, DATASET_STATS)
        af = audio_features if audio_features_mod is None else audio_features_mod
        
        return af


    def transform_audio(self):
        config = load_config(CONFIG_PATH)
        audio_folder = config['files']['audio']
        file_path = os.path.join(audio_folder,'recorded_audio.npy')
        audio = np.load(file_path, allow_pickle=True)
        
        audio = librosa.resample(audio.ravel(), orig_sr=44100, target_sr=16000, res_type='kaiser_best')
        audio = audio.reshape((1,  np.shape(audio)[0]))
        start_process_time = time.time()

        #common_pipeline
        audio_features = self.compute_features(audio)
    
        for index, name in enumerate(self.model_names):
            audio_features = self.set_model_params(index, audio, audio_features)
            new_audio = self.resynthesize(audio_features, name)
            new_audio = librosa.resample(new_audio, sr, target_sr, res_type='kaiser_best')
            path = os.path.join(audio_folder, f'{index}.npy')
            np.save(path, new_audio)            
    
        print('Total time:  %.1f seconds' % (time.time() - start_process_time))
    
