import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import importlib.util

# List of python scripts to choose from 
scripts = [
    "CleanScript.py",
    "Renamer.py",
    "FilesCopy.py",
    "ResorcesWriting.py",
    "ShopSettingsWriting.py",
    "ObjectLibraryWriter.py",
]

def check_and_install_module(module_name):
    """Check if a module is installed, and if not, install it."""
    if importlib.util.find_spec(module_name) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

def run_selected_scripts(selected_scripts):
    python_executable = sys.executable
    for script in selected_scripts:
        try:
            subprocess.run([python_executable, script], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running {script}:\n{e}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {script}")

def on_run():
    selected_scripts = [scripts[i] for i in range(len(scripts)) if var[i].get()]
    if not selected_scripts:
        messagebox.showwarning("Warning", "No scripts selected!")
    else:
        # Checking and installing lxml module if needed
        check_and_install_module("lxml")
        
        run_selected_scripts(selected_scripts)
        messagebox.showinfo("Info", "Selected scripts have been run.")

# Create the main window
root = tk.Tk()
root.title("Select Scripts to Run")

# Set the window size and center it on the screen
window_width = 300
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Define font size for the elements
font_style = ("Helvetica", 10)  # You can change the font family and size as needed

# Create a frame to hold the checkbuttons and center everything
frame = tk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

# Create checkbuttons for each script and center them, increase font size
var = [tk.BooleanVar() for _ in scripts]
for i, script in enumerate(scripts):
    chk = tk.Checkbutton(frame, text=script, variable=var[i], font=font_style)
    chk.pack(anchor=tk.CENTER, pady=5)

# Create the run button and center it, increase font size
run_button = tk.Button(frame, text="Run Selected Scripts", command=on_run, font=font_style)
run_button.pack(pady=20)

# Run the application
root.mainloop()
