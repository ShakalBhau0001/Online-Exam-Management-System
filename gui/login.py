import customtkinter as ctk
from tkinter import messagebox
from gui.student.signup import SignupWindow
from gui.student.dashboard import StudentDashboard
from gui.admin.dashboard import AdminDashboard
from core.db import validate_login, validate_admin


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Online Exam System — Login")
        self.geometry("520x480")
        self.resizable(False, False)
        self._center()
        self.build_ui()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"520x480+{(sw-520)//2}+{(sh-480)//2}")

    def build_ui(self):
        # Header
        ctk.CTkLabel(
            self,
            text="🎓 Online Exam System",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4DA6FF",
        ).pack(pady=(40, 5))
        ctk.CTkLabel(
            self,
            text="Select role and login to continue",
            font=ctk.CTkFont(size=13),
            text_color="#888",
        ).pack(pady=(0, 20))

        # Role selector
        role_frame = ctk.CTkFrame(self, fg_color="transparent")
        role_frame.pack(pady=(0, 10))
        self.role_var = ctk.StringVar(value="student")

        ctk.CTkRadioButton(
            role_frame,
            text="👨‍🎓 Student",
            variable=self.role_var,
            value="student",
            font=ctk.CTkFont(size=13),
        ).grid(row=0, column=0, padx=20)
        ctk.CTkRadioButton(
            role_frame,
            text="🛡️ Admin",
            variable=self.role_var,
            value="admin",
            font=ctk.CTkFont(size=13),
        ).grid(row=0, column=1, padx=20)

        # Form
        form = ctk.CTkFrame(self, corner_radius=15)
        form.pack(padx=50, pady=5, fill="both", expand=True)

        ctk.CTkLabel(form, text="Username :", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=20, pady=(25, 10), sticky="w"
        )
        self.username_entry = ctk.CTkEntry(
            form, width=210, placeholder_text="Enter username"
        )
        self.username_entry.grid(row=0, column=1, padx=20, pady=(25, 10))

        ctk.CTkLabel(form, text="Password :", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, padx=20, pady=10, sticky="w"
        )
        self.password_entry = ctk.CTkEntry(
            form, width=210, placeholder_text="Enter password", show="*"
        )
        self.password_entry.grid(row=1, column=1, padx=20, pady=10)

        # Buttons
        btn_f = ctk.CTkFrame(form, fg_color="transparent")
        btn_f.grid(row=2, column=0, columnspan=2, pady=(15, 20))

        ctk.CTkButton(
            btn_f,
            text="🔐 LOG IN",
            width=140,
            height=40,
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.do_login,
        ).grid(row=0, column=0, padx=15)

        ctk.CTkButton(
            btn_f,
            text="📝 SIGN UP",
            width=130,
            height=40,
            fg_color="#28a745",
            hover_color="#1e7e34",
            font=ctk.CTkFont(size=13),
            command=self.open_signup,
        ).grid(row=0, column=1, padx=15)

        self.bind("<Return>", lambda e: self.do_login())

    def do_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both fields!")
            return

        if role == "student":
            if validate_login(username, password):
                self.destroy()
                StudentDashboard(username=username).mainloop()
            else:
                messagebox.showerror("Login Error", "Invalid username or password!")
        else:
            if validate_admin(username, password):
                self.destroy()
                AdminDashboard().mainloop()
            else:
                messagebox.showerror("Login Error", "Invalid admin credentials!")

    def open_signup(self):
        self.destroy()
        SignupWindow().mainloop()
