import cv2
import tkinter as tk

cam = cv2.VideoCapture(0)

# while True:
#     check, img = cam.read()
#     img = cv2.flip(img, 1)
#     #cv2.imshow('video', img)

#     key = cv2.waitKey(1)
#     if key == 27:
#         break

# cam.release()
# cv2.destroyAllWindows()

window = tk.Tk()
window.title("Prova GUI con tkinter")
window.iconbitmap(r'C:\Users\ga88m\Documents\GitHub\tkinterprova\vinyl.ico')
window.geometry("500x100")



#vid = cv2.VideoCapture(img)

# canvas = tk.Canvas(window, width= vid.get(cv2.CAP_PROP_FRAME_WIDTH), height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

top_frame = tk.Frame(window).pack()
bottom_frame = tk.Frame(window).pack(side="bottom")


label=tk.Label(bottom_frame, text="label", font=15, bg='white', fg='blue').pack(side=tk.TOP, fill=tk.BOTH)

btn1 = tk.Button(bottom_frame, text = "Button1", fg = "red").pack()

window.mainloop()

# import cv2

# def show_webcam(mirror=False):
#     cam = cv2.VideoCapture(0)
#     while True:
#         ret_val, img = cam.read()
#         if mirror: 
#             img = cv2.flip(img, 1)
#         # cv2.imshow('my webcam', img)
#         if cv2.waitKey(1) == 27: 
#             break  # esc to quit
#     cv2.destroyAllWindows()

# def main():
#     show_webcam(mirror=True)

# if __name__ == '__main__':
#     main()