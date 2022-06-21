# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2

# Create an instance of TKinter Window or frame
win = Tk()

win.iconbitmap("./GUI_Tkinter/images/music-notes.ico")
win.title("MorphFun")
win.geometry("1280x720")

win.configure(bg = "#ffffff")
canvas = Canvas(
    win,
    bg = "#ffffff",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"./GUI_Tkinter/images/background.png")
background = canvas.create_image(
    640, 360,
    image=background_img)


# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=0, column=0)
cap= cv2.VideoCapture(0)

label.place(
  x=308, y=302, anchor=CENTER
)

#rec button
rec_image= (Image.open("./GUI_Tkinter/images/recbutton.png"))
rec_image= rec_image.resize((105,60), Image.ANTIALIAS)
rec_image= ImageTk.PhotoImage(rec_image)

btn_rec = Button(win, 
                 image = rec_image,
                 bd = 0, 
                 borderwidth=0, 
                 activebackground='#fff6b4',  
                 highlightthickness = 0, 
                 relief = "flat")
btn_rec.pack()
btn_rec.place(
  x=140,y=618, anchor=CENTER
)

#play/stop button
paused = True
 
def play() :
  global paused
  print("start of function", paused)
  if paused:
      btn_play.config(image=stop_image)
      paused = False
      print("inside if function", paused)
  else:
      btn_play.config(image=play_image)
      paused = True
      print("inside if function", paused)
  print('Play button has been clicked.')

def stop():
    global paused
    print("button stop")
    if not paused:
        btn_play.config(image=play_image)
        paused = True

play_image= (Image.open("./GUI_Tkinter/images/playbutton.png"))
play_image= play_image.resize((105,60), Image.ANTIALIAS)
play_image= ImageTk.PhotoImage(play_image)

stop_image= (Image.open("./GUI_Tkinter/images/stopbutton.png"))
stop_image= stop_image.resize((105,60), Image.ANTIALIAS)
stop_image= ImageTk.PhotoImage(stop_image)

btn_play = Button(win, 
                  image = play_image,
                  bd = 0, 
                  borderwidth=0, 
                  activebackground='#fff6b4', 
                  command = play, 
                  highlightthickness = 0, 
                  relief = "flat")
btn_play.pack()
btn_play.place(
  x=305,y=618, anchor=CENTER
)

#clear button
clear_image= (Image.open("./GUI_Tkinter/images/clearbutton.png"))
clear_image= clear_image.resize((105,60), Image.ANTIALIAS)
clear_image= ImageTk.PhotoImage(clear_image)

btn_clear = Button(win, 
                  image = clear_image,
                  bd = 0, 
                  borderwidth=0, 
                  activebackground='#fff6b4', 
                  highlightthickness = 0, 
                  relief = "flat")
btn_clear.pack()
btn_clear.place(
  x=470,y=618, anchor=CENTER
)

# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   cv2image = cv2.flip(cv2image,1) 
   #crop                                                            (img dim = 640x480)
   cv2image = cv2image[5:463, 80:560]
   img = Image.fromarray(cv2image)  
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)


show_frames()
win.mainloop()