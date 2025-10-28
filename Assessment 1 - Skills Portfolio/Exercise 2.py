from tkinter import *
import tkinter

root = Tk()
Label(root, text="Check Buttons to select multiple options").pack(anchor = W)

C1 = Checkbutton(root, text = "Gaming")
C1.pack(anchor = W)

C2 = Checkbutton(root, text = "Video Editing")
C2.pack(anchor = W)

C3 = Checkbutton(root, text = "Web Development")
C3.pack(anchor = W)

Label(root, text="Radio Buttons to select one option from multiple options").pack(anchor = W)

R1 = Radiobutton(root, text="Cooking", value=1)
R1.pack(anchor = W)

R2 = Radiobutton(root, text="Full Stack Developer", value=2)
R2.pack(anchor = W)

R3 = Radiobutton(root, text="Game Designer", value=3)
R3.pack(anchor = W)

root.mainloop()
