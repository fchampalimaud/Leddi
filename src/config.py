import tkinter as tk
from tkinter import messagebox
import yaml
import os

# Function to load YAML data
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to save YAML data
def save_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file)

# Function to update YAML file with new values
def update_yaml():
    try:
        data['light_cycle']['start_time'] = str(start_entry.get())
        data['light_cycle']['cycles'] = int(cycles_entry.get())
        data['light_cycle']['on_duration'] = int(daytime_entry.get())
        data['light_cycle']['off_duration'] = int(nighttime_entry.get())
        save_yaml(yaml_file, data)
        messagebox.showinfo("Success", "YAML file updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update YAML file: {e}")

# Load initial YAML data
yaml_file = 'light_cycle_config.yaml'
data = load_yaml(yaml_file)

root = tk.Tk()
root.title("Leddi")

tk.Label(root, text="Light Cycle Configuration", font=("Helvetica", 16)).grid(row=0, columnspan=2)

tk.Label(root, text="").grid(row=1, column=0)

# Create and place labels and entries
tk.Label(root, text="Start Time:").grid(row=2, column=0)
start_entry = tk.Entry(root)
start_entry.grid(row=2, column=1)
start_entry.insert(0, data['light_cycle']['start_time'])

tk.Label(root, text="Number of Cycles:").grid(row=3, column=0)
cycles_entry = tk.Entry(root)
cycles_entry.grid(row=3, column=1)
cycles_entry.insert(0, data['light_cycle']['cycles'])

tk.Label(root, text="Daytime Duration:").grid(row=4, column=0)
daytime_entry = tk.Entry(root)
daytime_entry.grid(row=4, column=1)
daytime_entry.insert(0, data['light_cycle']['on_duration'])

tk.Label(root, text="Nighttime Duration:").grid(row=5, column=0)
nighttime_entry = tk.Entry(root)
nighttime_entry.grid(row=5, column=1)
nighttime_entry.insert(0, data['light_cycle']['off_duration'])


tk.Label(root, text="").grid(row=6, column=0)

update_button = tk.Button(root, text="Update", command=update_yaml)
update_button.grid(row=8, columnspan=2)

tk.Label(root, text="").grid(row=10, column=0)

root.mainloop()