from customtkinter import *
from PIL import Image, ImageTk, ImageSequence
import mysql.connector
import subprocess
from tkinter import messagebox

# ---------- Main Window ----------
app = CTk()
app.iconbitmap("img/app_icon.ico")
app.title("Sign-In - Join the Club")
app.geometry("700x480+650+300")
app.resizable(False, False)

# ---------- Load Icons ----------
email_icon = CTkImage(Image.open("img/email-icon.png"), size=(20, 20))
password_icon = CTkImage(Image.open("img/password-icon.png"), size=(17, 17))
signup_icon = CTkImage(Image.open("img/signup-icon.png"), size=(17, 17))

# ---------- Load Animated GIF ----------
frames = [
    ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((480, 600)))
    for frame in ImageSequence.Iterator(Image.open("img/animated.gif"))
]

def animate_gif(counter=0):
    gif_label.configure(image=frames[counter])
    app.after(100, lambda: animate_gif((counter + 1) % len(frames)))

gif_label = CTkLabel(app, text="")
gif_label.pack(expand=True, side="left")
animate_gif()

# ---------- Right-side Login Frame ----------
frame = CTkFrame(app, width=400, height=480, fg_color="#ffffff")
frame.pack_propagate(False)
frame.pack(expand=True, side="right")

CTkLabel(frame, text="Welcome Back!", text_color="#601E88",
         font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(frame, text="Sign in to your account", text_color="#7E7E7E",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

# ---------- Username Entry ----------
CTkLabel(frame, text="  User Name:", text_color="#601E88",
         font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
username_entry = CTkEntry(frame, width=225, fg_color="#EEEEEE",
                          border_color="#601E88", text_color="#000000")
username_entry.pack(anchor="w", padx=(25, 0))

# ---------- Password Entry ----------
CTkLabel(frame, text="  Password:", text_color="#601E88",
         font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
password_entry = CTkEntry(frame, width=225, fg_color="#EEEEEE",
                          border_color="#601E88", text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

# ---------- Role Selector ----------
CTkLabel(frame, text="  Select Role:", text_color="#601E88",
         font=("Arial Bold", 14)).pack(anchor="w", pady=(21, 0), padx=(25, 0))
role_menu = CTkOptionMenu(frame, values=["User", "Admin"], width=225)
role_menu.pack(anchor="w", padx=(25, 0))
role_menu.set("User")  # Default role

# ---------- Login Function ----------
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    selected_role = role_menu.get().lower()

    if not username or not password or not selected_role:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        db = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12792132",
            password="JNjxJIR6et",
            database="sql12792132"
        )
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s AND role = %s"
        cursor.execute(query, (username, password, selected_role))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", f"Welcome, {username} ({selected_role.title()})!")
            app.destroy()

            if selected_role == "admin":
                subprocess.Popen(["python", "admin_dashboard.py"])
            else:
                subprocess.Popen(["python", "user_dashboard.py", username])
        else:
            messagebox.showerror("Login Failed", "Invalid credentials or role mismatch.")

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# ---------- Login Button ----------
CTkButton(frame, text="Login", fg_color="#601E88", hover_color="#E44982",
          font=("Arial Bold", 12), text_color="#ffffff", width=225,
          command=login).pack(anchor="w", pady=(30, 0), padx=(25, 0))

# ---------- Redirect to Signup ----------
def open_signup_page():
    app.destroy()
    subprocess.Popen(["python", "signup.py"])

CTkButton(frame, text="Haven’t an account?", fg_color="#EEEEEE", hover_color="#919191",
          font=("Arial Bold", 9), text_color="#601E88", width=225, image=signup_icon,
          command=open_signup_page).pack(anchor="w", pady=(20, 0), padx=(25, 0))

app.mainloop()