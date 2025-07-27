from customtkinter import *
from PIL import Image, ImageTk, ImageSequence
import subprocess
import mysql.connector
import re
from tkinter import messagebox

# --------- DB Connection ---------
try:
    db = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12792132",
        password="JNjxJIR6et",
        database="sql12792132"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Connection Failed: {err}")
    exit()

# --------- Email Format Check ---------
def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# --------- Main Window ---------
app = CTk()
app.iconbitmap("img/app_icon.ico")
app.title("Sign-Up - Join the Club")
app.geometry("700x600+650+300")
app.resizable(False, False)

# --------- Load Icons ---------
user_icon = CTkImage(Image.open("img/email-icon.png"), size=(20, 20))
pass_icon = CTkImage(Image.open("img/password-icon.png"), size=(17, 17))
back_icon = CTkImage(Image.open("img/signup-icon.png"), size=(17, 17))

# --------- Animated GIF ---------
frames = [
    ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((480, 780)))
    for frame in ImageSequence.Iterator(Image.open("img/animated2.gif"))
]
def animate_gif(counter=0):
    gif_label.configure(image=frames[counter])
    app.after(100, lambda: animate_gif((counter + 1) % len(frames)))

gif_label = CTkLabel(master=app, text="")
gif_label.pack(expand=True, side="left")
animate_gif()

# --------- Right-side Frame ---------
frame = CTkFrame(master=app, width=400, height=780, fg_color="#ffffff")
frame.pack_propagate(False)
frame.pack(expand=True, side="right")

# --------- Form Labels ---------
CTkLabel(frame, text="Create Account", text_color="#601E88", font=("Arial Bold", 24)).pack(anchor="w", pady=(20, 5), padx=(25, 0))
CTkLabel(frame, text="Register with your details", text_color="#7E7E7E", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

# --------- Form Entries ---------
CTkLabel(frame, text="  Email Address:", text_color="#601E88", font=("Arial Bold", 14)).pack(anchor="w", pady=(10, 0), padx=(25, 0))
email_entry = CTkEntry(frame, width=225, fg_color="#EEEEEE", border_color="#601E88", text_color="#000000")
email_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(frame, text="  User Name:", text_color="#601E88", font=("Arial Bold", 14), image=user_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
username_entry = CTkEntry(frame, width=225, fg_color="#EEEEEE", border_color="#601E88", text_color="#000000")
username_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(frame, text="  Password:", text_color="#601E88", font=("Arial Bold", 14), image=pass_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
password_entry = CTkEntry(frame, width=225, fg_color="#EEEEEE", border_color="#601E88", text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(frame, text="  Confirm Password:", text_color="#601E88", font=("Arial Bold", 14), image=pass_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
confirm_entry = CTkEntry(frame, width=225, fg_color="#EEEEEE", border_color="#601E88", text_color="#000000", show="*")
confirm_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(frame, text="  Select Role:", text_color="#601E88", font=("Arial Bold", 14)).pack(anchor="w", pady=(10, 0), padx=(25, 0))
role_option = StringVar(value="User")
role_menu = CTkOptionMenu(frame, values=["User", "Admin"], variable=role_option,
                          width=225, fg_color="#EEEEEE", button_color="#C7BCCE",
                          text_color="#000000", dropdown_hover_color="#E44982")
role_menu.pack(anchor="w", padx=(25, 0))

# --------- Status Label ---------
status_label = CTkLabel(master=frame, text="", text_color="red")
status_label.pack(anchor="w", pady=(10, 0), padx=(25, 0))

# --------- Register Function ---------
def register_user():
    email = email_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    confirm = confirm_entry.get().strip()
    role = role_option.get()

    if not email or not username or not password or not confirm:
        status_label.configure(text="❗ All fields must be filled", text_color="red")
        return
    if not valid_email(email):
        status_label.configure(text="❌ Invalid email format", text_color="red")
        return
    if password != confirm:
        status_label.configure(text="❌ Passwords don't match", text_color="red")
        return

    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        status_label.configure(text="⚠️ Email already exists", text_color="orange")
        return

    try:
        cursor.execute("INSERT INTO users (email, username, password, role) VALUES (%s, %s, %s, %s)",
                       (email, username, password, role))
        db.commit()
        status_label.configure(text="✅ Account created successfully!", text_color="green")
        email_entry.delete(0, 'end')
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        confirm_entry.delete(0, 'end')
        role_option.set("User")
        app.destroy()
        subprocess.Popen(["python", "dashboard.py"])
    except mysql.connector.Error as err:
        status_label.configure(text=f"❌ DB Error: {err}", text_color="red")

# --------- Buttons ---------
CTkButton(frame, text="Sign Up", fg_color="#601E88", hover_color="#E44982",
          font=("Arial Bold", 24), text_color="#ffffff", width=225,
          command=register_user).pack(anchor="w", pady=(10, 0), padx=(25, 0))

def reset_password():
    status_label.configure(text="🔄 Password reset not yet implemented", text_color="#7E7E7E")

CTkButton(frame, text="Reset Password", fg_color="#EEEEEE", hover_color="#919191",
          font=("Arial Bold", 9), text_color="#601E88", width=225,
          command=reset_password).pack(anchor="w", pady=(5, 0), padx=(25, 0))

def open_login_page():
    app.destroy()
    subprocess.Popen(["python", "login.py"])

CTkButton(frame, text="Back to Login", fg_color="#EEEEEE", hover_color="#919191",
          font=("Arial Bold", 9), text_color="#601E88", width=225, image=back_icon,
          command=open_login_page).pack(anchor="w", pady=(5, 0), padx=(25, 0))

app.mainloop()