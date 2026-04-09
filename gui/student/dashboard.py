import customtkinter as ctk
from gui.student.exam import ExamWindow
from gui.student.history import HistoryWindow
from gui.login import LoginWindow
from core.questions import SUBJECTS


class StudentDashboard(ctk.CTk):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.title(f"Student Dashboard — {username}")
        self.geometry("560x500")
        self.resizable(False, False)
        self._center()
        self.build_ui()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"560x500+{(sw-560)//2}+{(sh-500)//2}")

    def build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="📝 Online Exam Portal",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#4DA6FF",
        ).pack(side="left", padx=25, pady=20)
        ctk.CTkLabel(
            header,
            text=f"👤 {self.username}",
            font=ctk.CTkFont(size=13),
            text_color="#aaaaaa",
        ).pack(side="right", padx=25, pady=20)

        # Subject selector card
        subj_frame = ctk.CTkFrame(self, corner_radius=12)
        subj_frame.pack(padx=40, pady=(25, 10), fill="x")
        ctk.CTkLabel(
            subj_frame,
            text="📚 Select Subject :",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=18, sticky="w")

        self.subject_var = ctk.StringVar(value=list(SUBJECTS.keys())[0])
        ctk.CTkOptionMenu(
            subj_frame,
            values=list(SUBJECTS.keys()),
            variable=self.subject_var,
            width=230,
            font=ctk.CTkFont(size=13),
        ).grid(row=0, column=1, padx=15, pady=18)

        # Exam info card
        info_frame = ctk.CTkFrame(self, corner_radius=12)
        info_frame.pack(padx=40, pady=10, fill="x")
        for i, (k, v) in enumerate(
            [
                ("❓ Questions", "10 (Random each attempt)"),
                ("🔤 Type", "Multiple Choice (MCQ)"),
                ("⏱️ Time Limit", "10 Minutes"),
                ("✅ Pass Marks", "60% and above"),
            ]
        ):
            ctk.CTkLabel(
                info_frame,
                text=f"  {k} :",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
            ).grid(row=i, column=0, padx=20, pady=8, sticky="w")
            ctk.CTkLabel(
                info_frame,
                text=v,
                font=ctk.CTkFont(size=13),
                text_color="#aaaaaa",
                anchor="w",
            ).grid(row=i, column=1, padx=10, pady=8, sticky="w")

        # Action buttons
        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(pady=25)
        ctk.CTkButton(
            btn_f,
            text="▶  START EXAM",
            width=150,
            height=42,
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.start_exam,
        ).grid(row=0, column=0, padx=12)

        ctk.CTkButton(
            btn_f,
            text="📊 My History",
            width=130,
            height=42,
            fg_color="#6f42c1",
            hover_color="#5a32a3",
            font=ctk.CTkFont(size=13),
            command=self.show_history,
        ).grid(row=0, column=1, padx=12)

        ctk.CTkButton(
            btn_f,
            text="🚪 Logout",
            width=110,
            height=42,
            fg_color="#6c757d",
            hover_color="#545b62",
            font=ctk.CTkFont(size=13),
            command=self.logout,
        ).grid(row=0, column=2, padx=12)

    def start_exam(self):
        subject_name = self.subject_var.get()
        subject_key = SUBJECTS[subject_name]
        self.destroy()
        ExamWindow(
            username=self.username, subject_name=subject_name, subject_key=subject_key
        ).mainloop()

    def show_history(self):
        HistoryWindow(self, self.username)

    def logout(self):
        self.destroy()
        LoginWindow().mainloop()
