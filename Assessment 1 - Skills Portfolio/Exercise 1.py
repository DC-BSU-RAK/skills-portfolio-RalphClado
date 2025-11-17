from tkinter import *
import random
import time

score = 0
question_count = 0
difficulty = 1
operation = '+'
current_answer = 0

P5_RED = "#e41e1e"
P5_BLACK = "#000000"
P5_WHITE = "#ffffff"
P5_GRAY = "#2c2c2c"
P5_LIGHT_GRAY = "#4a4a4a"

slide_pos = 0
slide_direction = 1
pulse_scale = 1.0
pulse_direction = 0.01

def animate_background():
    global slide_pos, slide_direction, pulse_scale, pulse_direction

    slide_pos += slide_direction
    if slide_pos > 20 or slide_pos < 0:
        slide_direction *= -1

    pulse_scale += pulse_direction
    if pulse_scale > 1.1 or pulse_scale < 0.9:
        pulse_direction *= -1

    canvas.delete("all")

    for i in range(-5, 15):
        x1 = (i * 30) + slide_pos
        y1 = 0
        x2 = x1 + 200
        y2 = 300
        canvas.create_line(x1, y1, x2, y2, fill=P5_RED, width=3)

    center_x = 150
    center_y = 100
    radius = 80 * pulse_scale
    canvas.create_oval(center_x - radius, center_y - radius, 
                      center_x + radius, center_y + radius, 
                      fill=P5_BLACK, outline="")
    
    root.after(50, animate_background)

def displayMenu():
    global menu_frame, canvas

    canvas = Canvas(root, bg=P5_BLACK, highlightthickness=0)
    canvas.place(x=0, y=0, width=300, height=200)

    animate_background()
    
    menu_frame = Frame(root, bg=P5_BLACK)
    menu_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    title_label = Label(menu_frame, text="SELECT DIFFICULTY", 
                       font=("Arial", 12, "bold"), 
                       fg=P5_WHITE, bg=P5_BLACK)
    title_label.pack(pady=10)

    buttons_data = [
        ("EASY (1-DIGIT)", 1),
        ("MODERATE (2-DIGIT)", 2),
        ("HARD (4-DIGIT)", 4)
    ]
    
    for text, level in buttons_data:
        btn = Button(menu_frame, text=text, 
                    font=("Arial", 10, "bold"),
                    fg=P5_WHITE, bg=P5_RED,
                    relief="flat", width=15, height=1,
                    command=lambda l=level: startQuiz(l))
        btn.pack(pady=5)

        def on_enter(e, button=btn):
            button.config(bg=P5_WHITE, fg=P5_RED)
        
        def on_leave(e, button=btn):
            button.config(bg=P5_RED, fg=P5_WHITE)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

def startQuiz(level):
    global difficulty, menu_frame, canvas
    difficulty = level

    for i in range(10):
        menu_frame.place(relx=0.5 + i*0.05, rely=0.5, anchor=CENTER)
        root.update()
        time.sleep(0.02)
    
    menu_frame.destroy()
    canvas.destroy()
    nextQuestion()

def generateProblem():
    global current_answer, operation
    digits = {1: (1, 9), 2: (10, 99), 4: (1000, 9999)}
    low, high = digits[difficulty]
    num1 = random.randint(low, high)
    num2 = random.randint(low, high)
    operation = random.choice(['+', '-'])
    if operation == '+':
        current_answer = num1 + num2
    else:
        current_answer = num1 - num2
    return f"{num1} {operation} {num2} ="

def checkAnswer(user_input):
    global score
    try:
        if int(user_input) == current_answer:
            score += 10
    except ValueError:
        pass

def nextQuestion():
    global question_count, quiz_frame, canvas
    
    if question_count == 10:
        displayScore()
        return

    question_count += 1

    quiz_frame = Frame(root, bg=P5_BLACK)
    quiz_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    quiz_frame.place(relx=1.5, rely=0.5, anchor=CENTER)
    for i in range(10):
        quiz_frame.place(relx=1.5 - i*0.1, rely=0.5, anchor=CENTER)
        root.update()
        time.sleep(0.02)

    problem = generateProblem()

    question_label = Label(quiz_frame, 
                          text=f"QUESTION {question_count}: {problem}", 
                          font=("Arial", 12, "bold"),
                          fg=P5_WHITE, bg=P5_BLACK)
    question_label.pack(pady=15)

    answer_entry = Entry(quiz_frame, 
                        font=("Arial", 12),
                        fg=P5_WHITE, bg=P5_GRAY,
                        insertbackground=P5_WHITE,
                        relief="flat", width=15)
    answer_entry.pack(pady=10)
    answer_entry.focus()

    submit_btn = Button(quiz_frame, text="SUBMIT", 
                       font=("Arial", 10, "bold"),
                       fg=P5_WHITE, bg=P5_RED,
                       relief="flat", width=12,
                       command=lambda: submitAnswer(answer_entry.get()))
    submit_btn.pack(pady=10)

    def on_enter(e):
        submit_btn.config(bg=P5_WHITE, fg=P5_RED)
    
    def on_leave(e):
        submit_btn.config(bg=P5_RED, fg=P5_WHITE)
        
    submit_btn.bind("<Enter>", on_enter)
    submit_btn.bind("<Leave>", on_leave)

    answer_entry.bind('<Return>', lambda event: submitAnswer(answer_entry.get()))

def submitAnswer(user_input):
    global quiz_frame

    for i in range(10):
        quiz_frame.place(relx=0.5 - i*0.05, rely=0.5, anchor=CENTER)
        root.update()
        time.sleep(0.02)
    
    checkAnswer(user_input)
    quiz_frame.destroy()
    nextQuestion()

def displayScore():
    global score, question_count, canvas

    canvas = Canvas(root, bg=P5_BLACK, highlightthickness=0)
    canvas.place(x=0, y=0, width=300, height=200)
    animate_background()
    
    grade = ''
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'

    result_frame = Frame(root, bg=P5_BLACK)
    result_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    result_frame.place(relx=-0.5, rely=0.5, anchor=CENTER)
    for i in range(10):
        result_frame.place(relx=-0.5 + i*0.1, rely=0.5, anchor=CENTER)
        root.update()
        time.sleep(0.02)

    score_label = Label(result_frame, 
                       text=f"SCORE: {score}/100", 
                       font=("Arial", 14, "bold"),
                       fg=P5_WHITE, bg=P5_BLACK)
    score_label.pack(pady=10)

    grade_label = Label(result_frame, 
                       text=f"GRADE: {grade}", 
                       font=("Arial", 18, "bold"),
                       fg=P5_RED, bg=P5_BLACK)
    grade_label.pack(pady=10)

    play_btn = Button(result_frame, text="PLAY AGAIN", 
                     font=("Arial", 10, "bold"),
                     fg=P5_WHITE, bg=P5_RED,
                     relief="flat", width=12,
                     command=lambda: restartQuiz(result_frame))
    play_btn.pack(pady=15)

    def on_enter(e):
        play_btn.config(bg=P5_WHITE, fg=P5_RED)
    
    def on_leave(e):
        play_btn.config(bg=P5_RED, fg=P5_WHITE)
        
    play_btn.bind("<Enter>", on_enter)
    play_btn.bind("<Leave>", on_leave)

def restartQuiz(frame):
    global score, question_count, canvas
    score = 0
    question_count = 0

    for i in range(10):
        frame.place(relx=0.5, rely=0.5 - i*0.05, anchor=CENTER)
        root.update()
        time.sleep(0.02)
    
    frame.destroy()
    canvas.destroy()
    displayMenu()

root = Tk()
root.title("PERSONA 5 ARITHMETIC QUIZ")
root.geometry("300x200")
root.configure(bg=P5_BLACK)
root.resizable(False, False)

try:
    root.iconbitmap("persona5_icon.ico")
except:
    pass

displayMenu()
root.mainloop()
