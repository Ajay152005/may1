import tkinter as tk
from tkinter import messagebox
from database import execute_query, fetch
from ecommerce import ECommerceApp

def switch_to_signup():
    login_frame.place_forget()
    signup_frame.place(relx=0.5, rely=0.5, anchor="center")

def switch_to_login():
    signup_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

def login():
    username = username_entry.get()
    password = password_entry.get()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    result = fetch(query, (username, password))
    if result:
        messagebox.showinfo("Success", "Login successful!")
        root.withdraw()  # Hide the login window
        ecommerce_root = tk.Toplevel(root)  # Create a new Toplevel window
        app = ECommerceApp(ecommerce_root)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def signup():
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    execute_query(query, (username, password))
    messagebox.showinfo("Success", "Signup successful!")
    switch_to_login()  # Switch back to the login screen

def show_ecommerce_app(username):
    ecommerce_root = tk.Toplevel()
    app = ECommerceApp(ecommerce_root, username)

root = tk.Tk()
root.title("Login Page")
root.configure(bg="#CCCCCC")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate 80% of the screen dimensions
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

# Define colors
primary_color = "#4CAF50"
secondary_color = "#ffffff"
text_color = "#333333"
entry_bg_color = "#CCCCCC"

# Styling for labels, buttons, and entries
label_style = {"font": ("Helvetica", 16), "bg": secondary_color, "fg": text_color, "bd":0}
entry_style = {"font": ("Helvetica", 14), "bg": entry_bg_color, "relief": "flat"}
button_style = {"font": ("Helvetica", 16), "bg": primary_color, "activebackground": "#006400", "activeforeground": "#ffffff", "bd":0}

login_frame = tk.Frame(root, padx=20, pady=10)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

login_header = tk.Label(login_frame, text="Login Page", **label_style)
login_header.config(font=("Helvetica", 24, "bold"))
login_header.pack(pady=10)

username_label = tk.Label(login_frame, text="Username:", **label_style)
username_label.pack(pady=5)
username_entry = tk.Entry(login_frame, width=30, **entry_style)
username_entry.pack(pady=5)

password_label = tk.Label(login_frame, text="Password:", **label_style)
password_label.pack(pady=5)
password_entry = tk.Entry(login_frame, show="*", width=30, **entry_style)
password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=login, **button_style)
login_button.pack(pady=10)

signup_link = tk.Label(login_frame, text="Don't have an account? Sign up here", fg="blue", cursor="hand2")
signup_link.pack(pady=5)
signup_link.bind("<Button-1>", lambda e: switch_to_signup())

signup_frame = tk.Frame(root, padx=20, pady=10)

signup_header = tk.Label(signup_frame, text="Sign Up Page", **label_style)
signup_header.config(font=("Helvetica", 24, "bold"))
signup_header.pack(pady=10)

signup_username_label = tk.Label(signup_frame, text="Username:", **label_style)
signup_username_label.pack(pady=5)
signup_username_entry = tk.Entry(signup_frame, width=30, **entry_style)
signup_username_entry.pack(pady=5)

signup_password_label = tk.Label(signup_frame, text="Password:", **label_style)
signup_password_label.pack(pady=5)
signup_password_entry = tk.Entry(signup_frame, show="*", width=30, **entry_style)
signup_password_entry.pack(pady=5)

signup_button = tk.Button(signup_frame, text="Sign Up", command=signup, **button_style)
signup_button.pack(pady=10)

login_link = tk.Label(signup_frame, text="Already have an account? Login here", fg="blue", cursor="hand2")
login_link.pack(pady=5)
login_link.bind("<Button-1>", lambda e: switch_to_login())

welcome_frame = tk.Frame(root)

welcome_label = tk.Label(welcome_frame, **label_style)
welcome_label.config(font=("Helvetica", 20))
welcome_label.pack(padx=20, pady=10)

def switch_to_welcome():
    signup_frame.place_forget()
    login_frame.place_forget()
    welcome_frame.place(relx=0.5, rely=0.5, anchor="center")

def switch_to_login():
    welcome_frame.place_forget()
    signup_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

def switch_to_signup():
    welcome_frame.place_forget()
    login_frame.place_forget()
    signup_frame.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()
