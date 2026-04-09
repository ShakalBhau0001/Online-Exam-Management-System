import customtkinter as ctk
from tkinter import messagebox as mb
from gui.login import LoginWindow
from core.db import (
    get_dashboard_stats,
    get_all_students,
    delete_student,
    get_all_results,
)


class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ Admin Dashboard — Online Exam System")
        self.geometry("980x640")
        self._center()
        self.build_ui()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"980x640+{(sw-980)//2}+{(sh-640)//2}")

    def build_ui(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self, width=190, corner_radius=0, fg_color="#0f0f1a")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="🛡️ Admin Panel",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#dc3545",
        ).pack(pady=(30, 5))
        ctk.CTkLabel(
            sidebar,
            text="Online Exam System",
            font=ctk.CTkFont(size=11),
            text_color="#555",
        ).pack(pady=(0, 25))

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)
        nav_items = [
            ("🏠  Dashboard", self.show_dashboard),
            ("👥  Students", self.show_students),
            ("📊  All Results", self.show_results),
            ("🚪  Logout", self.logout),
        ]
        for text, cmd in nav_items:
            ctk.CTkButton(
                sidebar,
                text=text,
                width=160,
                height=40,
                fg_color="transparent",
                hover_color="#1e1e2e",
                anchor="w",
                font=ctk.CTkFont(size=13),
                command=cmd,
            ).pack(pady=4, padx=15)

        self.show_dashboard()

    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ── Dashboard Tab
    def show_dashboard(self):
        self._clear()
        stats = get_dashboard_stats()
        ctk.CTkLabel(
            self.content,
            text="🏠 Dashboard Overview",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4DA6FF",
        ).pack(pady=(20, 15))

        # Stat cards row
        cards_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        cards_frame.pack(padx=25, fill="x")
        stat_cards = [
            ("👨‍🎓 Total Students", stats.get("total_students", 0), "#007bff"),
            ("📝 Total Exams", stats.get("total_exams", 0), "#6f42c1"),
            ("✅ Total Passed", stats.get("total_pass", 0), "#28a745"),
            ("❌ Total Failed", stats.get("total_fail", 0), "#dc3545"),
        ]

        for i, (label, value, color) in enumerate(stat_cards):
            card = ctk.CTkFrame(cards_frame, corner_radius=12, fg_color=color)
            card.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            cards_frame.columnconfigure(i, weight=1)

            ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color="white",
            ).pack(pady=(18, 4))
            ctk.CTkLabel(
                card, text=label, font=ctk.CTkFont(size=12), text_color="white"
            ).pack(pady=(0, 18))

        # Pass/Fail ratio bar
        total_exams = stats.get("total_exams", 0)
        if total_exams > 0:
            ctk.CTkLabel(
                self.content,
                text="Pass / Fail Ratio",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#aaa",
            ).pack(anchor="w", padx=30, pady=(20, 5))

            ratio_frame = ctk.CTkFrame(self.content, corner_radius=10)
            ratio_frame.pack(padx=25, fill="x")
            pass_pct = stats.get("total_pass", 0) / total_exams * 100
            fail_pct = 100 - pass_pct
            bar_frame = ctk.CTkFrame(ratio_frame, fg_color="transparent")
            bar_frame.pack(padx=20, pady=15, fill="x")

            ctk.CTkLabel(
                bar_frame,
                text=f"✅ Pass: {pass_pct:.1f}%",
                font=ctk.CTkFont(size=13),
                text_color="#00c853",
            ).pack(side="left", padx=10)
            ctk.CTkProgressBar(
                bar_frame, width=400, height=18, progress_color="#28a745"
            ).pack(side="left", padx=10)
            ctk.CTkLabel(
                bar_frame,
                text=f"❌ Fail: {fail_pct:.1f}%",
                font=ctk.CTkFont(size=13),
                text_color="#ff5252",
            ).pack(side="left", padx=10)

        # Subject-wise attempts
        subject_data = stats.get("subject_attempts", [])
        if subject_data:
            ctk.CTkLabel(
                self.content,
                text="Subject-wise Exam Attempts",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#aaa",
            ).pack(anchor="w", padx=30, pady=(20, 5))

            subj_frame = ctk.CTkFrame(self.content, corner_radius=10)
            subj_frame.pack(padx=25, fill="x", pady=(0, 10))
            for i, (subj, cnt) in enumerate(subject_data):
                row_f = ctk.CTkFrame(subj_frame, fg_color="transparent")
                row_f.pack(fill="x", padx=15, pady=6)
                ctk.CTkLabel(
                    row_f, text=subj, width=180, font=ctk.CTkFont(size=13), anchor="w"
                ).pack(side="left")
                max_cnt = max(c for _, c in subject_data)
                pbar = ctk.CTkProgressBar(
                    row_f, width=300, height=14, progress_color="#4DA6FF"
                )
                pbar.set(cnt / max_cnt if max_cnt else 0)
                pbar.pack(side="left", padx=10)
                ctk.CTkLabel(
                    row_f,
                    text=f"{cnt} attempts",
                    font=ctk.CTkFont(size=12),
                    text_color="#aaa",
                ).pack(side="left")

    # ── Students Tab
    def show_students(self):
        self._clear()
        ctk.CTkLabel(
            self.content,
            text="👥 All Students",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4DA6FF",
        ).pack(pady=(20, 10))

        students = get_all_students()
        scroll = ctk.CTkScrollableFrame(self.content)
        scroll.pack(padx=20, pady=5, fill="both", expand=True)
        headers = ["Username", "Name", "Contact", "Email", "Action"]
        widths = [120, 155, 120, 205, 100]
        for c, (h, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                scroll,
                text=h,
                width=w,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4DA6FF",
            ).grid(row=0, column=c, padx=5, pady=8)

        if students:
            for r, (uname, name, contact, email) in enumerate(students, start=1):
                for c, (v, w) in enumerate(zip([uname, name, contact, email], widths)):
                    ctk.CTkLabel(
                        scroll, text=v, width=w, font=ctk.CTkFont(size=12)
                    ).grid(row=r, column=c, padx=5, pady=5)
                ctk.CTkButton(
                    scroll,
                    text="Delete",
                    width=85,
                    height=26,
                    fg_color="#dc3545",
                    hover_color="#b02a37",
                    font=ctk.CTkFont(size=11),
                    command=lambda u=uname: self._confirm_delete(u),
                ).grid(row=r, column=4, padx=5, pady=5)
        else:
            ctk.CTkLabel(scroll, text="No students found.", text_color="#888").grid(
                row=1, column=0, columnspan=5, pady=20
            )

    def _confirm_delete(self, username: str):
        if mb.askyesno(
            "Confirm Delete", f"Delete student '{username}' and all their exam results?"
        ):
            if delete_student(username):
                mb.showinfo("Success", f"Student '{username}' deleted successfully.")
                self.show_students()
            else:
                mb.showerror("Error", "Could not delete student.")

    # ── Results Tab
    def show_results(self):
        self._clear()
        ctk.CTkLabel(
            self.content,
            text="📊 All Exam Results",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4DA6FF",
        ).pack(pady=(20, 10))

        results = get_all_results()
        scroll = ctk.CTkScrollableFrame(self.content)
        scroll.pack(padx=20, pady=5, fill="both", expand=True)
        headers = ["Username", "Name", "Subject", "Score", "Marks", "Status", "Date"]
        widths = [100, 130, 155, 70, 70, 85, 160]
        for c, (h, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                scroll,
                text=h,
                width=w,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4DA6FF",
            ).grid(row=0, column=c, padx=4, pady=8)

        if results:
            for r, (uname, name, subj, score, total, passed, date) in enumerate(
                results, start=1
            ):
                pct = f"{score/total*100:.0f}%"
                status = "✅ Pass" if passed else "❌ Fail"
                sc = "#00c853" if passed else "#ff5252"
                vals = [
                    uname,
                    name,
                    subj,
                    f"{score}/{total}",
                    pct,
                    status,
                    str(date)[:16],
                ]
                colors = [None, None, None, None, None, sc, None]
                for c, (v, w, col) in enumerate(zip(vals, widths, colors)):
                    ctk.CTkLabel(
                        scroll,
                        text=v,
                        width=w,
                        font=ctk.CTkFont(size=11),
                        text_color=col if col else "white",
                    ).grid(row=r, column=c, padx=4, pady=4)
        else:
            ctk.CTkLabel(scroll, text="No exam results yet.", text_color="#888").grid(
                row=1, column=0, columnspan=7, pady=20
            )

    # ── Logout
    def logout(self):
        self.destroy()
        LoginWindow().mainloop()
