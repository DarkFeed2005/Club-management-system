from customtkinter import *
import subprocess
import sys

# ---------- App Setup ----------
app = CTk()
app.title("Club Management System")
app.geometry("600x400+650+300")
app.resizable(False, False)

# ---------- Theme Toggle ----------
theme_mode = StringVar(value="dark")
def toggle_theme():
    if theme_mode.get() == "dark":
        set_appearance_mode("light")
        theme_mode.set("light")
    else:
        set_appearance_mode("dark")
        theme_mode.set("dark")

switch_frame = CTkFrame(app)
switch_frame.pack(pady=5)
CTkLabel(switch_frame, text="Theme 🌗").pack(side="left", padx=10)
CTkSwitch(switch_frame, command=toggle_theme).pack(side="left")

# ---------- Branding & Description ----------
CTkLabel(app, text="Welcome to ClubVerse", font=("Arial Bold", 24), text_color="#601E88").pack(pady=20)

desc = """Join the ClubVerse — where passion meets opportunity! 🎉
Manage clubs, connect with members, explore events, and stay updated.
Built for students. Designed by Kalana. Powered with simplicity."""
CTkLabel(app, text=desc, wraplength=500, justify="center", font=("Arial", 15)).pack(pady=10)

# ---------- Navigation Buttons ----------
def open_login():
    subprocess.Popen([sys.executable, "login.py"])
    app.destroy()

def open_signup():
    subprocess.Popen([sys.executable, "signup.py"])
    app.destroy()

CTkButton(app, text="Login", command=open_login, width=200).pack(pady=10)
CTkButton(app, text="Sign Up", command=open_signup, width=200).pack()

app.mainloop()