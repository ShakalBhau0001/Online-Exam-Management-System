# Online-Exam-Management-System
A GUI-based Online Exam Management System built in Python, supporting admin and student roles with features like exam creation, question management, real-time test execution, and result tracking using a structured database backend.

---

## 📁 Project Structure

```
OnlineExamSystem/
│
├── core/
│   ├── __init__.py
│   ├── db.py              ← All database operations
│   └── questions.py       ← Question bank (Java, Python, DBMS)
│
├── gui/
│   ├── __init__.py
│   ├── login.py           ← Unified Login (Student + Admin)
│   │
│   ├── student/
│   │   ├── __init__.py
│   │   ├── dashboard.py   ← Student Home Screen
│   │   ├── exam.py        ← MCQ Exam + Answer Review
│   │   ├── history.py     ← Exam History & Performance
│   │   └── signup.py      ← Student Registration
│   │
│   └── admin/
│       ├── __init__.py
│       └── dashboard.py   ← Admin Panel (Stats + Students + Results)
│
├── main.py                ← Entry Point
├── setup_db.py            ← One-time DB setup
├── requirements.txt
├── LICENCE
└── README.md
```

---
