import tkinter as tk
from tkinter import messagebox
import subprocess

def login():
    username = username_entry.get()
    password = password_entry.get()
    role = role_var.get()

    # Simulated login check (replace with DB check later)
    if username == "admin" and password == "admin123" and role == "admin":
        open_dashboard(username, role)
    elif username == "user" and password == "user123" and role == "user":
        open_dashboard(username, role)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials or role selected.")

def open_dashboard(username, role):
    window.destroy()
    subprocess.run(["python", "dashboard.py", username, role])

# UI Setup
window = tk.Tk()
window.title("Login")
window.geometry("400x350")
window.config(bg="#1c1c1c")

tk.Label(window, text="CLUB LOGIN", font=("Segoe UI", 18, "bold"), fg="#00ffff", bg="#1c1c1c").pack(pady=20)

tk.Label(window, text="Username", fg="white", bg="#1c1c1c").pack()
username_entry = tk.Entry(window)
username_entry.pack(pady=5)

tk.Label(window, text="Password", fg="white", bg="#1c1c1c").pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack(pady=5)

tk.Label(window, text="Select Role", fg="white", bg="#1c1c1c").pack()
role_var = tk.StringVar(value="user")
role_dropdown = tk.OptionMenu(window, role_var, "admin", "user")
role_dropdown.config(bg="#444", fg="white", width=10)
role_dropdown.pack(pady=10)

tk.Button(window, text="Login", command=login, bg="#00ffff", fg="black", width=15).pack(pady=20)

window.mainloop()