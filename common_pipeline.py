import time
import numpy as np
import ddsp


def compute_features(audio):
    start_time = time.time()
    audio_features = ddsp.training.metrics.compute_audio_features(audio)
    audio_features['loudness_db'] = audio_features['loudness_db'].astype(
        np.float32)
    print('Audio features took %.1f seconds' % (time.time() - start_time))
    
    return (audio_features)



def common_pipeline(audio):
    # Setup the session.
    ddsp.spectral_ops.reset_crepe()
    
    #computing the features
    audio_features= compute_features(audio)
    return audio_features
    
    
    
    