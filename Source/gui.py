#imports
from cProfile import label
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
import cv2
import mediapipe as mp
import numpy as np

from utils import CONFIG_PATH, load_config


#
mp_holistic = mp.solutions.holistic

#
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    return results

#
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, lh, rh])


#webcam thread
class Thread(QtCore.QThread):

    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    #initialization
    def __init__(self, data_queue, parent=None):
        
        self.queue = data_queue
        super(Thread, self).__init__(parent=parent)
          
    
    def run(self):

        sequence_length = 30
        sequence = []
        cap = cv2.VideoCapture(0)
        counter = 0
        config = load_config(CONFIG_PATH)
        boost = config['pose_estimation']['latency_factor']
       
        # Set mediapipe model 
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

            while cap.isOpened():
                #read feed
                ret, frame = cap.read()

                if ret:
                
                    # Make detections
                    results = mediapipe_detection(frame, holistic)
                                
                    # 2. Prediction logic
                    keypoints = extract_keypoints(results)
                    sequence.append(keypoints)
                    
                    sequence = sequence[-sequence_length:]
                    
                    if len(sequence) == sequence_length:
                        if counter == 30*boost:
                            self.queue.put(sequence)
                            counter = 0
                        else :
                            counter += 1

                    #image show for window
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    rgbImage = rgbImage[5:463, 80:560]                              #crop
                    rgbImage = cv2.flip(rgbImage,1)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)
                    # self.queue.put('a')

#window
class Window(QDialog):

    #initialization
    def __init__(self, cmd_queue, data_queue):
        super().__init__()

        self.title = "MorphFun"
        self.left=350
        self.top=180
        self.width=1280
        self.height=720
        self.iconName = "./Source/images/music-notes.ico"
        self.paused = False
        self.isRecording = False

        self.InitWindow(cmd_queue, data_queue)

    def closeEvent(self, event):
        # report_session()
        from pynput.keyboard import Key, Controller
        mykeyboard = Controller()
        mykeyboard.press(Key.esc)

    #function for webcam implementation
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    #communication button
    def sendMessageAtClick(self, cmd_queue, message ):
        cmd_queue.put(message)
        # print(message)
        # print(cmd_queue) 

    #play pause button
    def play_pause(self, cmd_queue):
        

        if self.paused:
            self.play_btn.setStyleSheet('QPushButton'
                                        '{'
                                        'background-image: url(./Source/images/playbutton.png);'
                                        'background-repeat: no-repeat;'
                                        'border: none;'
                                        
                                        '}'
                                        'QPushButton::pressed'
                                        '{'
                                        'background-image: url(./Source/images/playbutton_pressed.png);'
                                        '}'
                                        )
            self.paused = False
            self.sendMessageAtClick(cmd_queue, 'Play')
        else:   
            self.play_btn.setStyleSheet('QPushButton'
                                        '{'
                                        'background-image: url(./Source/images/stopbutton.png);'
                                        'background-repeat: no-repeat;'
                                        'border: none;'
                                        
                                        '}'
                                        'QPushButton::pressed'
                                        '{'
                                        'background-image: url(./Source/images/stopbutton_pressed.png);'
                                        '}'
                                        )   
            self.paused = True
            self.sendMessageAtClick(cmd_queue, 'Pause')

    #play pause button
    def recording(self, cmd_queue):
        if self.isRecording:
            self.rec_btn.setStyleSheet('QPushButton'
                                        '{'
                                        'background-image: url(./Source/images/recbutton.png);'
                                        'background-repeat: no-repeat;'
                                        'border: none;'
                                        
                                        '}'
                                        'QPushButton::pressed'
                                        '{'
                                        'background-image: url(./Source/images/recbutton_pressed.png);'
                                        '}'
                                        )
            self.play_btn.setStyleSheet('QPushButton'
                                        '{'
                                        'background-image: url(./Source/images/playbutton.png);'
                                        'background-repeat: no-repeat;'
                                        'border: none;'
                                        
                                        '}'
                                        'QPushButton::pressed'
                                        '{'
                                        'background-image: url(./Source/images/playbutton_pressed.png);'
                                        '}'
                                        )
            self.paused = False
            self.isRecording = False
            self.sendMessageAtClick(cmd_queue, 'Rec')
        else:   
            self.rec_btn.setStyleSheet('QPushButton'
                                        '{'
                                        'background-image: url(./Source/images/recbutton_on.png);'
                                        'background-repeat: no-repeat;'
                                        'border: none;'
                                        
                                        '}'
                                        'QPushButton::pressed'
                                        '{'
                                        'background-image: url(./Source/images/recbutton_pressed.png);'
                                        '}'
                                        )   
            self.isRecording = True
            self.sendMessageAtClick(cmd_queue, 'Rec')

    #initi function
    def InitWindow(self, cmd_queue, data_queue):
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        #label containing background image
        vbox = QVBoxLayout()
        labelImage = QLabel(self)
        pixmap = QPixmap("./Source/images/background.png")
        labelImage.setPixmap(pixmap)
        vbox.addWidget(labelImage)
       
        #label for webcam
        self.label = QLabel(self)
        self.label.move(61,67)
        self.label.resize(495, 470)
        
        self.label.setStyleSheet("border :2px solid #fcd462;"
                                "border-top-left-radius :5px;"
                                "border-top-right-radius : 5px; "
                                "border-bottom-left-radius : 5px; "
                                "border-bottom-right-radius : 5px")
        #webcam
        th = Thread(data_queue)
        th.changePixmap.connect(self.setImage)
        th.start()
        
        #button rec
        self.rec_btn = QtWidgets.QPushButton(self)
        
        self.rec_btn.setGeometry(93, 577, 123, 100)
        self.rec_btn.setStyleSheet('QPushButton'
                                   '{'
                                   'background-image: url(./Source/images/recbutton.png);'
                                   'background-repeat: no-repeat;'
                                   'border: none;'
                                   
                                   '}'
                                   'QPushButton::pressed'
                                   '{'
                                   'background-image: url(./Source/images/recbutton_pressed.png);'
                                   '}'
                                   )
        self.rec_btn.clicked.connect(lambda: self.recording(cmd_queue))      


        #button play
        self.play_btn = QtWidgets.QPushButton(self)
        
        self.play_btn.setGeometry(243, 576, 123, 88)
        self.play_btn.setStyleSheet('QPushButton'
                                   '{'
                                   'background-image: url(./Source/images/playbutton.png);'
                                   'background-repeat: no-repeat;'
                                   'border: none;'
                                   
                                   '}'
                                   'QPushButton::pressed'
                                   '{'
                                   'background-image: url(./Source/images/playbutton_pressed.png);'
                                   '}'
                                   )
        self.play_btn.clicked.connect(lambda: self.play_pause(cmd_queue))     
       
        #button clear
        self.clear_btn = QtWidgets.QPushButton(self)
        
        self.clear_btn.setGeometry(393, 576, 123, 88)
        self.clear_btn.setStyleSheet('QPushButton'
                                   '{'
                                   'background-image: url(./Source/images/clearbutton.png);'
                                   'background-repeat: no-repeat;'
                                   'border: none;'
                                   
                                   '}'
                                   'QPushButton::pressed'
                                   '{'
                                   'background-image: url(./Source/images/clearbutton_pressed.png);'
                                   '}'
                                   )    
        self.clear_btn.clicked.connect(lambda: self.sendMessageAtClick(cmd_queue, 'Clear'))


        self.show()
        return()

    def exit_app(self):
        print("Shortcut pressed") #verification of shortcut press
        self.close()

