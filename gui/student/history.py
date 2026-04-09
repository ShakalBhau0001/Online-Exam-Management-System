import customtkinter as ctk
from core.db import get_subject_performance, get_student_history


class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, master, username: str):
        super().__init__(master)
        self.title("📊 My Exam History")
        self.geometry("760x590")
        self.grab_set()
        self._center()
        self.username = username
        self.build_ui()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"760x590+{(sw-760)//2}+{(sh-590)//2}")

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text=f"📊 Exam History — {self.username}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4DA6FF",
        ).pack(pady=(20, 5))

        # Subject-wise performance table
        ctk.CTkLabel(
            self,
            text="Subject-wise Performance",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#aaa",
        ).pack(anchor="w", padx=25, pady=(10, 3))
        subj_frame = ctk.CTkFrame(self, corner_radius=10)
        subj_frame.pack(padx=20, fill="x")
        headers = ["Subject", "Attempts", "Avg %", "Best Score", "Passes"]
        widths = [200, 80, 80, 110, 80]
        for c, (h, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                subj_frame,
                text=h,
                width=w,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4DA6FF",
            ).grid(row=0, column=c, padx=5, pady=8)

        rows = get_subject_performance(self.username)
        if rows:
            for r, (subj, attempts, avg, best, passes) in enumerate(rows, start=1):
                for c, (v, w) in enumerate(
                    zip(
                        [subj, str(attempts), f"{avg}%", f"{best}/10", str(passes)],
                        widths,
                    )
                ):
                    ctk.CTkLabel(
                        subj_frame, text=v, width=w, font=ctk.CTkFont(size=12)
                    ).grid(row=r, column=c, padx=5, pady=5)
        else:
            ctk.CTkLabel(subj_frame, text="No attempts yet.", text_color="#888").grid(
                row=1, column=0, columnspan=5, pady=10
            )

        # All attempts
        ctk.CTkLabel(
            self,
            text="All Attempts",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#aaa",
        ).pack(anchor="w", padx=25, pady=(15, 3))
        scroll = ctk.CTkScrollableFrame(self, height=230)
        scroll.pack(padx=20, pady=(0, 10), fill="both", expand=True)
        h_headers = ["Subject", "Score", "Marks", "Status", "Date & Time"]
        h_widths = [200, 75, 75, 85, 185]
        for c, (h, w) in enumerate(zip(h_headers, h_widths)):
            ctk.CTkLabel(
                scroll,
                text=h,
                width=w,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4DA6FF",
            ).grid(row=0, column=c, padx=5, pady=6)

        history = get_student_history(self.username)
        if history:
            for r, (subj, score, total, passed, date) in enumerate(history, start=1):
                pct = f"{score/total*100:.0f}%"
                status = "✅ Pass" if passed else "❌ Fail"
                s_color = "#00c853" if passed else "#ff5252"
                vals = [subj, f"{score}/{total}", pct, status, str(date)[:16]]
                colors = [None, None, None, s_color, None]
                for c, (v, w, col) in enumerate(zip(vals, h_widths, colors)):
                    ctk.CTkLabel(
                        scroll,
                        text=v,
                        width=w,
                        font=ctk.CTkFont(size=12),
                        text_color=col if col else "white",
                    ).grid(row=r, column=c, padx=5, pady=4)
        else:
            ctk.CTkLabel(scroll, text="No exam history found.", text_color="#888").grid(
                row=1, column=0, columnspan=5, pady=15
            )

        ctk.CTkButton(
            self,
            text="Close",
            width=120,
            height=36,
            fg_color="#6c757d",
            hover_color="#545b62",
            command=self.destroy,
        ).pack(pady=10)
