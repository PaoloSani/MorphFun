import threading
from pynput import keyboard
from audio_utilities.handle_record import start_recording, stop_recording, handle_recorded_audio
import numpy as np
from audio_utilities.start_morphing import AudioClass
from ddsp_functions.morpher_module import MorpherClass 
from pose_estimation.pose_estimation_loop import estimate_pose
from utils import CONFIG_PATH, load_config
import os
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()
import pygame
global connectionIsActive
connectionIsActive = True

def on_press(key):
    if key == keyboard.Key.esc:
        global connectionIsActive
        connectionIsActive = False
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys


def controller(App, command_queue, data_queue, morphing_queue):
    global connectionIsActive
    config = load_config(CONFIG_PATH)
    max_duration = config['controller']['max_duration']
    model_path = config['files']['model_path']
    audio_folder = config['files']['audio']
    sr = config['controller']['sr']
    messages = config['controller']['messages']

    os.makedirs(audio_folder, exist_ok=True)

    init = True
    startRecording = True

    init_mixer = pygame.mixer.init
    init_mixer(frequency=22050, size=32)    
    mixer = pygame.mixer
    audio_controller = AudioClass(mixer)
    morpherClass = MorpherClass()

    recorded_audio =  np.zeros((sr* max_duration, 1), np.float32)
    
    print("\nEnter 'Esc' to close the connection at any time\n")

    exitListener = keyboard.Listener(on_press=on_press, daemon=True)
    exitListener.start()
    
    pose_estimation = threading.Thread(target=estimate_pose, args=(model_path, morphing_queue, data_queue,), daemon=True)

    morphing_thread = threading.Thread(target=audio_controller.start_morphing, args=(morphing_queue,), daemon=True)  


    while connectionIsActive:
        if ( init ):
            print("\n")
            print("Ready to record audio!")
            print("\n")   
            init = False
        else:
            if ( not command_queue.empty() ):
                message = command_queue.get()
                print(f"Message received \"{message}\"")

                if (message == 'Rec'):
                    if ( morphing_thread.is_alive() ):
                        recorded_audio =  np.zeros((sr* max_duration, 1), np.float32)
                        morphing_queue.put(-1)
                        morphing_thread.join()
                        data_queue.put(-1)
                        pose_estimation.join()
                        pose_estimation = threading.Thread(target=estimate_pose, args=(model_path, morphing_queue, data_queue,), daemon=True)
                        morphing_thread = threading.Thread(target=audio_controller.start_morphing, args=(morphing_queue,), daemon=True)

                    if ( startRecording ):
                        startRecording = False
                        start_time = start_recording(recorded_audio)
                    else:
                        startRecording = True
                        stop_recording()
                        recorded_audio = handle_recorded_audio(recorded_audio=recorded_audio, start_time=start_time, max_duration=max_duration)
                        

                        recorded_audio_path = os.path.join(audio_folder, 'recorded_audio.npy')
                        np.save(recorded_audio_path, recorded_audio)

                        print("\n!!! M0RPH!NG B3G!N$ !!!\n")
                        audio_controller.play_sd_audio(recorded_audio)
                        morphing_process = threading.Thread(target=morpherClass.transform_audio, daemon=True)

                        morphing_process.start()
                        morphing_process.join()   
                        print(f'Audios were generated and saved to {audio_folder}.')
                        audio_controller.load_sounds()
                        
                        morphing_thread.start()
                        pose_estimation.start()
                        data_queue.put('start')


                elif message == 'Play':
                    audio_controller.unpause_playing()
                
                elif message == 'Pause':
                    audio_controller.pause_playing()

                elif message == 'Clear':
                    audio_controller.clear_playing()

                else:
                    if message not in messages:
                        print(f'ERROR. {message} is not a valid message.')

    if ( morphing_thread.is_alive() ):
        morphing_queue.put(-1)
        morphing_thread.join()
        data_queue.put(-1)
        pose_estimation.join()
    
    print('Closing app.')

    try:
        App.quit()
    except:
        return   