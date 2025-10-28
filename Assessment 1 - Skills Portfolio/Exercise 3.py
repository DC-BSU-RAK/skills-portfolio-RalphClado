from tkinter import *
from tkinter import messagebox, simpledialog
import os

FILENAME = "studentMarks.txt"

def load_students():
    students = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 6:
                    sid, name, m1, m2, m3, exam = parts
                    coursework = (int(m1) + int(m2) + int(m3)) / 3
                    final = 0.7 * coursework + 0.3 * int(exam)
                    grade = get_grade(final)
                    students.append({
                        "id": sid, "name": name,
                        "coursework": coursework,
                        "exam": int(exam),
                        "final": final,
                        "grade": grade
                    })
    return students

def get_grade(mark):
    if mark >= 70: return "A"
    elif mark >= 60: return "B"
    elif mark >= 50: return "C"
    else: return "F"

def display_all():
    students = load_students()
    output.delete(1.0, END)
    for s in students:
        output.insert(END, f"{s['id']} - {s['name']} | CW: {s['coursework']:.1f} | Exam: {s['exam']} | Final: {s['final']:.1f} | Grade: {s['grade']}\n")
    avg = sum(s['final'] for s in students) / len(students) if students else 0
    output.insert(END, f"\nTotal Students: {len(students)} | Class Average: {avg:.1f}%")

def view_individual():
    sid = simpledialog.askstring("Student ID", "Enter student ID:")
    students = load_students()
    found = next((s for s in students if s['id'] == sid), None)
    output.delete(1.0, END)
    if found:
        output.insert(END, f"{found['id']} - {found['name']} | CW: {found['coursework']:.1f} | Exam: {found['exam']} | Final: {found['final']:.1f} | Grade: {found['grade']}")
    else:
        output.insert(END, "Student not found.")

def show_highest():
    students = load_students()
    top = max(students, key=lambda s: s['final'], default=None)
    output.delete(1.0, END)
    if top:
        output.insert(END, f"Highest: {top['id']} - {top['name']} | Final: {top['final']:.1f} | Grade: {top['grade']}")

def show_lowest():
    students = load_students()
    low = min(students, key=lambda s: s['final'], default=None)
    output.delete(1.0, END)
    if low:
        output.insert(END, f"Lowest: {low['id']} - {low['name']} | Final: {low['final']:.1f} | Grade: {low['grade']}")

def sort_records(order="asc"):
    students = load_students()
    students.sort(key=lambda s: s['final'], reverse=(order=="desc"))
    output.delete(1.0, END)
    for s in students:
        output.insert(END, f"{s['id']} - {s['name']} | Final: {s['final']:.1f} | Grade: {s['grade']}\n")

def add_student():
    sid = simpledialog.askstring("Student ID", "Enter student ID:")
    name = simpledialog.askstring("Name", "Enter student name:")
    m1 = simpledialog.askinteger("Mark 1", "Enter coursework mark 1:")
    m2 = simpledialog.askinteger("Mark 2", "Enter coursework mark 2:")
    m3 = simpledialog.askinteger("Mark 3", "Enter coursework mark 3:")
    exam = simpledialog.askinteger("Exam", "Enter exam mark:")
    with open(FILENAME, "a") as file:
        file.write(f"{sid},{name},{m1},{m2},{m3},{exam}\n")
    messagebox.showinfo("Success", "Student added.")

def delete_student():
    sid = simpledialog.askstring("Student ID", "Enter student ID to delete:")
    students = load_students()
    updated = [s for s in students if s['id'] != sid]
    if len(updated) < len(students):
        with open(FILENAME, "w") as file:
            for s in updated:
                file.write(f"{s['id']},{s['name']},{int(s['coursework'])},{int(s['coursework'])},{int(s['coursework'])},{s['exam']}\n")
        messagebox.showinfo("Deleted", "Student record deleted.")
    else:
        messagebox.showwarning("Not Found", "Student ID not found.")

def update_student():
    sid = simpledialog.askstring("Student ID", "Enter student ID to update:")
    students = load_students()
    for s in students:
        if s['id'] == sid:
            field = simpledialog.askstring("Field", "Enter field to update (name, m1, m2, m3, exam):")
            if field in ["name", "m1", "m2", "m3", "exam"]:
                new_val = simpledialog.askstring("New Value", f"Enter new value for {field}:")
                index = students.index(s)
                with open(FILENAME, "r") as file:
                    lines = file.readlines()
                parts = lines[index].strip().split(",")
                if field == "name":
                    parts[1] = new_val
                else:
                    parts[int(field[1])] = new_val
                lines[index] = ",".join(parts) + "\n"
                with open(FILENAME, "w") as file:
                    file.writelines(lines)
                messagebox.showinfo("Updated", "Student record updated.")
                return
    messagebox.showwarning("Not Found", "Student ID not found.")

root = Tk()
root.title("Student Manager")
root.geometry("600x400")

frame = Frame(root)
frame.pack()

Button(frame, text="View All", command=display_all).grid(row=0, column=0)
Button(frame, text="View Individual", command=view_individual).grid(row=0, column=1)
Button(frame, text="Highest Mark", command=show_highest).grid(row=0, column=2)
Button(frame, text="Lowest Mark", command=show_lowest).grid(row=0, column=3)
Button(frame, text="Sort Asc", command=lambda: sort_records("asc")).grid(row=1, column=0)
Button(frame, text="Sort Desc", command=lambda: sort_records("desc")).grid(row=1, column=1)
Button(frame, text="Add Student", command=add_student).grid(row=1, column=2)
Button(frame, text="Delete Student", command=delete_student).grid(row=1, column=3)
Button(frame, text="Update Student", command=update_student).grid(row=2, column=1)

output = Text(root, wrap=WORD)
output.pack(expand=True, fill=BOTH)

root.mainloop()
