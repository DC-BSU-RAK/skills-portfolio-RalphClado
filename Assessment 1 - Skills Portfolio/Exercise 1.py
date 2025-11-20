import tkinter as tk
from tkinter import ttk
import random
import time

class MathQuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz Game - Persona 5 Style")
        self.root.geometry("900x700")
        self.root.configure(bg='#000000')
        
        self.colors = {'bg': '#000000', 'primary': '#ff0000', 'accent': '#ffd700', 'text': '#ffffff', 'card_bg': '#1a1a1a'}
        self.difficulty = self.score = self.current_question = self.attempts = 0
        self.total_questions = 10
        self.current_problem = self.questions = None
        
        self.configure_styles()
        self.main_frame = ttk.Frame(self.root, style='Card.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.center_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        self.center_frame.pack(expand=True, fill=tk.BOTH)
        self.show_welcome_screen()
    
    def configure_styles(self):
        style = ttk.Style()
        style.configure('Card.TFrame', background=self.colors['card_bg'], relief='raised', borderwidth=2)
        style.configure('Center.TFrame', background=self.colors['card_bg'])
        style.configure('P5Button.TButton', background=self.colors['primary'], foreground=self.colors['text'],
                       borderwidth=0, font=('Arial', 12, 'bold'), padding=(30, 15))
        style.map('P5Button.TButton', background=[('active', self.colors['accent']), ('pressed', self.colors['accent'])],
                 foreground=[('active', self.colors['bg']), ('pressed', self.colors['bg'])])
    
    def clear_frame(self): [widget.destroy() for widget in self.center_frame.winfo_children()]
    
    def create_label(self, text, font_size=16, bold=False, color=None, pady=10):
        color = color or self.colors['text']
        font = ("Arial", font_size, "bold") if bold else ("Arial", font_size)
        label = tk.Label(self.center_frame, text=text, font=font, bg=self.colors['card_bg'], fg=color, justify=tk.CENTER)
        label.pack(pady=pady, fill=tk.X)
        if len(text) > 10: self.animate_typing(label, text)
        return label
    
    def create_button(self, text, command, style='P5Button.TButton', width=20, pady=10):
        frame = ttk.Frame(self.center_frame, style='Center.TFrame')
        frame.pack(pady=pady, fill=tk.X)
        button = ttk.Button(frame, text=text, command=command, style=style, width=width)
        button.pack()
        button.bind("<Enter>", lambda e: self.pulse_animation(button))
        return button
    
    def create_frame(self, fill=tk.X, pady=10, padx=50):
        frame = ttk.Frame(self.center_frame, style='Card.TFrame')
        frame.pack(pady=pady, padx=padx, fill=fill, expand=False)
        return frame
    
    def animate_typing(self, label, text):
        def type_effect(i=0):
            if i <= len(text):
                label.config(text=text[:i])
                if i < len(text): self.root.after(50, lambda: type_effect(i + 1))
        type_effect()
    
    def pulse_animation(self, widget):
        def pulse():
            for intensity in [1.0, 1.2, 1.0, 1.1, 1.0]:
                if widget.winfo_exists():
                    try: widget.config(bg=self.colors['accent'] if intensity > 1 else self.colors['primary'])
                    except: pass
                    self.root.update(); time.sleep(0.1)
        self.root.after(100, pulse)
    
    def show_welcome_screen(self):
        self.clear_frame()
        self.create_label("MATH QUIZ TIME", 32, True, self.colors['primary'], 40)
        self.create_label("Persona 5 Edition", 16, False, self.colors['accent'], 10)
        
        rules_frame = self.create_frame(pady=30, padx=100)
        for rule in ["ANSWER THE QUESTIONS", "EARN POINTS", "SHOW YOUR SKILLS", "BECOME A PHANTOM THIEF"]:
            tk.Label(rules_frame, text=f"○ {rule}", font=("Arial", 12), bg=self.colors['card_bg'], 
                    fg=self.colors['text']).pack(pady=5)
        
        self.create_label("ARE YOU READY TO BEGIN?", 18, True, self.colors['primary'], 30)
        self.create_button("START QUIZ", self.show_difficulty_menu, pady=20)
    
    def show_difficulty_menu(self):
        self.clear_frame()
        self.create_label("SELECT DIFFICULTY", 24, True, self.colors['primary'], 30)
        self.create_label("Choose your challenge level:", 14, False, self.colors['text'], 10)
        
        for i, (text, level) in enumerate([("★ EASY", "easy"), ("★★ MODERATE", "moderate"), ("★★★ ADVANCED", "advanced")]):
            button = self.create_button(text, lambda l=level: self.set_difficulty(l), width=30, pady=15)
            self.root.after(300 + i * 200, lambda b=button: self.pulse_animation(b))
    
    def set_difficulty(self, level):
        self.clear_frame()
        loading = self.create_label("PREPARING QUESTIONS...", 18, False, self.colors['primary'], 0)
        loading.pack(expand=True); self.pulse_animation(loading)
        self.root.after(1500, lambda: self.start_quiz(level))
    
    def start_quiz(self, level):
        self.difficulty, self.score, self.current_question, self.questions = level, 0, 0, []
        self.generate_questions(); self.show_next_question()
    
    def generate_questions(self):
        ranges = {"easy": (1, 9), "moderate": (10, 99), "advanced": (1000, 9999)}
        min_val, max_val = ranges.get(self.difficulty, (1, 9))
        
        for _ in range(self.total_questions):
            num1, num2 = random.randint(min_val, max_val), random.randint(min_val, max_val)
            operation = random.choice(['+', '-'])
            if operation == '+': answer = num1 + num2
            else: num1, num2 = max(num1, num2), min(num1, num2); answer = num1 - num2
            self.questions.append({'num1': num1, 'num2': num2, 'operation': operation, 'answer': answer})
    
    def show_next_question(self):
        if self.current_question >= self.total_questions: return self.displayResults()
        self.current_problem, self.attempts = self.questions[self.current_question], 0
        self.displayProblem()
    
    def displayProblem(self):
        self.clear_frame()
        header = self.create_frame(fill=tk.X, pady=10, padx=20)
        tk.Label(header, text=f"QUESTION {self.current_question + 1}/{self.total_questions}", 
                font=("Arial", 14, "bold"), bg=self.colors['card_bg'], fg=self.colors['primary']).pack(side=tk.LEFT)
        tk.Label(header, text=f"SCORE: {self.score}", font=("Arial", 14, "bold"), 
                bg=self.colors['card_bg'], fg=self.colors['accent']).pack(side=tk.RIGHT)
        
        problem_frame = self.create_frame(fill=tk.BOTH, pady=50, padx=50); problem_frame.pack(expand=True)
        problem_text = f"{self.current_problem['num1']} {self.current_problem['operation']} {self.current_problem['num2']} = ?"
        problem_label = tk.Label(problem_frame, text=problem_text, font=("Arial", 36, "bold"), 
                               bg=self.colors['card_bg'], fg=self.colors['text'])
        problem_label.pack(expand=True)
        
        answer_frame = self.create_frame(fill=tk.X, pady=20, padx=100)
        self.answer_var = tk.StringVar()
        entry = tk.Entry(answer_frame, textvariable=self.answer_var, font=("Arial", 24), bg=self.colors['bg'],
                        fg=self.colors['text'], justify=tk.CENTER, relief='solid', borderwidth=2)
        entry.pack(pady=20, fill=tk.X, ipady=10); entry.focus()
        
        self.create_button("SUBMIT ANSWER", self.checkAnswer, pady=10)
        self.root.bind('<Return>', lambda e: self.checkAnswer())
        self.root.after(200, lambda: self.pulse_animation(problem_label))
    
    def checkAnswer(self):
        try:
            user_answer = int(self.answer_var.get())
            if user_answer == self.current_problem['answer']: self.handle_answer(True)
            else: self.handle_answer(False)
        except ValueError: self.show_popup("Please enter a valid number!", "Invalid Input")
    
    def handle_answer(self, correct):
        if correct:
            points, message, color = (10, "PERFECT! +10 POINTS", self.colors['accent']) if self.attempts == 0 else (5, "CORRECT! +5 POINTS", self.colors['primary'])
            self.score += points; self.show_popup(message, "Result", color, True)
            self.current_question += 1; self.root.after(2000, self.show_next_question)
        else:
            self.attempts += 1
            if self.attempts < 2: self.show_popup("TRY AGAIN!", "Result", self.colors['primary'], False); self.answer_var.set("")
            else: self.show_popup(f"ANSWER: {self.current_problem['answer']}", "Result", self.colors['primary'], False, True)
    
    def show_popup(self, message, title, color=None, is_correct=False, final=False):
        color = color or self.colors['primary']
        popup = tk.Toplevel(self.root); popup.title(title); popup.configure(bg=self.colors['bg']); popup.geometry("400x200")
        popup.transient(self.root); popup.grab_set()
        popup.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 200; y = (self.root.winfo_screenheight() // 2) - 100
        popup.geometry(f"400x200+{x}+{y}")
        
        tk.Label(popup, text=message, font=("Arial", 16, "bold"), bg=self.colors['bg'], fg=color).pack(expand=True, pady=30)
        if not final and not is_correct:
            ttk.Button(popup, text="CONTINUE", command=popup.destroy, style='P5Button.TButton').pack(pady=10)
        if final: self.current_question += 1; self.root.after(2000, self.show_next_question)
    
    def displayResults(self):
        self.clear_frame()
        grade = "A+" if self.score >= 90 else "A" if self.score >= 80 else "B" if self.score >= 70 else "C" if self.score >= 60 else "D" if self.score >= 50 else "F"
        ranks = {'A+': 'PHANTOM THIEF LEGEND', 'A': 'EXPERT', 'B': 'SKILLED', 'C': 'APPRENTICE', 'D': 'BEGINNER', 'F': 'NEEDS TRAINING'}
        
        self.create_label(f"FINAL SCORE: {self.score}/100", 28, True, self.colors['accent'], 30)
        self.create_label(f"GRADE: {grade}", 24, False, self.colors['primary'], 20)
        self.create_label(f"RANK: {ranks.get(grade, 'UNRANKED')}", 20, False, self.colors['text'], 20)
        self.create_button("PLAY AGAIN", self.show_difficulty_menu, pady=20)
        self.create_button("EXIT", self.root.quit, style='P5Button.TButton', pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizGame(root)
    root.mainloop()
