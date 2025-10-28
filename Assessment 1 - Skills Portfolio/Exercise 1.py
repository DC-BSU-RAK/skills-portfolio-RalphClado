from tkinter import *
import random

score = 0
question_count = 0
difficulty = 1
operation = '+'
current_answer = 0

def displayMenu():
    global menu_frame
    menu_frame = Frame(root)
    menu_frame.pack()

    Label(menu_frame, text="Select Difficulty Level").pack()
    Button(menu_frame, text="Easy (1-digit)", command=lambda: startQuiz(1)).pack()
    Button(menu_frame, text="Moderate (2-digit)", command=lambda: startQuiz(2)).pack()
    Button(menu_frame, text="Hard (4-digit)", command=lambda: startQuiz(4)).pack()

def startQuiz(level):
    global difficulty, menu_frame
    difficulty = level
    menu_frame.destroy()
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
    global question_count, quiz_frame
    if question_count == 10:
        displayScore()
        return

    question_count += 1
    quiz_frame = Frame(root)
    quiz_frame.pack()

    problem = generateProblem()
    Label(quiz_frame, text=f"Question {question_count}: {problem}").pack()

    answer_entry = Entry(quiz_frame)
    answer_entry.pack()

    Button(quiz_frame, text="Submit", command=lambda: submitAnswer(answer_entry.get())).pack()

def submitAnswer(user_input):
    global quiz_frame
    checkAnswer(user_input)
    quiz_frame.destroy()
    nextQuestion()

def displayScore():
    global score, question_count
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

    result_frame = Frame(root)
    result_frame.pack()
    Label(result_frame, text=f"Your Score: {score}/100").pack()
    Label(result_frame, text=f"Grade: {grade}").pack()
    Button(result_frame, text="Play Again", command=lambda: restartQuiz(result_frame)).pack()

def restartQuiz(frame):
    global score, question_count
    score = 0
    question_count = 0
    frame.destroy()
    displayMenu()

root = Tk()
root.title("Arithmetic Quiz")
root.geometry("300x200")
displayMenu()
root.mainloop()
