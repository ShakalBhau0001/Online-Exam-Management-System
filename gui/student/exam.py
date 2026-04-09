import customtkinter as ctk
from tkinter import messagebox
from gui.student.dashboard import StudentDashboard
from core.db import save_result
from core.questions import (
    get_shuffled_questions,
    TOTAL_QUESTIONS,
    TIMER_SECONDS,
    PASS_PERCENT,
)


class ReviewWindow(ctk.CTkToplevel):
    def __init__(self, master, questions: list, user_answers: list, score: int):
        super().__init__(master)
        self.title("📋 Answer Review")
        self.geometry("700x620")
        self.grab_set()
        self._center()
        self.questions = questions
        self.user_answers = user_answers
        self.score = score
        self.build_ui()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"700x620+{(sw-700)//2}+{(sh-620)//2}")

    def build_ui(self):
        total = len(self.questions)
        percent = (self.score / total) * 100
        grade = (
            "Excellent 🏆"
            if percent >= 80
            else "Good 👍" if percent >= 60 else "Keep Practicing 📚"
        )

        # Score banner
        banner = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=0, height=75)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        ctk.CTkLabel(
            banner,
            text=f"🎉  Score: {self.score}/{total}  |  {percent:.0f}%  |  {grade}",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#4DA6FF",
        ).pack(expand=True)

        # Scrollable review
        scroll = ctk.CTkScrollableFrame(
            self,
            label_text="📝 Question-wise Review",
            label_font=ctk.CTkFont(size=13, weight="bold"),
        )
        scroll.pack(padx=20, pady=(10, 5), fill="both", expand=True)

        for i, q in enumerate(self.questions):
            u_idx = self.user_answers[i]
            c_idx = q["answer"]
            ok = u_idx == c_idx
            card = ctk.CTkFrame(
                scroll, fg_color="#1e3a1e" if ok else "#3a1e1e", corner_radius=10
            )
            card.pack(fill="x", padx=5, pady=6)
            ctk.CTkLabel(
                card,
                text=f"{'✅' if ok else '❌'}  Q{i+1}. {q['question']}",
                font=ctk.CTkFont(size=13, weight="bold"),
                wraplength=600,
                justify="left",
                anchor="w",
            ).pack(padx=15, pady=(12, 4), anchor="w")

            for j, opt in enumerate(q["options"]):
                if j == c_idx == u_idx:
                    color, pre = "#00c853", "✔ Your Answer (Correct): "
                elif j == c_idx:
                    color, pre = "#00c853", "✔ Correct Answer: "
                elif j == u_idx:
                    color, pre = "#ff5252", "✘ Your Answer (Wrong): "
                else:
                    color, pre = "#888888", "      "
                ctk.CTkLabel(
                    card,
                    text=f"  {pre}{opt}",
                    font=ctk.CTkFont(size=12),
                    text_color=color,
                    anchor="w",
                ).pack(padx=20, pady=1, anchor="w")
            ctk.CTkLabel(card, text="").pack(pady=3)

        # Buttons
        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(pady=10)
        ctk.CTkButton(
            btn_f,
            text="🏠 Back to Dashboard",
            width=180,
            height=38,
            fg_color="#007bff",
            hover_color="#0056b3",
            command=self.go_home,
        ).grid(row=0, column=0, padx=15)
        ctk.CTkButton(
            btn_f,
            text="❌ Close & Exit",
            width=130,
            height=38,
            fg_color="#dc3545",
            hover_color="#b02a37",
            command=self.close_all,
        ).grid(row=0, column=1, padx=15)

    def go_home(self):
        username = self.master.username
        self.master.destroy()
        StudentDashboard(username).mainloop()

    def close_all(self):
        self.master.destroy()


class ExamWindow(ctk.CTk):
    def __init__(self, username: str, subject_name: str, subject_key: str):
        super().__init__()
        self.username = username
        self.subject_name = subject_name
        self.subject_key = subject_key
        self.title(f"Exam — {subject_name}")
        self.geometry("650x510")
        self.resizable(False, False)
        self._center()

        # Exam state
        self.current_q = 0
        self.score = 0
        self.selected = ctk.IntVar(value=-1)
        self.user_answers = []
        self.time_left = TIMER_SECONDS
        self.exam_active = True

        # Block window close during exam
        self.protocol("WM_DELETE_WINDOW", self._block_close)
        self.questions = get_shuffled_questions(subject_key)
        self.build_ui()
        self.load_question()
        self.update_timer()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"650x510+{(sw-650)//2}+{(sh-510)//2}")

    def _block_close(self):
        messagebox.showwarning(
            "Exam In Progress",
            "⚠️ Exam is in progress!\nPlease complete the exam before exiting.",
        )

    def build_ui(self):
        # Header with timer
        header = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=0, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)
        self.header_label = ctk.CTkLabel(
            header,
            text=f"Question 1 / {TOTAL_QUESTIONS}  |  {self.subject_name}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#4DA6FF",
        )
        self.header_label.pack(side="left", padx=20, pady=20)
        self.timer_label = ctk.CTkLabel(
            header,
            text="⏱ 10:00",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFD700",
        )
        self.timer_label.pack(side="right", padx=20, pady=20)

        # Question card
        q_frame = ctk.CTkFrame(self, corner_radius=12)
        q_frame.pack(padx=30, pady=15, fill="both", expand=True)
        self.question_label = ctk.CTkLabel(
            q_frame,
            text="",
            font=ctk.CTkFont(size=15, weight="bold"),
            wraplength=555,
            justify="left",
            anchor="w",
        )
        self.question_label.pack(padx=20, pady=(20, 10), anchor="w")
        self.option_buttons = []
        for i in range(4):
            rb = ctk.CTkRadioButton(
                q_frame,
                text="",
                variable=self.selected,
                value=i,
                font=ctk.CTkFont(size=13),
            )
            rb.pack(padx=30, pady=7, anchor="w")
            self.option_buttons.append(rb)

        # Bottom — only NEXT button, no BACK
        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(pady=14)
        self.next_btn = ctk.CTkButton(
            btn_f,
            text="NEXT ▶",
            width=160,
            height=40,
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.next_question,
        )
        self.next_btn.pack()

    def update_timer(self):
        if not self.exam_active:
            return
        if self.time_left <= 0:
            self.exam_active = False
            messagebox.showwarning(
                "Time Up!", "⏰ Time is up! Exam has been auto-submitted."
            )
            while len(self.user_answers) < TOTAL_QUESTIONS:
                self.user_answers.append(-1)
            self.finish_exam()
            return

        mins = self.time_left // 60
        secs = self.time_left % 60
        color = "#ff5252" if self.time_left <= 60 else "#FFD700"
        self.timer_label.configure(text=f"⏱ {mins:02d}:{secs:02d}", text_color=color)
        self.time_left -= 1
        self.after(1000, self.update_timer)

    def load_question(self):
        q = self.questions[self.current_q]
        self.header_label.configure(
            text=f"Question {self.current_q+1} / {TOTAL_QUESTIONS}  |  {self.subject_name}"
        )
        self.question_label.configure(text=f"Q{self.current_q+1}.  {q['question']}")
        self.selected.set(-1)
        for i, btn in enumerate(self.option_buttons):
            btn.configure(text=q["options"][i])
        if self.current_q == TOTAL_QUESTIONS - 1:
            self.next_btn.configure(text="SUBMIT ✅")

    def next_question(self):
        if self.selected.get() == -1:
            messagebox.showwarning(
                "No Selection", "Please select an option before proceeding!"
            )
            return

        chosen = self.selected.get()
        self.user_answers.append(chosen)
        if chosen == self.questions[self.current_q]["answer"]:
            self.score += 1
        self.current_q += 1
        if self.current_q >= TOTAL_QUESTIONS:
            self.finish_exam()
        else:
            self.load_question()

    def finish_exam(self):
        self.exam_active = False
        # Allow window to be closed now
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        passed = self.score >= int(TOTAL_QUESTIONS * PASS_PERCENT)
        percent = (self.score / TOTAL_QUESTIONS) * 100
        grade = (
            "Excellent 🏆"
            if percent >= 80
            else "Good 👍" if percent >= 60 else "Keep Practicing 📚"
        )

        save_result(
            self.username, self.subject_name, self.score, TOTAL_QUESTIONS, passed
        )

        messagebox.showinfo(
            "Exam Result",
            f"🎉 Exam Completed!\n\n"
            f"Subject : {self.subject_name}\n"
            f"Score   : {self.score} / {TOTAL_QUESTIONS}\n"
            f"Marks   : {percent:.0f}%\n"
            f"Grade   : {grade}\n"
            f"Status  : {'✅ PASSED' if passed else '❌ FAILED'}\n\n"
            f"Click OK to see Answer Review 📋",
        )
        self.withdraw()
        ReviewWindow(self, self.questions, self.user_answers, self.score)
