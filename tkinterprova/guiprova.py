import tkinter 
import cv2
from PIL import Image, ImageTk
import time


class App:
    def __init__(self, video_source=0):
        self.appName = "CID camera v1.0"
        self.window = tkinter.Tk()
        self.window.title(self.appName)
        self.window.resizable(0,0)
        # self.window.wm_iconbitmap("cam.ico")
        self.window['bg']='black'
        self.video_source = video_source

        self.vid = myVideoCapture(self.video_source)
        self.label = tkinter.Label(self.window, text=self.appName, font=15, bg='blue', fg='white').pack(side=tkinter.TOP,fill=tkinter.BOTH)

        #create canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.window, width = self.vid.width, height = self.vid.height, bg='red')
        self.canvas.pack()




class myVideoCapture:
    def __init__(self, video_source=0):
        #open video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open this camera \n select another video source", video_source)

        #get video source width and wieght
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        
        def getFrame(self):
            if self.vid.isOpened():
                isTrue, frame = self.vid.read()
                if isTrue:
                    #if isture then current frame converted to rgb
                    return (isTrue, cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
                else:
                    return(isTrue, None)
            else: 
                return (isTrue, None)
        def __del__(self):
            if self.vid.isOpened():
                self.vid.release()


if __name__ =="__main__":
    App()


# window = tkinter.Tk()
# window.title("Provagab")

# top_frame = tkinter.Frame(window).pack()
# bottom_frame = tkinter.Frame(window).pack(side="bottom")

# btn1 = tkinter.Button(top_frame, text = "Button1", fg = "red").pack()

# window.mainloop()