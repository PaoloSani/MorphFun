from queue import Queue
import threading
from PYQT_GUI  import useGUI

def main():
    command_que = Queue()
    data_que = Queue()
    # print(type(command_que))
    gui_thread = threading.Thread(target= useGUI, args=(command_que, data_que))
    gui_thread.start()

    while True:
        if ( data_que.not_empty):
            message = data_que.get()
            print(message)
        elif command_que.not_empty:
            message = command_que.get()
            print(message)

if __name__ == '__main__':
    main()
