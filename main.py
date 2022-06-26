from queue import Queue
import threading
from pynput import keyboard
import numpy as np
import multiprocessing as mp
from pose_estimation.pose_estimation_loop import estimate_pose
from utils import CONFIG_PATH, load_config
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()
from PyQt5.QtWidgets import QApplication
import sys
from GUI.PYQT_GUI import Window
from controller import controller
import warnings 
import tensorflow as tf 
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from pynput.keyboard import Key, Controller



def main():
    warnings.filterwarnings("ignore")
    command_queue = Queue()
    data_queue = Queue()
    morphing_queue = Queue()

    App = QApplication(sys.argv)

    window = Window(command_queue, data_queue)
    controller_thread = threading.Thread(target=controller, args=(App, command_queue, data_queue, morphing_queue))
    controller_thread.start()
    window
    sys.exit(App.exec())
    
    
if __name__ == '__main__':
    main()


