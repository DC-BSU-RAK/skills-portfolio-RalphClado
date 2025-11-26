from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import os

FILENAME = "studentMarks.txt"

def load_students():
    students = []
    if not os.path.exists(FILENAME):
        return students
        
    try:
        with open(FILENAME, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 6:
                    sid, name, m1, m2, m3, exam = parts
                    
                    try:
                        coursework = (float(m1) + float(m2) + float(m3)) / 3
                        final = 0.7 * coursework + 0.3 * float(exam)
                        grade = get_grade(final)
                        students.append({
                            "id": sid, "name": name,
                            "coursework": coursework,
                            "exam": float(exam),
                            "final": final,
                            "grade": grade
                        })
                    except ValueError:
                        print(f"Skipping invalid data: {line}")
                        continue
    except Exception as e:
        messagebox.showerror("Error", f"Error loading students: {str(e)}")
    
    return students

def get_grade(mark):
    if mark >= 70: return "A"
    elif mark >= 60: return "B"
    elif mark >= 50: return "C"
    else: return "F"

def display_all():
    try:
        students = load_students()
        output.delete(1.0, END)
        if not students:
            output.insert(END, "No student records found.")
            return
            
        for s in students:
            output.insert(END, f"{s['id']} - {s['name']} | CW: {s['coursework']:.1f} | Exam: {s['exam']} | Final: {s['final']:.1f} | Grade: {s['grade']}\n")
        avg = sum(s['final'] for s in students) / len(students) if students else 0
        output.insert(END, f"\nTotal Students: {len(students)} | Class Average: {avg:.1f}%")
    except Exception as e:
        messagebox.showerror("Error", f"Error displaying students: {str(e)}")

def view_individual():
    try:
        sid = simpledialog.askstring("Student ID", "Enter student ID:")
        if not sid:
            return
            
        students = load_students()
        found = next((s for s in students if s['id'] == sid), None)
        output.delete(1.0, END)
        if found:
            output.insert(END, f"{found['id']} - {found['name']} | CW: {found['coursework']:.1f} | Exam: {found['exam']} | Final: {found['final']:.1f} | Grade: {found['grade']}")
        else:
            output.insert(END, "Student not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Error viewing student: {str(e)}")

def show_highest():
    try:
        students = load_students()
        if not students:
            output.delete(1.0, END)
            output.insert(END, "No student records found.")
            return
            
        top = max(students, key=lambda s: s['final'])
        output.delete(1.0, END)
        output.insert(END, f"Highest: {top['id']} - {top['name']} | Final: {top['final']:.1f} | Grade: {top['grade']}")
    except Exception as e:
        messagebox.showerror("Error", f"Error finding highest mark: {str(e)}")

def show_lowest():
    try:
        students = load_students()
        if not students:
            output.delete(1.0, END)
            output.insert(END, "No student records found.")
            return
            
        low = min(students, key=lambda s: s['final'])
        output.delete(1.0, END)
        output.insert(END, f"Lowest: {low['id']} - {low['name']} | Final: {low['final']:.1f} | Grade: {low['grade']}")
    except Exception as e:
        messagebox.showerror("Error", f"Error finding lowest mark: {str(e)}")

def sort_records(order="asc"):
    try:
        students = load_students()
        if not students:
            output.delete(1.0, END)
            output.insert(END, "No student records found.")
            return
            
        students.sort(key=lambda s: s['final'], reverse=(order=="desc"))
        output.delete(1.0, END)
        for s in students:
            output.insert(END, f"{s['id']} - {s['name']} | Final: {s['final']:.1f} | Grade: {s['grade']}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Error sorting records: {str(e)}")

def add_student():
    try:
        sid = simpledialog.askstring("Student ID", "Enter student ID:")
        if not sid:
            return
            
        name = simpledialog.askstring("Name", "Enter student name:")
        if not name:
            return
            
        m1 = simpledialog.askinteger("Mark 1", "Enter coursework mark 1 (0-100):")
        if m1 is None or m1 < 0 or m1 > 100:
            messagebox.showerror("Error", "Invalid mark 1. Must be between 0-100.")
            return
            
        m2 = simpledialog.askinteger("Mark 2", "Enter coursework mark 2 (0-100):")
        if m2 is None or m2 < 0 or m2 > 100:
            messagebox.showerror("Error", "Invalid mark 2. Must be between 0-100.")
            return
            
        m3 = simpledialog.askinteger("Mark 3", "Enter coursework mark 3 (0-100):")
        if m3 is None or m3 < 0 or m3 > 100:
            messagebox.showerror("Error", "Invalid mark 3. Must be between 0-100.")
            return
            
        exam = simpledialog.askinteger("Exam", "Enter exam mark (0-100):")
        if exam is None or exam < 0 or exam > 100:
            messagebox.showerror("Error", "Invalid exam mark. Must be between 0-100.")
            return

        with open(FILENAME, "a") as file:
            file.write(f"{sid},{name},{m1},{m2},{m3},{exam}\n")
            
        messagebox.showinfo("Success", "Student added successfully!")
        display_all()
    except Exception as e:
        messagebox.showerror("Error", f"Error adding student: {str(e)}")

def delete_student():
    try:
        sid = simpledialog.askstring("Student ID", "Enter student ID to delete:")
        if not sid:
            return
            
        students = load_students()
        updated = [s for s in students if s['id'] != sid]
        
        if len(updated) < len(students):
            with open(FILENAME, "w") as file:
                for s in updated:
                    file.write(f"{s['id']},{s['name']},{int(s['coursework'])},{int(s['coursework'])},{int(s['coursework'])},{int(s['exam'])}\n")
            messagebox.showinfo("Deleted", "Student record deleted.")
            display_all()
        else:
            messagebox.showwarning("Not Found", "Student ID not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting student: {str(e)}")

def update_student():
    try:
        sid = simpledialog.askstring("Student ID", "Enter student ID to update:")
        if not sid:
            return
            
        students = load_students()
        student_index = None
        student_data = None
        
        for i, s in enumerate(students):
            if s['id'] == sid:
                student_index = i
                student_data = s
                break
        
        if student_index is None:
            messagebox.showwarning("Not Found", "Student ID not found.")
            return

        field = simpledialog.askstring("Field", "Enter field to update (name, m1, m2, m3, exam):")
        if not field or field not in ["name", "m1", "m2", "m3", "exam"]:
            messagebox.showwarning("Invalid", "Invalid field specified.")
            return

        if field == "name":
            new_val = simpledialog.askstring("New Value", f"Enter new value for {field}:")
            if not new_val:
                return
        else:
            new_val = simpledialog.askinteger("New Value", f"Enter new value for {field} (0-100):")
            if new_val is None or new_val < 0 or new_val > 100:
                messagebox.showerror("Error", "Invalid mark. Must be between 0-100.")
                return
            new_val = str(new_val)

        with open(FILENAME, "r") as file:
            lines = file.readlines()

        if student_index < len(lines):
            parts = lines[student_index].strip().split(",")
            if field == "name":
                parts[1] = new_val
            elif field == "m1":
                parts[2] = new_val
            elif field == "m2":
                parts[3] = new_val
            elif field == "m3":
                parts[4] = new_val
            elif field == "exam":
                parts[5] = new_val
            
            lines[student_index] = ",".join(parts) + "\n"
            
            with open(FILENAME, "w") as file:
                file.writelines(lines)
            
            messagebox.showinfo("Updated", "Student record updated successfully!")
            display_all()
    except Exception as e:
        messagebox.showerror("Error", f"Error updating student: {str(e)}")

def search_student():
    try:
        search_term = simpledialog.askstring("Search", "Enter student ID or name to search:")
        if not search_term:
            return
            
        students = load_students()
        output.delete(1.0, END)
        found = False
        
        for s in students:
            if search_term.lower() in s['id'].lower() or search_term.lower() in s['name'].lower():
                output.insert(END, f"{s['id']} - {s['name']} | CW: {s['coursework']:.1f} | Exam: {s['exam']} | Final: {s['final']:.1f} | Grade: {s['grade']}\n")
                found = True
        
        if not found:
            output.insert(END, "No matching students found.")
    except Exception as e:
        messagebox.showerror("Error", f"Error searching students: {str(e)}")

def show_statistics():
    try:
        students = load_students()
        if not students:
            messagebox.showinfo("Statistics", "No student data available.")
            return
            
        total_students = len(students)
        avg_final = sum(s['final'] for s in students) / total_students
        grades = {'A': 0, 'B': 0, 'C': 0, 'F': 0}
        
        for s in students:
            grades[s['grade']] += 1
        
        stats_text = f"Total Students: {total_students}\n"
        stats_text += f"Average Final Score: {avg_final:.1f}%\n\n"
        stats_text += "Grade Distribution:\n"
        stats_text += f"A: {grades['A']} students\n"
        stats_text += f"B: {grades['B']} students\n"
        stats_text += f"C: {grades['C']} students\n"
        stats_text += f"F: {grades['F']} students"
        
        messagebox.showinfo("Class Statistics", stats_text)
    except Exception as e:
        messagebox.showerror("Error", f"Error calculating statistics: {str(e)}")

def clear_data():
    try:
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all student data?"):
            if os.path.exists(FILENAME):
                os.remove(FILENAME)
            output.delete(1.0, END)
            output.insert(END, "All student data cleared.")
    except Exception as e:
        messagebox.showerror("Error", f"Error clearing data: {str(e)}")

root = Tk()
root.title("Student Management System")
root.geometry("750x550")

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

button_frame = Frame(main_frame)
button_frame.pack(fill=X, pady=5)

Button(button_frame, text="View All Students", command=display_all, width=15).grid(row=0, column=0, padx=2, pady=2)
Button(button_frame, text="View Individual", command=view_individual, width=15).grid(row=0, column=1, padx=2, pady=2)
Button(button_frame, text="Highest Mark", command=show_highest, width=15).grid(row=0, column=2, padx=2, pady=2)
Button(button_frame, text="Lowest Mark", command=show_lowest, width=15).grid(row=0, column=3, padx=2, pady=2)
Button(button_frame, text="Sort Ascending", command=lambda: sort_records("asc"), width=15).grid(row=1, column=0, padx=2, pady=2)
Button(button_frame, text="Sort Descending", command=lambda: sort_records("desc"), width=15).grid(row=1, column=1, padx=2, pady=2)
Button(button_frame, text="Add Student", command=add_student, width=15).grid(row=1, column=2, padx=2, pady=2)
Button(button_frame, text="Delete Student", command=delete_student, width=15).grid(row=1, column=3, padx=2, pady=2)
Button(button_frame, text="Update Student", command=update_student, width=15).grid(row=2, column=0, padx=2, pady=2)
Button(button_frame, text="Search Student", command=search_student, width=15).grid(row=2, column=1, padx=2, pady=2)
Button(button_frame, text="Statistics", command=show_statistics, width=15).grid(row=2, column=2, padx=2, pady=2)
Button(button_frame, text="Clear All Data", command=clear_data, width=15, bg="#ff6b6b").grid(row=2, column=3, padx=2, pady=2)

output_frame = Frame(main_frame)
output_frame.pack(fill=BOTH, expand=True, pady=5)

scrollbar = Scrollbar(output_frame)
scrollbar.pack(side=RIGHT, fill=Y)

output = Text(output_frame, wrap=WORD, yscrollcommand=scrollbar.set, font=("Courier", 10))
output.pack(fill=BOTH, expand=True)
scrollbar.config(command=output.yview)

status_frame = Frame(main_frame)
status_frame.pack(fill=X, pady=5)

status_label = Label(status_frame, text="Ready - Student Management System", relief=SUNKEN, anchor=W)
status_label.pack(fill=X)

display_all()

root.mainloop()
