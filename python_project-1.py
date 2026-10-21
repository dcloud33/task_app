import json
import sqlite3
import tkinter as tk
from tkinter import messagebox        
    
def calculate_progress(selected_task):
    completed_count = 0
    
    for subtask in selected_task["subtasks"]:
        if subtask["status"] == "Completed":
            completed_count += 1
    
    total_subtasks = len(selected_task["subtasks"])
    
    if total_subtasks > 0:
        percentage = completed_count / total_subtasks * 100
    else:
        percentage = 0
        
    return percentage




def update_subtask_status(selected_task):
    for index, subtask in enumerate(selected_task["subtasks"], start=1):
        print(f"{index}. {subtask['name']} - {subtask['status']}")
    
        
    while True:
        try:
            subtasks_number = int(input("Enter a subtask number: "))
        except ValueError:
            print("That is not a number.")
            continue
    
        subtasks_index = subtasks_number - 1
    
        if subtasks_index in range(0, len(selected_task["subtasks"])):
            selected_subtask = selected_task["subtasks"][subtasks_index]
            break
        
        print("Number not in range")
        continue
    
    status_value = ["Not Started", "In Progress", "Completed"]
    

    while True:
        print("Update status with Not Started, In Progress, or Completed")
        new_status = input("Enter a status: ")
        
        if new_status not in status_value:
            print("Invalid status")
            continue
        
        selected_subtask["status"] = new_status
        print(selected_subtask["status"])
        break
    
def select_task(tasks):
    if not tasks:
        print("Task list is empty.")
        return

    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task['name']}")    
          
    while True:
        try:
            tasks_number = int(input("Enter a task number: "))
        except ValueError:
            print("That is not a number.")
            continue
    
        tasks_index = tasks_number - 1
    
        if tasks_index in range(0, len(tasks)):
            selected_task = tasks[tasks_index]
            return selected_task
        
        print("Number not in range")
        continue
    

    

def initialize_database():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS "
        "tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL)"
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS subtasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
        """
    )

    connection.commit()
    connection.close()

def create_task():
    while True:
        task_name = input("Enter task name: ").strip()
        if task_name == "":
            print("task name cannot be empty")
            continue
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO tasks (name) VALUES (?)", (task_name,))
        
        connection.commit()
        connection.close()
        break

def add_subtasks():
    while True:
        try:
            task_id = int(input("Enter task number: "))
        except ValueError:
            print("Task number not an integer")
            continue
        if task_id <= 0:
            print("Task number not in range")
            continue
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        
        cursor.execute("SELECT id FROM tasks WHERE id=?", (task_id,))
        task = cursor.fetchone()
        
        if task is None:
            print("Task not found.")
            connection.close()
            continue
        break
    
    while True:
        
        subtask_name = input("Enter a subtask or 'done' to finish: ").strip()
        
        if subtask_name.lower() == "done":
            break
        
        cursor.execute("INSERT INTO subtasks (task_id, name, status) VALUES (?, ?, ?)", (task_id, subtask_name, "Not Started"))
        
    connection.commit()
    connection.close()
        
        
            
        

def display_tasks():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, name FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        cursor.execute("SELECT name, status FROM subtasks WHERE task_id=?", (task[0], ))
        subtasks = cursor.fetchall()
        print(f"{task[0]}. {task[1]}")
        if subtasks == []:
            print("   No subtasks.")
            continue
        for subtask in subtasks:
            print(f"   - {subtask[0]} ({subtask[1]})")
        
    connection.close()


def update_subtask_status():
    while True:
        try:
            task_id = int(input("Enter task number: "))
        except ValueError:
            print("Task number not an integer")
            continue
        if task_id <= 0:
            print("Task number not in range")
            continue
        
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        
        if task is None:
            print("Task not found.")
            connection.close()
            continue
        break
    cursor.execute("SELECT id, name, status FROM subtasks WHERE task_id = ?",(task_id,))

    subtasks = cursor.fetchall()
    
    if not subtasks:
        print("No subtasks found.")
        connection.close()
        return
    for subtask in subtasks:
        print(f"{subtask[0]}. {subtask[1]} - {subtask[2]}")
        
    while True:
        try:
            subtask_id = int(input("Enter subtask number: "))
        except ValueError:
            print("Subtask number not an integer")
            continue 
        if subtask_id <= 0:
            print("Subtask number not in range")
            continue
        cursor.execute("SELECT id FROM subtasks WHERE id = ? AND task_id = ?", (subtask_id, task_id ))
        
        selected_subtask = cursor.fetchone()
        if selected_subtask is None:
            print("Subtask not found.")
            continue     
        break
    status_values = ["Not Started", "In Progress", "Completed"]

    while True:
        new_status = input(
        "Enter status (Not Started, In Progress, Completed): "
        ).strip()

        if new_status not in status_values:
            print("Invalid status.")
            continue

        break
    cursor.execute("UPDATE subtasks SET status = ? WHERE id = ?", (new_status, subtask_id))
    connection.commit() 
    connection.close()
    
def calculate_progress():
    while True:
        try:
            task_id = int(input("Enter task number: "))
        except ValueError:
            print("Task number not an integer")
            continue
        if task_id <= 0:
            print("Task number not in range")
            continue   
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, name FROM tasks WHERE id = ?",
            (task_id,)
        )

        task = cursor.fetchone()
        
        if task is None:
            print("Task not found.")
            connection.close()
            continue 
        
        break
    
    cursor.execute(
        "SELECT COUNT(*) FROM subtasks WHERE task_id = ?",
        (task_id,)
    )
    total_subtasks = cursor.fetchone()[0]
    
    cursor.execute(
    "SELECT COUNT(*) FROM subtasks WHERE task_id = ? AND status = ?",
    (task_id, "Completed"))
    
    completed_subtasks = cursor.fetchone()[0]
    if total_subtasks > 0:
        progress_percentage = (completed_subtasks / total_subtasks) * 100
    else:
        progress_percentage = 0
    print(f"{task[1]} - {progress_percentage:.1f}% complete")
    connection.close()

def create_task_gui():
    task_name = task_entry.get().strip()

    if task_name == "":
        return

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (name) VALUES (?)",
        (task_name,)
    )

    connection.commit()
    connection.close()
    task_entry.delete(0, tk.END)
    refresh_task_list()
    
    messagebox.showinfo("Success", "Task created successfully!")

def refresh_task_list():
    task_listbox.delete(0, tk.END)

    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, name FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        task_listbox.insert(tk.END, f"{task[0]}. {task[1]}")
    
    

    connection.close()

def get_selected_task():
    selection = task_listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a task.")
        return
    selected_text = task_listbox.get(selection[0])
    task_id = int(selected_text.split(".")[0])
    return task_id

def refresh_subtask_list():
    task_id = get_selected_task()
    if task_id is None:
        return
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute(
    "SELECT id, name, status FROM subtasks WHERE task_id = ?",
    (task_id,))
    subtasks = cursor.fetchall()
    subtask_listbox.delete(0, tk.END)
    
    for subtask in subtasks:
        subtask_listbox.insert(tk.END, f"{subtask[0]}. {subtask[1]} - {subtask[2]}")
    connection.close()
    
def add_subtask_gui():
    task_id = get_selected_task()
    
    if task_id is None:
        return
    
    subtask_name = subtask_entry.get().strip() 
    
    if subtask_name == "":
        messagebox.showwarning("Invalid Input", "Subtask name cannot be empty.")
        return 
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    
    cursor.execute(
        "INSERT INTO subtasks (task_id, name, status) VALUES (?, ?, ?)",
        (task_id, subtask_name, "Not Started"))
    
    connection.commit()
    connection.close()
    
    subtask_entry.delete(0, tk.END)
    
    refresh_subtask_list()

  
def get_selected_subtask():
    selection = subtask_listbox.curselection()

    if not selection:
        messagebox.showwarning("No Selection", "Please select a subtask.")
        return    
    selected_text = subtask_listbox.get(selection[0])
    subtask_id = int(selected_text.split(".")[0])
    return subtask_id

def update_subtask_status_gui():
    subtask_id = get_selected_subtask()

    if subtask_id is None:
        return

    new_status = status_var.get()
    
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    
    cursor.execute(
        "UPDATE subtasks SET status = ? WHERE id = ?",
        (new_status, subtask_id))
    
    connection.commit()
    connection.close()
    
    refresh_subtask_list()

def show_progress_gui():
    task_id = get_selected_task()

    if task_id is None:
        return
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT name FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    cursor.execute(
        "SELECT COUNT(*) FROM subtasks WHERE task_id = ?",
        (task_id,))
    total_subtasks = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM subtasks WHERE task_id = ? AND status = ?",
        (task_id, "Completed"))
    completed_subtasks = cursor.fetchone()[0]
    
    if total_subtasks > 0:
        progress_percentage = (completed_subtasks / total_subtasks) * 100
    else:
        progress_percentage = 0
    
    progress_label.config(
    text=f"{task[0]} - {progress_percentage:.1f}% complete")   
    
    connection.close() 
    
def delete_task_gui():
    task_id = get_selected_task()

    if task_id is None:
        return  
    confirm = messagebox.askyesno(
    "Delete Task",
    "Are you sure you want to delete this task and all of its subtasks?")

    if not confirm:
        return
    
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM subtasks WHERE task_id = ?", (task_id,))
    
    cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
    
    connection.commit()
    connection.close()

    refresh_task_list()
    subtask_listbox.delete(0, tk.END)
    progress_label.config(text="Progress: ")
    

    
# Tkinter application
root = tk.Tk()
root.title("Task Management System")
root.geometry("900x1050")
root.minsize(700, 700)

title_label = tk.Label(
    root,
    text="Task Management System",
    font=("Arial", 20)
)
title_label.pack(pady=20)

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

create_button = tk.Button(
    root,
    text="Create Task",
    command=create_task_gui
)
create_button.pack(pady=10)
tasks_label = tk.Label(
    root,
    text="Tasks",
    font=("Arial", 14)
)
tasks_label.pack(pady=(10, 5))

task_listbox = tk.Listbox(
    root,
    width=60,
    height=8,
    exportselection=False
)
task_listbox.pack(pady=10)
task_listbox.bind("<<ListboxSelect>>", lambda event: refresh_subtask_list())

delete_task_button = tk.Button(
    root,
    text="Delete Task",
    command=delete_task_gui)

delete_task_button.pack(pady=5)

subtask_entry = tk.Entry(root, width=40)
subtask_entry.pack(pady=5)

add_subtask_button = tk.Button(
    root,
    text="Add Subtask",
    command=add_subtask_gui
)

add_subtask_button.pack(pady=5)

subtasks_label = tk.Label(
    root,
    text="Subtasks",
    font=("Arial", 14)
)
subtasks_label.pack(pady=(10, 5))

subtask_listbox = tk.Listbox(
    root,
    width=60,
    height=6,
    exportselection=False
)
subtask_listbox.pack(pady=10)

status_label = tk.Label(
    root,
    text="Update Subtask Status",
    font=("Arial", 12)
)
status_label.pack(pady=(10, 5))

status_values = ["Not Started", "In Progress", "Completed"]

status_var = tk.StringVar()
status_var.set("Not Started")

status_menu = tk.OptionMenu(
    root,
    status_var,
    *status_values
)

status_menu.pack(pady=5)

update_status_button = tk.Button(
    root,
    text="Update Status",
    command=update_subtask_status_gui
)

update_status_button.pack(pady=5)

progress_label = tk.Label(
    root,
    text="Progress: "
)

progress_label.pack(pady=10)

show_progress_button = tk.Button(
    root,
    text="Show Progress",
    command=show_progress_gui
)

show_progress_button.pack(pady=5)

refresh_task_list()

root.mainloop()


def main():
    initialize_database()
    

    while True:
        print("1. Create Tasks")
        print("2. Display Tasks")
        print("3. Add Subtasks")
        print("4. Update Subtask Status")
        print("5. Show Progress")
        print("6. Exit")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_task()
        elif choice == "2":
            display_tasks()
        elif choice == "3":
            add_subtasks()
        elif choice == "4":
            update_subtask_status()
        elif choice == "5":
            calculate_progress()
        elif choice == "6":
            print("Exiting program")
            break
        else:
            print("Invalid choice. Please try again.")
            continue
    


if __name__ == "__main__":
    main()









































