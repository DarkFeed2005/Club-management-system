from customtkinter import *
import mysql.connector
from tkinter import messagebox
from functools import partial

# ---------- App Initialization ----------
app = CTk()
app.title("User Dashboard - Join the Club")
app.geometry("750x600+650+250")
app.resizable(False, False)

# ---------- Theme Switch ----------
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
CTkLabel(switch_frame, text="Toggle Theme 🌗").pack(side="left", padx=10)
CTkSwitch(switch_frame, command=toggle_theme).pack(side="left")

# ---------- Connect to Database ----------
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

# ---------- Username Logic ----------
USER = "kalana"  # Replace with login module

cursor.execute("SELECT id FROM users WHERE username = %s", (USER,))
user_id_row = cursor.fetchone()
if not user_id_row:
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (USER,))
    db.commit()
    cursor.execute("SELECT id FROM users WHERE username = %s", (USER,))
user_id = user_id_row[0] if user_id_row else cursor.fetchone()[0]

# ---------- Dashboard Title ----------
CTkLabel(app, text=f"Welcome {USER.capitalize()}", font=("Arial Bold", 22), text_color="#0A6375").pack(pady=10)

# ---------- Available Clubs ----------
CTkLabel(app, text="Available Clubs", font=("Arial Bold", 18), text_color="#0A6375").pack(pady=10)
club_list = CTkScrollableFrame(app, width=700, height=200)
club_list.pack()

def enroll_in_club(club_id, club_name):
    cursor.execute("SELECT * FROM enrollments WHERE user_id=%s AND club_id=%s", (user_id, club_id))
    if cursor.fetchone():
        messagebox.showinfo("Already Enrolled", f"You're already in '{club_name}'.")
        return
    cursor.execute("INSERT INTO enrollments (user_id, club_id) VALUES (%s, %s)", (user_id, club_id))
    db.commit()
    load_my_clubs()

def load_clubs():
    for widget in club_list.winfo_children():
        widget.destroy()
    cursor.execute("SELECT id, name FROM clubs")
    for cid, cname in cursor.fetchall():
        box = CTkFrame(master=club_list)
        box.pack(pady=5, padx=10, fill="x")
        CTkLabel(box, text=cname, font=("Arial Bold", 14)).pack(side="left", padx=10)
        CTkButton(box, text="Join", width=80, command=partial(enroll_in_club, cid, cname)).pack(side="right", padx=10)

# ---------- My Clubs & Notifications ----------
CTkLabel(app, text="My Clubs & Notifications", font=("Arial Bold", 18), text_color="#0A6375").pack(pady=10)
my_club_list = CTkScrollableFrame(app, width=700, height=280)
my_club_list.pack()

def leave_club(club_id):
    cursor.execute("DELETE FROM enrollments WHERE user_id = %s AND club_id = %s", (user_id, club_id))
    db.commit()
    load_my_clubs()

def open_club_details(club_id, club_name):
    top = CTkToplevel(app)
    top.title(f"{club_name} Details")
    top.geometry("800x500")
    CTkLabel(top, text=f"{club_name} - Dashboard", font=("Arial Bold", 20), text_color="#0A6375").pack(pady=10)

    # ---------- Messages 📌 ----------
    CTkLabel(top, text="Messages 📌", font=("Arial Bold", 16)).pack(pady=5)
    msg_frame = CTkScrollableFrame(top, width=600, height=100)
    msg_frame.pack()
    cursor.execute("SELECT content FROM messages WHERE club_id = %s", (club_id,))
    for (text,) in cursor.fetchall():
        CTkLabel(msg_frame, text=f"- {text}").pack(anchor="w")

    # ---------- Events 📅 ----------
    CTkLabel(top, text="Upcoming Events 📅", font=("Arial Bold", 16)).pack(pady=5)
    evt_frame = CTkScrollableFrame(top, width=600, height=100)
    evt_frame.pack()
    cursor.execute("SELECT title FROM events WHERE club_id = %s", (club_id,))
    for (evt,) in cursor.fetchall():
        CTkLabel(evt_frame, text=f"- {evt}").pack(anchor="w")

def load_my_clubs():
    for widget in my_club_list.winfo_children():
        widget.destroy()
    cursor.execute("""
        SELECT c.id, c.name
        FROM clubs c
        JOIN enrollments e ON c.id = e.club_id
        WHERE e.user_id = %s
    """, (user_id,))
    for cid, cname in cursor.fetchall():
        box = CTkFrame(master=my_club_list)
        box.pack(pady=5, padx=10, fill="x")
        CTkLabel(box, text=cname, font=("Arial Bold", 14)).pack(side="left", padx=10)
        CTkButton(box, text="View", width=80, command=partial(open_club_details, cid, cname)).pack(side="right", padx=10)
        CTkButton(box, text="Leave", width=80, command=partial(leave_club, cid)).pack(side="right")

load_clubs()
load_my_clubs()
app.mainloop()