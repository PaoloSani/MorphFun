import tensorflow as tf
import pickle
import gin
import time
import ddsp

from model_conditioning import model_conditioning


def specific_model_pipeline(model_paths, audio, audio_features):
    DATASET_STATS = None

    try:
        if tf.io.gfile.exists(model_paths['dataset_stats_file']):
            with tf.io.gfile.GFile(model_paths['dataset_stats_file'], 'rb') as f:
                DATASET_STATS = pickle.load(f)
    except Exception as err:
        print('Loading dataset statistics from pickle failed: {}.'.format(err))

    # Parse gin config,
    with gin.unlock_config():
        gin.parse_config_file(model_paths['gin_file'], skip_unknown=True)

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


    # Set up the model just to predict audio given new conditioning
    model = ddsp.training.models.Autoencoder()
    model.restore(model_paths['ckpt'])

    # Build model by running a batch through it.
    start_time = time.time()
    _ = model(audio_features, training=False)
    print('Restoring model took %.1f seconds' % (time.time() - start_time))
    
    
    audio_features_mod = model_conditioning(audio_features, DATASET_STATS)
    af = audio_features if audio_features_mod is None else audio_features_mod
    
    return (model, af)
