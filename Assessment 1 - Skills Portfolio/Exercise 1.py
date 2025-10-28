from tkinter import *
root = Tk()
root.title("First App")
root.geometry("400x200")

l = Label(root, text="Hello !",
          fg="red",
          bg="#FFFFFF",
          font=('Roboto',25))
l.pack()

l = Label(root, text="My name is Ralph",
          fg="Blue",
          bg="#FFFFFF",
          font=('Roboto',25))
l.pack()

l2 = Label(root, text="\n I am studying in Bath Spa University Academic center RAK \n I am enrolled in BSC CC Year 2, Group - C",
           fg="#FFFFFF", bg="#000000", font=('Roboto',8))
l2.pack()

root.mainloop()


