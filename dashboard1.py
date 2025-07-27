from customtkinter import *
from tkinter import messagebox
import json
import subprocess
import os

# -------- Read session data --------
try:
    with open("session.json", "r") as f:
        session = json.load(f)
        username = session.get("username", "Unknown")
        role = session.get("role", "Unknown")
except (FileNotFoundError, json.JSONDecodeError):
    username = "Unknown"
    role = "Unknown"

# -------- Dashboard UI --------
app = CTk()
app.title("Dashboard - Join the Club")
app.geometry("700x480+650+300")
app.resizable(False, False)

# -------- Header --------
CTkLabel(app, text=f"Welcome {username}!",
         font=("Arial Bold", 22), text_color="#601E88").pack(pady=(30, 10))
CTkLabel(app, text=f"You are logged in as: {role}",
         font=("Arial", 14), text_color="#7E7E7E").pack()

# -------- Role-specific Content --------
if role == "Admin":
    CTkLabel(app, text="Admin Panel",
             font=("Arial", 16), text_color="#E44982").pack(pady=(40, 5))
    CTkButton(app, text="Manage Users", fg_color="#601E88", hover_color="#E44982",
              width=200).pack(pady=10)
    CTkButton(app, text="View Reports", fg_color="#601E88", hover_color="#E44982",
              width=200).pack(pady=10)

elif role == "User":
    CTkLabel(app, text="User Dashboard",
             font=("Arial", 16), text_color="#3A8F3A").pack(pady=(40, 5))
    CTkButton(app, text="Browse Content", fg_color="#3A8F3A", hover_color="#45C945",
              width=200).pack(pady=10)
    CTkButton(app, text="Edit Profile", fg_color="#3A8F3A", hover_color="#45C945",
              width=200).pack(pady=10)

else:
    CTkLabel(app, text="Unknown Role",
             font=("Arial", 16), text_color="gray").pack(pady=(40, 5))

# -------- Logout Function --------
def logout():
    try:
        os.remove("session.json")  # Delete session file
    except FileNotFoundError:
        pass  # Already cleared
    except Exception as e:
        messagebox.showerror("Logout Error", str(e))
    finally:
        app.destroy()
        subprocess.Popen(["python", "login.py"])  # Relaunch login screen

CTkButton(app, text="Logout", fg_color="#EEEEEE", hover_color="#919191",
          text_color="#601E88", width=120, command=logout).pack(pady=(60, 10))

app.mainloop()