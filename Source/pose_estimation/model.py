import os
import tensorflow
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ReduceLROnPlateau


def create_model(sequence_length, actions):
    log_dir = os.path.join('Logs')
    callbacks = [
        EarlyStopping(monitor='val_loss', mode='min', patience=30, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', mode='min', patience=5, factor=0.5, min_lr=1e-5)
        ]

    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(sequence_length, 258)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(actions.shape[0], activation='softmax'))

    return model


def main():
    sequence_length = 30
    actions = np.array(['flute', 'violin', 'trumpet', 'saxophone', 'no action'])

    model = create_model(sequence_length, actions)
    print(model.summary())

if __name__  == '__main__':
    main()