
# 🏫 ClubVerse – Club Management System

Welcome to **ClubVerse**, a full-stack Club Management System built with Python, MySQL, and CustomTkinter. Designed to empower students and admins to explore, manage, and participate in extracurricular communities effortlessly.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-Dynamic-Orange?logo=mysql)
![UI Toolkit](https://img.shields.io/badge/CustomTkinter-Stylish%20UI-purple?logo=tkinter)
![License](https://img.shields.io/github/license/your-username/club-management-system)

---

## 🎯 Features

### 👥 User Dashboard
- Browse & join clubs with live enrollment
- See your enrolled clubs, events, and messages
- 🔔 Get real-time club notifications
- Toggle between 🔦 Dark/Light Mode

### 🧑‍💼 Admin Dashboard
- Add, view, and delete clubs with scrollable UI
- Manage enrolled students for each club
- Post events and important messages
- Cleanly remove clubs and all dependencies

### 🔐 Login System
- Role-based access: Admin or User
- Credentials stored securely in database
- Navigation from a welcoming landing page

### 📝 Sign Up Module
- Register new users with email, password, and profile image
- Ready for extension: password hashing, validation, and roles

---

## 🗄️ Technologies Used

| Layer        | Tools & Frameworks             |
|-------------|--------------------------------|
| Language     | Python                         |
| UI           | CustomTkinter (Dark/Light Mode)|
| Database     | MySQL (with ON DELETE CASCADE) |
| Auth         | Username/Password (plaintext now)|
| Navigation   | Tkinter subprocess for module routing|

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/your-username/club-management-system
cd club-management-system
pip install customtkinter mysql-connector-python
python main.py