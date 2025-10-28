from tkinter import *
import random

def load_jokes():
    with open("randomJokes.txt", "r") as file:
        lines = file.readlines()
    jokes = [line.strip().split("?") for line in lines if "?" in line]
    return jokes

def show_joke():
    global current_joke
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0] + "?")
    punchline_label.config(text="") 

def show_punchline():
    if current_joke:
        punchline_label.config(text=current_joke[1])

def quit_app():
    root.destroy()

root = Tk()
root.title("Alexa Joke Assistant")
root.geometry("400x200")

jokes = load_jokes()
current_joke = None

setup_label = Label(root, text="", font=("Arial", 12), wraplength=380)
setup_label.pack(pady=10)

punchline_label = Label(root, text="", font=("Arial", 10), fg="blue", wraplength=380)
punchline_label.pack(pady=5)

Button(root, text="Alexa tell me a Joke", command=show_joke).pack(pady=5)
Button(root, text="Show Punchline", command=show_punchline).pack(pady=5)
Button(root, text="Next Joke", command=show_joke).pack(pady=5)
Button(root, text="Quit", command=quit_app).pack(pady=5)

root.mainloop()
