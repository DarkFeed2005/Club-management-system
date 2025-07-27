from customtkinter import *
import mysql.connector
from tkinter import messagebox
from functools import partial

# ---------- App Config ----------
app = CTk()
app.title("Admin Dashboard - Join the Club")
app.geometry("750x600+650+250")
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
CTkLabel(switch_frame, text="Toggle Theme 🌗").pack(side="left", padx=10)
CTkSwitch(switch_frame, command=toggle_theme).pack(side="left")

# ---------- Database Connection ----------
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

# ---------- Header ----------
CTkLabel(app, text="Admin Control Panel", font=("Arial Bold", 22), text_color="#601E88").pack(pady=10)

# ---------- Add Club ----------
club_entry = CTkEntry(app, placeholder_text="Enter new club name", width=400)
club_entry.pack(pady=10)

def add_club():
    name = club_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Club name cannot be empty.")
        return
    try:
        cursor.execute("INSERT INTO clubs (name) VALUES (%s)", (name,))
        db.commit()
        messagebox.showinfo("Success", f"✅ '{name}' added.")
        club_entry.delete(0, 'end')
        load_clubs()
    except:
        messagebox.showwarning("Warning", "⚠️ Club may already exist.")

CTkButton(app, text="Add Club", command=add_club, fg_color="#601E88", text_color="white").pack()

# ---------- Club List Scroll ----------
CTkLabel(app, text="All Clubs", font=("Arial Bold", 18), text_color="#601E88").pack(pady=10)
club_list = CTkScrollableFrame(app, width=700, height=350)
club_list.pack()

def delete_club(club_id, club_name):
    confirm = messagebox.askyesno("Confirm", f"Delete '{club_name}' and all related data?")
    if confirm:
        try:
            cursor.execute("DELETE FROM enrollments WHERE club_id = %s", (club_id,))
            cursor.execute("DELETE FROM events WHERE club_id = %s", (club_id,))
            cursor.execute("DELETE FROM messages WHERE club_id = %s", (club_id,))
            cursor.execute("DELETE FROM clubs WHERE id = %s", (club_id,))
            db.commit()
            messagebox.showinfo("Deleted", f"'{club_name}' and all dependencies removed.")
            load_clubs()
        except mysql.connector.Error as err:
            messagebox.showerror("Delete Error", f"Could not delete club:\n{err}")

def view_club_details(club_id, club_name):
    top = CTkToplevel(app)
    top.title(f"{club_name} Details")
    top.geometry("800x500")
    CTkLabel(top, text=f"{club_name} Dashboard", font=("Arial Bold", 20), text_color="#601E88").pack(pady=10)

    # ---------- Enrolled Students ----------
    cursor.execute("""SELECT username FROM users
                      JOIN enrollments ON users.id = enrollments.user_id
                      WHERE enrollments.club_id = %s""", (club_id,))
    members = cursor.fetchall()
    CTkLabel(top, text="Enrolled Students", font=("Arial Bold", 16)).pack()
    member_list = CTkScrollableFrame(top, width=400, height=100)
    member_list.pack(pady=5)
    for (name,) in members:
        box = CTkFrame(master=member_list)
        box.pack(pady=2, fill="x", padx=10)
        CTkLabel(box, text=name).pack(side="left")
        CTkButton(box, text="Remove", width=80, command=partial(remove_user, club_id, name)).pack(side="right")

    # ---------- Event and Message Inputs ----------
    section = CTkFrame(top)
    section.pack(pady=10)

    event_entry = CTkEntry(section, placeholder_text="Add Event or Session", width=300)
    event_entry.pack(side="left", padx=10)
    CTkButton(section, text="Add", command=lambda: add_event(club_id, event_entry.get())).pack(side="left")

    message_entry = CTkEntry(top, placeholder_text="Add Important Message", width=400)
    message_entry.pack(pady=5)
    CTkButton(top, text="Add Message", command=lambda: add_message(club_id, message_entry.get())).pack()

def remove_user(club_id, username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM enrollments WHERE user_id = %s AND club_id = %s", (user_id, club_id))
    db.commit()
    messagebox.showinfo("Removed", f"{username} removed from club.")
    load_clubs()

def add_event(club_id, text):
    if text.strip():
        cursor.execute("INSERT INTO events (club_id, title) VALUES (%s, %s)", (club_id, text.strip()))
        db.commit()
        messagebox.showinfo("Event Added", f"📅 {text.strip()} saved.")

def add_message(club_id, text):
    if text.strip():
        cursor.execute("INSERT INTO messages (club_id, content) VALUES (%s, %s)", (club_id, text.strip()))
        db.commit()
        messagebox.showinfo("Message Posted", "📌 Message added.")

def load_clubs():
    for widget in club_list.winfo_children():
        widget.destroy()
    cursor.execute("SELECT id, name FROM clubs")
    for club_id, club_name in cursor.fetchall():
        box = CTkFrame(master=club_list)
        box.pack(pady=5, padx=10, fill="x")
        CTkLabel(box, text=club_name, font=("Arial Bold", 14)).pack(side="left", padx=10)
        CTkButton(box, text="Go", width=60, command=partial(view_club_details, club_id, club_name)).pack(side="right", padx=5)
        CTkButton(box, text="Delete", width=60, command=partial(delete_club, club_id, club_name)).pack(side="right", padx=5)

# ---------- Create Tables with Foreign Keys ----------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        club_id INT,
        title VARCHAR(255),
        FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        club_id INT,
        content TEXT,
        FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        club_id INT,
        FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
    )
""")
db.commit()
load_clubs()

app.mainloop()