# 📝 Online Exam Management System

**Online Exam Management System** is a **modern desktop-based online examination system** built with **Python, CustomTkinter, and MySQL**, designed to simplify digital exam workflows with a clean and interactive user interface.

The system supports **Admin and Student role-based access**, allowing administrators to manage question banks, monitor student performance, and control exam activities, while students can securely sign up, log in, attempt MCQ-based exams, review answers, and track exam history.

This project demonstrates **Python GUI development, database integration, modular architecture, and real-world role-based workflows**, making it ideal for academic mini-projects and portfolio showcases.

---

## ✨ Key Principles

1. **Role-Based Access** – Separate Admin and Student interfaces  
2. **MCQ Exam Automation** – Auto-evaluation with instant scoring  
3. **Structured Architecture** – Modular `core` and `gui` separation  
4. **Performance Tracking** – Students can review exam history and results  

 This system is both **practical and educational**, demonstrating how modern desktop-based examination systems are built using Python.

---

## 🧩 System Overview

The application is built around two primary user roles:

### 👨‍💼 Admin
- Admin login access
- Manage question bank
- Monitor student exam performance
- View system-level records
- Control exam flow

### 👨‍🎓 Student
- Student registration & signup
- Secure login
- Dashboard access
- Attempt MCQ exams
- Review answers after submission
- View exam history

### 📊 Result & Analytics
- Automatic score calculation
- Exam-wise performance tracking
- Previous exam history
- Student progress insights

---

## 🔗 Core Workflow

- Students create an account and log in  
- Admin manages question bank  
- Student starts MCQ exam  
- System auto-checks answers  
- Results are saved in database  
- Students can review performance history  

> Ensures smooth digital exam execution with instant feedback.

---

## ⚙️ Features

- Python GUI desktop application
- Admin and Student authentication
- Student signup system
- MCQ-based real-time exam
- Answer review after exam
- Exam history tracking
- Modular folder architecture
- Database-backed persistent storage

---

## 📁 Project Structure

```bash
Online-Exam-Management-System/
│
├── assets/                        # Screenshots / images
├── core/
│   ├── __init__.py
│   ├── db.py                      # All database operations
│   └── questions.py               # Question bank
│
├── gui/
│   ├── __init__.py
│   ├── login.py                   # Unified Login
│   │
│   ├── student/
│   │   ├── __init__.py
│   │   ├── dashboard.py           # Student Home Screen
│   │   ├── exam.py                # MCQ Exam + Answer Review
│   │   ├── history.py             # Exam History
│   │   └── signup.py              # Student Registration
│   │
│   └── admin/
│       ├── __init__.py
│       └── dashboard.py           # Admin Panel
│
├── main.py                        # Entry Point
├── setup_db.py                    # One-time DB setup
├── requirements.txt               # Dependencies
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
- Python 3.10+
- Tkinter (GUI support)
- SQLite / local DB support
- pip package manager

### 2️⃣ Clone Repository
```bash
git clone https://github.com/ShakalBhau0001/Online-Exam-Management-System.git
cd Online-Exam-Management-System
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Database
```bash
python setup_db.py
```

### 5️⃣ Run Application
```bash
python main.py
```

---

## 🔑 Modules

### Login System

- Unified login interface
- Admin authentication
- Student authentication
- Registration support

### Student Dashboard

- Start new exam
- Review answers
- Check exam history
- Track performance

### Admin Dashboard

- Manage questions
- Access records
- Monitor exams

---

## 🧠 Exam Logic

| Feature | Description |
|---|---|
| Question Type | MCQ |
| Evaluation | Automatic |
| Result | Instant |
| Review | Supported |
| History | Stored |

> Objective answers are automatically checked immediately after submission.

---

## 🗄️ Database Design

### Students
```json
{
  "student_id": 101,
  "name": "Rahul",
  "email": "rahul@email.com"
}
```

### Questions
```json
{
  "question_id": 1,
  "question": "What is Python?",
  "options": ["Language", "OS", "Browser", "IDE"],
  "answer": "Language"
}
```

### Results
```json
{
  "student_id": 101,
  "score": 8,
  "total": 10,
  "percentage": 80
}
```

---

## 🖼️ Screenshots

### 1. Login Screen
![Login](assets/login.png)

### 2. Student Dashboard
![Student Dashboard](assets/student_dashboard.png)

### 3. MCQ Exam Window
![Exam Window](assets/exam.png)

### 4. Exam History
![History](assets/history.png)

### 5. Admin Dashboard
![Admin Dashboard](assets/admin_dashboard.png)

---

## 🛣️ Future Improvements

- Timer-based exams
- Subject-wise categories
- Leaderboard system
- PDF result export
- Multi-admin roles

---

## 🙏 Acknowledgments

- Python community
- CustomTkinter
- MySQL
- Open-source contributors

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Contributors

> Developer: **Shakal Bhau** & **Rajlaxmi Patil**

> GitHub: **[ShakalBhau0001](https://github.com/ShakalBhau0001) & [Rajlaxmi-1307](https://github.com/Rajlaxmi-1307)**

---
