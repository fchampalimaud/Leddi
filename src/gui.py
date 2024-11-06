import tkinter as tk
from tkinter import messagebox
from json_utils import *

class GUI(object):
    def __init__(self, esp32):
        self.window = tk.Tk()
        self.window.title("Leddi")

        self.esp32 = esp32

    def window_aspect(self, json_file = 'light_cycle_config.json'):
        data = load_json(json_file)

        tk.Label(self.window, text="Light Cycle Configuration", font=("Helvetica", 16)).grid(row=0, columnspan=2, sticky='e')
        tk.Label(self.window, text="").grid(row=1, column=0, sticky='e')

        # Create and place labels and entries
        tk.Label(self.window, text="Start Time:").grid(row=2, column=0, sticky='e')
        self.start_entry = tk.Entry(self.window)
        self.start_entry.grid(row=2, column=1, sticky='e')
        self.start_entry.insert(0, data['light_cycle']['start_time'])

        tk.Label(self.window, text="Number of Cycles:").grid(row=3, column=0, sticky='e')
        self.cycles_entry = tk.Entry(self.window)
        self.cycles_entry.grid(row=3, column=1, sticky='e')
        self.cycles_entry.insert(0, data['light_cycle']['cycles'])

        tk.Label(self.window, text="Daytime Duration:").grid(row=4, column=0, sticky='e')
        self.daytime_entry = tk.Entry(self.window)
        self.daytime_entry.grid(row=4, column=1, sticky='e')
        self.daytime_entry.insert(0, data['light_cycle']['on_duration'])

        tk.Label(self.window, text="Nighttime Duration:").grid(row=5, column=0, sticky='e')
        self.nighttime_entry = tk.Entry(self.window)
        self.nighttime_entry.grid(row=5, column=1, sticky='e')
        self.nighttime_entry.insert(0, data['light_cycle']['off_duration'])

        tk.Label(self.window, text="Init Time Lag:").grid(row=6, column=0, sticky='e')
        self.init_time_lag_entry = tk.Entry(self.window)
        self.init_time_lag_entry.grid(row=6, column=1, sticky='e')
        self.init_time_lag_entry.insert(0, data['light_cycle']['delay_before_start'])

        tk.Label(self.window, text="Sunrise Duration:").grid(row=7, column=0, sticky='e')
        self.sunrise_duration_entry = tk.Entry(self.window)
        self.sunrise_duration_entry.grid(row=7, column=1, sticky='e')
        self.sunrise_duration_entry.insert(0, data['light_cycle']['fade_in_duration'])

        tk.Label(self.window, text="Sunset Duration:").grid(row=8, column=0, sticky='e')
        self.sunset_duration_entry = tk.Entry(self.window)
        self.sunset_duration_entry.grid(row=8, column=1, sticky='e')
        self.sunset_duration_entry.insert(0, data['light_cycle']['fade_out_duration'])

        tk.Label(self.window, text="").grid(row=9, column=0, sticky='e')

        upload_button = tk.Button(self.window, text="Update", command=lambda: self.upload_json(json_file))
        upload_button.grid(row=10, columnspan=2)

        tk.Label(self.window, text="").grid(row=11, column=0, sticky='e')


    def upload_json(self, json_file = 'light_cycle_config.json'):
        # Update JSON file
        data = load_json(json_file)
        try:
            data['light_cycle']['start_time'] = str(self.start_entry.get())
            data['light_cycle']['cycles'] = int(self.cycles_entry.get())
            data['light_cycle']['on_duration'] = int(self.daytime_entry.get())
            data['light_cycle']['off_duration'] = int(self.nighttime_entry.get())
            data['light_cycle']['delay_before_start'] = int(self.init_time_lag_entry.get())
            data['light_cycle']['fade_in_duration'] = int(self.sunrise_duration_entry.get())
            data['light_cycle']['fade_out_duration'] = int(self.sunset_duration_entry.get())
            save_json(json_file, data)
            messagebox.showinfo("Success", "JSON file updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update JSON file: {e}")
        
        # Upload JSON data to ESP32 FLASH memory
        json_data = json.dumps(data)
        self.esp32.upload_config(json_data)
