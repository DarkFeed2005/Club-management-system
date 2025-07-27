from database import init_db
from login import login_screen
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

init_db()
login_screen()