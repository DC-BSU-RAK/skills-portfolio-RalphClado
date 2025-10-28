from tkinter import *

main = Tk()
main.title('Using pack()')

Button(main, text="A").pack(side=LEFT, expand=YES, fill=Y)
Button(main, text="B").pack(side=TOP, expand=YES, fill=BOTH)
Button(main, text="C").pack(side=RIGHT, expand=YES, fill=Y)
Button(main, text="D").pack(side=BOTTOM, expand=NO, fill=X)

main.mainloop()
