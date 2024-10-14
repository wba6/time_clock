import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
import sys
from pathlib import Path

# Function to get the absolute path, works for both dev and PyInstaller
def get_base_path():
    """Get the base path of the application."""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundled exe
        base_path = Path(sys.executable).parent
    else:
        # If the application is run as a script
        base_path = Path(__file__).parent
    return base_path

# Function to get the path to the CSV file in the same directory as the exe/script
def get_csv_path():
    """Get the path for the CSV file in the application's base directory."""
    base_path = get_base_path()
    return base_path / 'time_log.csv'

# File where the data will be stored
CSV_FILE = get_csv_path()

# Initialize variables
clock_in_time = None

# Function to initialize the CSV file with headers if it doesn't exist
def initialize_csv():
    try:
        if not CSV_FILE.is_file():
            with open(str(CSV_FILE), mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Clock In', 'Clock Out', 'Duration'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize CSV file: {e}")
        sys.exit(1)

# Function to clock in
def clock_in():
    global clock_in_time
    if clock_in_time is not None:
        messagebox.showwarning("Warning", "You have already clocked in. Please clock out before clocking in again.")
        return
    clock_in_time = datetime.now()
    lbl_status.config(text=f"Clocked in at: {clock_in_time.strftime('%Y-%m-%d %H:%M:%S')}")
    btn_clock_in.config(state=tk.DISABLED)
    btn_clock_out.config(state=tk.NORMAL)

# Function to clock out
def clock_out():
    global clock_in_time
    if clock_in_time is None:
        messagebox.showwarning("Warning", "You haven't clocked in yet.")
        return
    clock_out_time = datetime.now()
    duration = clock_out_time - clock_in_time
    duration_str = str(duration).split('.')[0]  # Remove microseconds
    date_str = clock_in_time.strftime('%Y-%m-%d')
    clock_in_str = clock_in_time.strftime('%H:%M:%S')
    clock_out_str = clock_out_time.strftime('%H:%M:%S')

    # Write to CSV
    try:
        with open(str(CSV_FILE), mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([date_str, clock_in_str, clock_out_str, duration_str])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write to CSV file: {e}")
        return

    lbl_status.config(text=f"Clocked out at: {clock_out_time.strftime('%Y-%m-%d %H:%M:%S')}\nDuration: {duration_str}")
    clock_in_time = None
    btn_clock_in.config(state=tk.NORMAL)
    btn_clock_out.config(state=tk.DISABLED)
    messagebox.showinfo("Info", f"Clock out successful!\nDuration: {duration_str}")

# Initialize the CSV file
initialize_csv()

# Set up the main application window
root = tk.Tk()
root.title("Simple Time Tracker")
root.geometry("400x200")
root.resizable(False, False)

# Create and place the Clock In button
btn_clock_in = tk.Button(root, text="Clock In", font=("Helvetica", 14), width=15, command=clock_in)
btn_clock_in.pack(pady=20)

# Create and place the Clock Out button
btn_clock_out = tk.Button(root, text="Clock Out", font=("Helvetica", 14), width=15, command=clock_out,
                          state=tk.DISABLED)
btn_clock_out.pack(pady=10)

# Label to show status messages
lbl_status = tk.Label(root, text="Please clock in to start tracking your time.", font=("Helvetica", 10))
lbl_status.pack(pady=10)

# Run the application
root.mainloop()
