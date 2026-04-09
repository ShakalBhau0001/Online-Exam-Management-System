import customtkinter as ctk
from tkinter import messagebox
from gui.login import LoginWindow
from core.db import username_exists, email_exists, insert_student


class SignupWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sign Up — New Student")
        self.geometry("520x540")
        self.resizable(False, False)
        self._center()
        self.build_ui()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"520x540+{(sw-520)//2}+{(sh-540)//2}")

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="📋 Student Registration",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4DA6FF",
        ).pack(pady=(30, 20))
        form = ctk.CTkFrame(self, corner_radius=15)
        form.pack(padx=40, pady=5, fill="both", expand=True)
        fields = [
            ("UserName :", False),
            ("Full Name :", False),
            ("Contact No :", False),
            ("Email :", False),
            ("Password :", True),
        ]
        self.entries = []
        for i, (label, is_pass) in enumerate(fields):
            ctk.CTkLabel(form, text=label, font=ctk.CTkFont(size=13)).grid(
                row=i, column=0, padx=25, pady=10, sticky="w"
            )
            e = ctk.CTkEntry(
                form,
                width=220,
                show="*" if is_pass else "",
                placeholder_text=label.replace(" :", "").strip(),
            )
            e.grid(row=i, column=1, padx=15, pady=10)
            self.entries.append(e)
        btn_f = ctk.CTkFrame(form, fg_color="transparent")
        btn_f.grid(row=len(fields), column=0, columnspan=2, pady=(15, 20))
        ctk.CTkButton(
            btn_f,
            text="✅ SUBMIT",
            width=130,
            height=38,
            fg_color="#28a745",
            hover_color="#1e7e34",
            command=self.submit,
        ).grid(row=0, column=0, padx=15)
        ctk.CTkButton(
            btn_f,
            text="⬅ BACK",
            width=100,
            height=38,
            fg_color="#6c757d",
            hover_color="#545b62",
            command=self.go_back,
        ).grid(row=0, column=1, padx=15)

    def submit(self):
        username, name, contact, email, password = [
            e.get().strip() for e in self.entries
        ]

        if not all([username, name, contact, email, password]):
            messagebox.showwarning("Input Error", "Please fill all fields!")
            return
        if not contact.isdigit():
            messagebox.showwarning("Input Error", "Contact No must be numeric!")
            return
        if "@" not in email or "." not in email:
            messagebox.showwarning("Input Error", "Enter a valid email!")
            return
        if len(password) < 6:
            messagebox.showwarning(
                "Input Error", "Password must be at least 6 characters!"
            )
            return
        if username_exists(username):
            messagebox.showerror("Error", f"Username '{username}' already taken!")
            return
        if email_exists(email):
            messagebox.showerror("Error", f"Email '{email}' already registered!")
            return

        if insert_student(username, name, contact, email, password):
            messagebox.showinfo("Success", "Registration Successful! ✅\nPlease login.")
            self.go_back()
        else:
            messagebox.showerror("Error", "Registration failed. Try again.")

    def go_back(self):
        self.destroy()
        LoginWindow().mainloop()
