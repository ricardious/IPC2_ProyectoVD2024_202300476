import tkinter as tk
from tkinter import messagebox


# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "AdminIPC" and password == "ARTIPC2":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")


# Create main window
root = tk.Tk()
root.title("IPCArt-Studio Login")
root.geometry("400x300")
root.configure(bg="#2c3e50")  # Background color

# Title label
label_title = tk.Label(
    root,
    text="Welcome to IPCArt-Studio",
    font=("Helvetica", 16, "bold"),
    fg="#ecf0f1",
    bg="#2c3e50",
)
label_title.pack(pady=20)

# Username field
frame_username = tk.Frame(root, bg="#2c3e50")
frame_username.pack(pady=10)
label_username = tk.Label(
    frame_username, text="Username:", font=("Helvetica", 12), fg="#ecf0f1", bg="#2c3e50"
)
label_username.pack(side=tk.LEFT, padx=10)
entry_username = tk.Entry(frame_username, font=("Helvetica", 12), width=20)
entry_username.pack(side=tk.LEFT)

# Password field
frame_password = tk.Frame(root, bg="#2c3e50")
frame_password.pack(pady=10)
label_password = tk.Label(
    frame_password, text="Password:", font=("Helvetica", 12), fg="#ecf0f1", bg="#2c3e50"
)
label_password.pack(side=tk.LEFT, padx=10)
entry_password = tk.Entry(frame_password, font=("Helvetica", 12), width=20, show="*")
entry_password.pack(side=tk.LEFT)

# Login button
login_button = tk.Button(
    root,
    text="Login",
    font=("Helvetica", 12, "bold"),
    fg="#ffffff",
    bg="#1abc9c",
    activebackground="#16a085",
    activeforeground="#ffffff",
    command=login,
)
login_button.pack(pady=20)

# Footer label
label_footer = tk.Label(
    root,
    text="© 2024 IPCArt-Studio",
    font=("Helvetica", 10),
    fg="#bdc3c7",
    bg="#2c3e50",
)
label_footer.pack(side=tk.BOTTOM, pady=10)

# Run the application
root.mainloop()
