from queue import Queue
import threading
import multiprocessing as mp
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()
from PyQt5.QtWidgets import QApplication
import sys
from gui import Window
from controller import controller
import warnings 
import tensorflow as tf 
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)



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


