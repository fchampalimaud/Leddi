import tkinter as tk
from tkinter import messagebox
import json
import os

# Function to load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to save JSON data
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to update JSON file with new values
def update_json():
    try:
        data['light_cycle']['start_time'] = str(start_entry.get())
        data['light_cycle']['cycles'] = int(cycles_entry.get())
        data['light_cycle']['on_duration'] = int(daytime_entry.get())
        data['light_cycle']['off_duration'] = int(nighttime_entry.get())
        save_json(json_file, data)
        messagebox.showinfo("Success", "JSON file updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update JSON file: {e}")

# Load initial JSON data
json_file = 'light_cycle_config.json'
data = load_json(json_file)

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

update_button = tk.Button(root, text="Update", command=update_json)
update_button.grid(row=8, columnspan=2)


# ------------------------------------------------------------
import serial
import time

# Initialize serial connection to COM5
ser = serial.Serial(
    port='COM5',        
    baudrate=115200,    # Same baud rate as ESP32 program
    timeout=1
)
# Check if the serial connection is open
if ser.is_open:
    print("Connection established on COM5")
else:
    ser.open()
    print("Opening serial connection on COM5")


def upload_config():
    try:
        response = ser.readline().decode().strip()
        if response:
            print(f"ESP32 Response: {response}")
        else:
            print("No response from ESP32")
        
        if ser.is_open:
            print(data)
            ser.write((json.dumps(data) + '\n').encode())
            print(f"Sent JSON data: {data}")
            response = ser.readline().decode().strip()
            response_2 = ser.readline().decode().strip()
            if response:
                print(f"ESP32 Response: {response}")
            else:
                print("No response from ESP32")
            if response_2:
                print(f"ESP32 Response: {response_2}")
        else:
            print("Serial port is not open")

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        ser.close()
        print("Serial connection closed")

upload_button = tk.Button(root, text="Upload Config", command=upload_config)
upload_button.grid(row=9, columnspan=2)

tk.Label(root, text="").grid(row=10, column=0)



root.mainloop()
