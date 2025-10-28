from tkinter import *

root = Tk()
root.title("Find & Replace")
root.geometry("400x200")

Label(root, text="Find:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
Entry(root).grid(row=0, column=1, padx=5, pady=5)
Button(root, text="Find").grid(row=0, column=2, padx=5, pady=5)
Button(root, text="Find All").grid(row=0, column=3, padx=5, pady=5)

Label(root, text="Replace:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
Entry(root).grid(row=1, column=1, padx=5, pady=5)
Button(root, text="Replace").grid(row=1, column=2, padx=5, pady=5)
Button(root, text="Replace All").grid(row=1, column=3, padx=5, pady=5)

Checkbutton(root, text="Match whole word only").grid(row=2, column=0, columnspan=2, sticky=W, padx=5)
Checkbutton(root, text="Match Case").grid(row=3, column=0, columnspan=2, sticky=W, padx=5)
Checkbutton(root, text="Wrap around").grid(row=4, column=0, columnspan=2, sticky=W, padx=5)

Label(root, text="Direction:").grid(row=2, column=2, sticky=W, padx=5)
Radiobutton(root, text="Up", value=1).grid(row=3, column=2, sticky=W, padx=5)
Radiobutton(root, text="Down", value=2).grid(row=4, column=2, sticky=W, padx=5)

root.mainloop()

