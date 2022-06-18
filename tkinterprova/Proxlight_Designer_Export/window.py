from tkinter import *
import skimage.color
import skimage.io
from PIL import Image
import cv2

def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("1236x712")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 712,
    width = 1236,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    569.5, 333.5,
    image=background_img)


# #BUTTON PLAY
# img0 = PhotoImage(file = f"img0.png")
# b0 = Button(
#     image = img0,
#     borderwidth = 0,
#     highlightthickness = 0,
#     command = btn_clicked,
#     relief = "flat")

# b0.place(
#     x = 518, y = 598,
#     width = 186,
#     height = 205)



# #BUTTON STOP

# img1 = PhotoImage(file = f"img1.png")
# b1 = Button(
#     image = img1,
#     borderwidth = 0,
#     highlightthickness = 0,
#     command = btn_clicked,
#     relief = "flat")

# b1.place(
#     x = 712, y = 598,
#     width = 186,
#     height = 205)



# #BUTTON REC


# img2 = PhotoImage(file=f"img2.png", master=window)

# # img2 = skimage.io.imread('https://flyclipart.com/thumb2/button-png-172003.png')
# # img2 = skimage.color.rgba2rgb(img2)

# # img2=Image.open(r"C:\Users\ga88m\Documents\GitHub\tkinterprova\Proxlight_Designer_Export\img2.png").convert('RGBA')
# # ph = PhotoImage(img2)
# # label = Label(window, image=ph)
# # label.image=ph
# b2 = Button(
#     image = img2,
#     borderwidth = 0,
#     highlightthickness = 0,
#     command = btn_clicked,
#     relief = "flat")

# b2.place(
#     x = 315, y = 598,
#     width = 186,
#     height = 205)



#WEBCAM

#Lable to capture frames
label =Label(window)
label.grid(row=0, column=0)
cap= cv2.VideoCapture(0)

label.place(
    x = 212, y = 198,
    width = 700,
    height = 405
)

#Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)

show_frames()


window.resizable(False, False)
window.mainloop()
