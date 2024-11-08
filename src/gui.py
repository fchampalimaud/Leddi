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

        tk.Label(self.window, text="Light Cycle Configuration", font=("Helvetica", 16)).grid(row=0, columnspan=3)
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
        
        # Daytime Duration Unit
        self.daytime_unit = tk.StringVar(self.window)
        self.daytime_unit.set("sec")
        self.daytime_unit_menu = tk.OptionMenu(self.window, self.daytime_unit, "sec", "min", "hrs")
        self.daytime_unit_menu.grid(row=4, column=2, sticky='e')

        # Nighttime Duration Unit
        tk.Label(self.window, text="Nighttime Duration:").grid(row=5, column=0, sticky='e')
        self.nighttime_entry = tk.Entry(self.window)
        self.nighttime_entry.grid(row=5, column=1, sticky='e')
        self.nighttime_entry.insert(0, data['light_cycle']['off_duration'])

        self.nighttime_unit = tk.StringVar(self.window)
        self.nighttime_unit.set("sec")
        self.nighttime_unit_menu = tk.OptionMenu(self.window, self.nighttime_unit, "sec", "min", "hrs")
        self.nighttime_unit_menu.grid(row=5, column=2, sticky='e')

        # Sunrise Duration Unit
        tk.Label(self.window, text="Sunrise Duration:").grid(row=7, column=0, sticky='e')
        self.sunrise_duration_entry = tk.Entry(self.window)
        self.sunrise_duration_entry.grid(row=7, column=1, sticky='e')
        self.sunrise_duration_entry.insert(0, data['light_cycle']['fade_in_duration'])

        self.sunrise_unit = tk.StringVar(self.window)
        self.sunrise_unit.set("sec")
        self.sunrise_unit_menu = tk.OptionMenu(self.window, self.sunrise_unit, "sec", "min", "hrs")
        self.sunrise_unit_menu.grid(row=7, column=2, sticky='e')

        # Sunset Duration Unit
        tk.Label(self.window, text="Sunset Duration:").grid(row=8, column=0, sticky='e')
        self.sunset_duration_entry = tk.Entry(self.window)
        self.sunset_duration_entry.grid(row=8, column=1, sticky='e')
        self.sunset_duration_entry.insert(0, data['light_cycle']['fade_out_duration'])

        self.sunset_unit = tk.StringVar(self.window)
        self.sunset_unit.set("sec")
        self.sunset_unit_menu = tk.OptionMenu(self.window, self.sunset_unit, "sec", "min", "hrs")
        self.sunset_unit_menu.grid(row=8, column=2, sticky='e')

        tk.Label(self.window, text="Nighttime Duration:").grid(row=5, column=0, sticky='e')
        self.nighttime_entry = tk.Entry(self.window)
        self.nighttime_entry.grid(row=5, column=1, sticky='e')
        self.nighttime_entry.insert(0, data['light_cycle']['off_duration'])

        tk.Label(self.window, text="Init Time Lag:").grid(row=6, column=0, sticky='e')
        self.init_time_lag_entry = tk.Entry(self.window)
        self.init_time_lag_entry.grid(row=6, column=1, sticky='e')
        self.init_time_lag_entry.insert(0, data['light_cycle']['delay_before_start'])
      
        self.init_time_lag_unit = tk.StringVar(self.window)
        self.init_time_lag_unit.set("sec")
        self.init_time_lag_unit_menu = tk.OptionMenu(self.window, self.init_time_lag_unit, "sec", "min", "hrs")
        self.init_time_lag_unit_menu.grid(row=6, column=2, sticky='e')

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
        upload_button.grid(row=10, columnspan=3)

        tk.Label(self.window, text="").grid(row=11, column=0, sticky='e')


    def upload_json(self, json_file = 'light_cycle_config.json'):
        # Update JSON file
        data = load_json(json_file)
        try:
            data['light_cycle']['start_time'] = str(self.start_entry.get())
            data['light_cycle']['cycles'] = int(self.cycles_entry.get())

            on_duration = int(self.daytime_entry.get())
            if self.daytime_unit.get() == "min":
                on_duration *= 60
            elif self.daytime_unit.get() == "hrs":
                on_duration *= 3600
            data['light_cycle']['on_duration'] = on_duration

            off_duration = int(self.nighttime_entry.get())
            if self.nighttime_unit.get() == "min":
                off_duration *= 60
            elif self.nighttime_unit.get() == "hrs":
                off_duration *= 3600
            data['light_cycle']['off_duration'] = off_duration

            delay_durantion = int(self.init_time_lag_entry.get())
            if self.init_time_lag_unit.get() == "min":
                delay_durantion *= 60
            elif self.init_time_lag_unit.get() == "hrs":
                delay_durantion *= 3600
            data['light_cycle']['delay_before_start'] = delay_durantion

            fade_in_duration = int(self.sunrise_duration_entry.get())
            if self.sunrise_unit.get() == "min":
                fade_in_duration *= 60
            elif self.sunrise_unit.get() == "hrs":
                fade_in_duration *= 3600
            data['light_cycle']['fade_in_duration'] = fade_in_duration

            fade_out_duration = int(self.sunset_duration_entry.get())
            if self.sunset_unit.get() == "min":
                fade_out_duration *= 60
            elif self.sunset_unit.get() == "hrs":
                fade_out_duration *= 3600
            data['light_cycle']['fade_out_duration'] = fade_out_duration
            save_json(json_file, data)
            messagebox.showinfo("Success", "JSON file updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update JSON file: {e}")
        
        # Upload JSON data to ESP32 FLASH memory
        json_data = json.dumps(data)
        self.esp32.upload_config(json_data)
