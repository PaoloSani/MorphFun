import numpy as np
import librosa
from ddsp.training.postprocessing import detect_notes, fit_quantile_transform
import ddsp


def model_conditioning(audio_features,  STATISTICS):
    #@markdown You can leave this at 1.0 for most cases
    threshold = 0.7  # @param {type:"slider", min: 0.0, max:2.0, step:0.01}


    #@markdown ## Automatic

    ADJUST = True  # @param{type:"boolean"}

    #@markdown Quiet parts without notes detected (dB)
    quiet = 20  # @param {type:"slider", min: 0, max:60, step:1}

    #@markdown Force pitch to nearest note (amount)
    autotune = 0.0 # @param {type:"slider", min: 0.0, max:1.0, step:0.1}

    #@markdown ## Manual


    #@markdown Shift the pitch (octaves)
    pitch_shift = -1  # @param {type:"slider", min:-2, max:2, step:1}

    #@markdown Adjust the overall loudness (dB)
    loudness_shift = 0  # @param {type:"slider", min:-20, max:20, step:1}


    audio_features_mod = {k: v for k, v in audio_features.items()}


    ## Helper functions.
    def shift_ld(audio_features, ld_shift=0.0):
      """Shift loudness by a number of ocatves."""
      audio_features['loudness_db'] += ld_shift
      return audio_features


    def shift_f0(audio_features, pitch_shift=0.0):
      """Shift f0 by a number of ocatves."""
      audio_features['f0_hz'] *= 2.0 ** (pitch_shift)
      audio_features['f0_hz'] = np.clip(audio_features['f0_hz'],
                                        0.0,
                                        librosa.midi_to_hz(110.0))
      return audio_features


    def get_tuning_factor(f0_midi, f0_confidence, mask_on):
      """Get an offset in cents, to most consistent set of chromatic intervals."""
      # Difference from midi offset by different tuning_factors.
      tuning_factors = np.linspace(-0.5, 0.5, 101)  # 1 cent divisions.
      midi_diffs = (f0_midi[mask_on][:, np.newaxis] -
                    tuning_factors[np.newaxis, :]) % 1.0
      midi_diffs[midi_diffs > 0.5] -= 1.0
      weights = f0_confidence[mask_on][:, np.newaxis]

      ## Computes mininmum adjustment distance.
      cost_diffs = np.abs(midi_diffs)
      cost_diffs = np.mean(weights * cost_diffs, axis=0)

      ## Computes mininmum "note" transitions.
      f0_at = f0_midi[mask_on][:, np.newaxis] - midi_diffs
      f0_at_diffs = np.diff(f0_at, axis=0)
      deltas = (f0_at_diffs != 0.0).astype(np.float)
      cost_deltas = np.mean(weights[:-1] * deltas, axis=0)

      # Tuning factor is minimum cost.
      norm = lambda x: (x - np.mean(x)) / np.std(x)
      cost = norm(cost_deltas) + norm(cost_diffs)
      return tuning_factors[np.argmin(cost)]





    mask_on = None

    if ADJUST and STATISTICS is not None:
      # Detect sections that are "on".
      mask_on, note_on_value = detect_notes(audio_features['loudness_db'],
                                            audio_features['f0_confidence'],
                                            threshold)

      if np.any(mask_on):
        # Shift the pitch register.
        target_mean_pitch = STATISTICS['mean_pitch']
        pitch = ddsp.core.hz_to_midi(audio_features['f0_hz'])
        mean_pitch = np.mean(pitch[mask_on])
        p_diff = target_mean_pitch - mean_pitch
        p_diff_octave = p_diff / 12.0
        round_fn = np.floor if p_diff_octave > 1.5 else np.ceil
        p_diff_octave = round_fn(p_diff_octave)
        audio_features_mod = shift_f0(audio_features_mod, p_diff_octave)

        # Quantile shift the note_on parts.
        _, loudness_norm = fit_quantile_transform(
            np.asarray(audio_features['loudness_db']),
            mask_on,
            inv_quantile=STATISTICS['quantile_transform'])

        # Turn down the note_off parts.
        mask_off = np.logical_not(mask_on)
        loudness_norm[mask_off] -= quiet * \
            (1.0 - note_on_value[mask_off][:, np.newaxis])
        loudness_norm = np.reshape(
            loudness_norm, audio_features['loudness_db'].shape)

        audio_features_mod['loudness_db'] = loudness_norm



      else:
        print('\nSkipping auto-adjust (no notes detected or ADJUST box empty).')

    else:
      print('\nSkipping auto-adujst (box not checked or no dataset statistics found).')


    
    return audio_features_mod