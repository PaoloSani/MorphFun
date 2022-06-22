from queue import Queue
import threading
from pynput import keyboard
import numpy as np
import multiprocessing as mp
from pose_estimation.pose_estimation_loop import estimate_pose
from utils import CONFIG_PATH, load_config
import os
import os
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()
from PyQt5.QtWidgets import QApplication
import sys
from GUI.PYQT_GUI import Window
from controller import controller
import warnings 


def main():
    warnings.filterwarnings("ignore")
    morphing_queue = Queue()
    command_queue = Queue()
    data_queue = Queue()

    controller_thread = threading.Thread(target=controller, args=(command_queue, data_queue, morphing_queue))
    controller_thread.start()

    App = QApplication(sys.argv)
    window = Window(command_queue, data_queue)
    window
    sys.exit(App.exec())
    
    
if __name__ == '__main__':
    main()


