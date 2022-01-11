import numpy as np
import time


def resynthesize(audio_features, model):
    # Run a batch of predictions.
    start_time = time.time()
    outputs = model(audio_features, training=False)
    audio_gen = model.get_audio_from_outputs(outputs).numpy() 
    print('Prediction took %.1f seconds' % (time.time() - start_time))
    #audio_gen = audio_gen + np.abs(audio_gen.min())
    audio_gen = audio_gen[0]
    
    
    return audio_gen
    