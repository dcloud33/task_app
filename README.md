# Task Management System

A Python desktop task management application built with **Tkinter** and **SQLite**.

The application allows users to create tasks, add and manage subtasks, update completion statuses, calculate task progress, and persist data between application sessions.

This project was developed incrementally to strengthen practical skills in Python application design, relational databases, event-driven GUI development, input validation, debugging, and software organization.

---

## Project Overview

The Task Management System began as a command-line Python application using in-memory data structures.

The project was then progressively expanded through several stages:

1. In-memory Python task management
2. JSON persistence
3. SQLite database migration
4. Relational task/subtask modeling
5. Tkinter graphical user interface
6. GUI-driven database operations
7. Input validation and application-state handling

This progression allowed the application architecture to evolve while preserving the core business logic.

---

## Features

### Task Management

- Create tasks
- Display existing tasks
- Select tasks from the graphical interface
- Delete tasks
- Automatically delete associated subtasks when a task is removed

### Subtask Management

- Add multiple subtasks to a task
- Display subtasks belonging to the selected task
- Update subtask status
- Persist status changes in SQLite

Supported statuses:

- `Not Started`
- `In Progress`
- `Completed`

### Progress Tracking

Task completion is calculated using:

```text
Completed Subtasks / Total Subtasks × 100
```

Example:

```text
Task: Python Study

Subtasks:
- Review Functions — Completed
- Practice SQLite — Completed
- Build Tkinter GUI — In Progress
- Write Tests — Not Started

Completion: 50.0%
```

Only subtasks marked `Completed` contribute toward the completion percentage.

### Persistent Storage

Application data is stored in SQLite.

Tasks and subtasks remain available after the application is closed and restarted.

### Graphical User Interface

The Tkinter interface provides controls for:

- Task creation
- Task selection
- Task deletion
- Subtask creation
- Subtask selection
- Status updates
- Task progress calculation

The application refreshes the GUI automatically after database changes.

---

## Technology Stack

### Language

- Python 3

### Database

- SQLite

### GUI

- Tkinter

### Python Standard Library

- `sqlite3`
- `tkinter`

### Development Tools

- Git
- GitHub
- Visual Studio Code
- macOS Terminal

---

## Application Architecture

The application follows a simple layered flow:

```text
User
  |
  v
Tkinter GUI
  |
  v
Python Application Logic
  |
  v
SQLite Queries
  |
  v
tasks.db
```

The graphical interface handles user interaction while Python functions perform validation and database operations.

SQLite acts as the persistent source of truth.

---

## Database Design

The application uses two relational tables.

### Tasks Table

```text
tasks
-------------------------
id      INTEGER PRIMARY KEY
name    TEXT NOT NULL
```

Example:

| id | name |
|---:|---|
| 1 | Terraform Practice |
| 2 | Python Study |

### Subtasks Table

```text
subtasks
-----------------------------------------
id        INTEGER PRIMARY KEY
task_id   INTEGER NOT NULL
name      TEXT NOT NULL
status    TEXT NOT NULL
```

Example:

| id | task_id | name | status |
|---:|---:|---|---|
| 1 | 2 | Review Functions | Completed |
| 2 | 2 | Practice SQLite | In Progress |

### Relationship

The application uses a **one-to-many relationship**:

```text
Task
 |
 | 1
 |
 +-------------------+
                     |
                     | many
                     v
                  Subtasks
```

Each subtask contains a `task_id` that references its parent task.

Example:

```text
tasks.id = 3
name = "Python Study"

            |
            |
            v

subtasks.task_id = 3
name = "Practice SQLite"
```

---

## Database Initialization

The application automatically initializes the database when it starts.

```python
def initialize_database():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
```

Tables are created using:

```sql
CREATE TABLE IF NOT EXISTS
```

This allows the application to safely start whether or not the database has already been created.

---

## CRUD Operations

The project implements standard CRUD-style database operations.

### Create

Create a task:

```sql
INSERT INTO tasks (name)
VALUES (?)
```

Create a subtask:

```sql
INSERT INTO subtasks (task_id, name, status)
VALUES (?, ?, ?)
```

### Read

Retrieve tasks:

```sql
SELECT id, name
FROM tasks
```

Retrieve subtasks belonging to a task:

```sql
SELECT id, name, status
FROM subtasks
WHERE task_id = ?
```

### Update

Update a subtask status:

```sql
UPDATE subtasks
SET status = ?
WHERE id = ?
```

### Delete

Delete associated subtasks:

```sql
DELETE FROM subtasks
WHERE task_id = ?
```

Then delete the parent task:

```sql
DELETE FROM tasks
WHERE id = ?
```

This prevents subtasks from being left behind after their parent task is removed.

---

## Progress Calculation

Progress is calculated by querying SQLite directly.

Total subtasks:

```sql
SELECT COUNT(*)
FROM subtasks
WHERE task_id = ?
```

Completed subtasks:

```sql
SELECT COUNT(*)
FROM subtasks
WHERE task_id = ?
AND status = ?
```

Python then calculates:

```python
if total_subtasks > 0:
    progress_percentage = (
        completed_subtasks / total_subtasks
    ) * 100
else:
    progress_percentage = 0
```

The zero-subtask guard prevents division-by-zero errors.

---

## Input Validation

The application includes validation for several common user errors.

### Empty Task Names

```python
if task_name == "":
    return
```

### Empty Subtask Names

Users cannot create blank subtasks.

### Invalid Database Selections

The CLI version validated IDs before database operations using queries such as:

```sql
SELECT id
FROM tasks
WHERE id = ?
```

### GUI Selection Validation

Actions requiring a selected task or subtask display a warning when nothing is selected.

Example:

```python
if not selection:
    messagebox.showwarning(
        "No Selection",
        "Please select a task."
    )
    return
```

---

## GUI Design

The Tkinter interface contains several major sections.

```text
Task Management System

[ Task Name Entry ]
[ Create Task ]

Tasks

[ Task List ]

[ Delete Task ]

[ Subtask Entry ]
[ Add Subtask ]

Subtasks

[ Subtask List ]

Update Subtask Status

[ Status Dropdown ]
[ Update Status ]

Progress: 50.0%

[ Show Progress ]
```

Task and subtask selections are maintained independently using:

```python
exportselection=False
```

This solved an issue where selecting a subtask caused the task selection to disappear.

---

## Key Engineering Challenges

### 1. Moving From In-Memory Data to Persistent Storage

The original application stored tasks in Python lists and dictionaries.

Example:

```python
tasks = [
    {
        "name": "Python Study",
        "subtasks": []
    }
]
```

This data disappeared when the program terminated.

The application initially added JSON persistence before later migrating to SQLite.

#### What I Learned

Storage concerns should be separated from application logic so the persistence layer can evolve without redesigning the entire application.

---

### 2. Modeling Task Relationships

The original nested Python structure naturally represented:

```text
Task
 └── Subtasks
```

Migrating to SQLite required translating this relationship into two tables connected through a foreign key.

#### What I Learned

Relational database design represents application relationships differently from nested Python data structures but solves the same underlying problem.

---

### 3. Preventing Invalid Database Operations

A positive integer does not necessarily represent an existing database record.

The application validates IDs before continuing:

```sql
SELECT id
FROM tasks
WHERE id = ?
```

#### What I Learned

Input validation has multiple layers:

```text
Is the input the correct type?
        |
        v
Is the value valid?
        |
        v
Does the database record exist?
```

---

### 4. Tkinter Listbox Selection State

While testing the GUI, selecting a subtask caused the selected task to lose focus.

This resulted in:

```text
Please select a task.
```

appearing during status updates.

The issue was resolved using:

```python
exportselection=False
```

for both listboxes.

#### What I Learned

GUI applications introduce application-state concerns that do not exist in command-line programs.

---

### 5. GUI Layout Constraints

As features were added, the application became taller than the available screen space.

This was addressed by:

- Reducing Listbox heights
- Reducing vertical padding
- Setting a minimum window size
- Reconsidering how widgets were organized

#### What I Learned

GUI development requires considering both functionality and usability.

---

## Project Evolution

### Phase 1 — Python Fundamentals

Implemented:

- Lists
- Dictionaries
- Loops
- Conditionals
- Input validation
- Nested data structures
- Completion calculations

### Phase 2 — Modular Functions

Application logic was separated into functions including:

```text
create_task()
display_tasks()
select_task()
add_subtasks()
update_subtask_status()
calculate_progress()
```

This reduced duplicated logic and improved readability.

### Phase 3 — JSON Persistence

Added:

```python
json.dump()
json.load()
```

This allowed data to survive between executions.

### Phase 4 — SQLite Migration

JSON was replaced with SQLite.

Implemented:

- Database initialization
- Task insertion
- Subtask insertion
- Relational queries
- Status updates
- Progress queries
- Task deletion

SQLite became the application's persistent source of truth.

### Phase 5 — Tkinter GUI

The command-line interface was replaced with an event-driven GUI.

Implemented:

- Entry widgets
- Buttons
- Listboxes
- OptionMenu
- Labels
- Message boxes
- Selection events
- Database-driven refresh functions

---

## Skills Demonstrated

### Python

- Functions
- Conditionals
- Loops
- Exceptions
- Variables
- Lists
- Dictionaries
- Tuples
- String manipulation
- Modular programming

### SQL and Databases

- Relational modeling
- Primary keys
- Foreign keys
- Parameterized queries
- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `COUNT`
- Database persistence

### GUI Development

- Tkinter
- Event-driven programming
- Listbox selection
- Entry widgets
- Buttons
- Dropdown menus
- Message dialogs
- Dynamic GUI refreshes

### Software Engineering

- Incremental development
- Input validation
- Guard clauses
- Separation of concerns
- Debugging
- Persistence design
- State management
- Refactoring
- Feature testing

---

## Running the Application

### Requirements

- Python 3
- Tkinter
- SQLite

Tkinter and SQLite are included with many standard Python installations.

### Clone the Repository

```bash
git clone <repository-url>
```

Enter the project directory:

```bash
cd <repository-name>
```

Run the application:

```bash
python3 python_project-1.py
```

The SQLite database will be initialized automatically.

---

## Project Structure

Current structure:

```text
task-management-system/
│
├── python_project-1.py
├── tasks.db
└── README.md
```

A future refactor could separate responsibilities into:

```text
task-management-system/
│
├── app/
│   ├── database.py
│   ├── tasks.py
│   ├── gui.py
│   └── __init__.py
│
├── tests/
│   └── test_tasks.py
│
├── main.py
├── README.md
└── requirements.txt
```

---

## Future Improvements

Potential future enhancements include:

- Task editing
- Subtask deletion
- Due dates
- Task priorities
- Task categories
- Sorting and filtering
- Search
- Progress bars
- Automated tests
- Application logging
- Database abstraction
- PostgreSQL support
- REST API
- FastAPI backend
- Web frontend
- Docker containerization
- CI/CD pipeline

---

## What I Learned

This project helped reinforce that application development is more than writing individual Python statements.

The application evolved from:

```text
Python fundamentals
        ↓
data structures
        ↓
functions
        ↓
persistent files
        ↓
relational database
        ↓
event-driven GUI
```

One of the most important lessons was learning how separate pieces of an application communicate.

The GUI does not need to understand how SQLite stores the data.

SQLite does not need to understand how the GUI displays it.

Python functions connect those layers together.

That separation made it possible to progressively replace the original command-line and JSON implementations without rebuilding the entire project.

---

## Project Status

**Status:** Functional / Final Polish

Core functionality is complete.

Current work includes:

- Final testing
- UI cleanup
- Documentation
- Repository cleanup
- GitHub publication