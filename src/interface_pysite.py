import sys
import json
import serial.tools.list_ports
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
    QLabel, QLineEdit, QComboBox, QPushButton, QSpinBox, QTimeEdit, QGroupBox, QFormLayout, QScrollArea, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QPixmap
import PySide6.QtSvg
from PySide6.QtSvgWidgets import QSvgWidget

import numpy as np
from json_utils import *
import time
import random
import datetime
from serial_esp32 import SerialESP32
from ino_utils import compile_and_upload
import threading
from PySide6.QtWidgets import QFileDialog
import pyqtgraph as pg
from pyqtgraph import PlotWidget

class RefreshableComboBox(QComboBox):
    def __init__(self, refresh_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_callback = refresh_callback

    def showPopup(self):
        self.refresh_callback()
        super().showPopup()

class Bar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(10, 20)
        self.setStyleSheet("background-color: lightgray; border: 0.5px solid gray;")

    def fill(self, filled: bool, is_critical: bool = False):
        if filled:
            color = "red" if is_critical else "green"
        else:
            color = "lightgray"
        self.setStyleSheet(f"background-color: {color}; border: 0.5px solid gray;")

class LightCycleConfigurator(QMainWindow):
    def __init__(self, esp32):
        # Specify board details
        self.board_fqbn = "esp32:esp32:XIAO_ESP32S3"
        self.baud_rate = 115200
        self.source_file = "src/configuration/configuration.ino"

        super().__init__()
        self.setWindowTitle("Light Cycle Configurator")
        
        self.setGeometry(100, 100, 550, 800)

        self.esp32 = esp32

        # Enable scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        self.setCentralWidget(scroll_area)
        self.main_layout = QVBoxLayout(scroll_content) # vertically lining up the widgets

        # Logo widget
        logo = QSvgWidget('./src/Assets/cf_hardware_software_logo.svg')
        logo_layout = QHBoxLayout()
        logo.setFixedSize(100, 40)
        logo.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        self.main_layout.addWidget(logo, alignment=Qt.AlignRight | Qt.AlignTop)

        # Title label
        title_label = QLabel("Light Cycle Configurator")
        font = title_label.font()
        title_label.setFixedHeight(25)
        font.setPointSize(12)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.main_layout.addWidget(title_label)
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)
        
        # Help button
        help_button = QPushButton("Help")
        help_button.clicked.connect(self.show_help)
        title_layout.addWidget(help_button, alignment=Qt.AlignRight)
        self.main_layout.addLayout(title_layout)

        # Load preexisting configuration button
        load_config_button = QPushButton("  Load Pre-set Configuration  ")
        button_layout = QHBoxLayout()
        button_layout.addWidget(load_config_button, alignment=Qt.AlignRight)
        self.main_layout.addLayout(button_layout)
        load_config_button.clicked.connect(self.load_config)

        self.window_loading()

        # Config form elements
        self.config_form()
        
        # Patterns container
        self.patterns = []
        self.pattern_container = QVBoxLayout()
        self.main_layout.addLayout(self.pattern_container)

        self.update_patterns() # Add initial pattern form

        # Buttons for JSON generation and Plotting
        self.buttons()

        # Output JSON and Plot section
        self.setup_plot()
    
    def show_help(self):
        self.help_window = QWidget()
        self.help_window.setWindowTitle("Help")
        self.help_window.setGeometry(200, 200, 400, 300)

        help_layout = QVBoxLayout(self.help_window)
        help_text = QLabel(
            " <b> Instructions on how to use the application:</b><br><br>"
            "<b>1. Establish Connection</b><br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- When the application window opens, select the correct COM port for your device.<br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- Click 'Connect' and wait for the status to change from 'Not Connected' to 'Connected' (this may take up to 30 seconds).<br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- During this time, the interface may be unresponsive.<br><br>"
            "<b>2. Configure Settings</b><br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- Adjust the main settings and lighting patterns as needed.<br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- (Optional) Load a pre-saved configuration from a JSON file.<br><br>"
            "<b>3. Preview (Optional)</b><br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- Click 'Generate Plot' to visualize the lighting pattern before applying it.<br><br>"
            "<b>4. Apply Configuration</b><br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- Press 'Configure' to upload the settings to the device.<br><br>"
            "<b>5. Safely Disconnect</b><br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- Close the application window.<br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- Wait 30 seconds before unplugging the device to ensure proper shutdown.<br><br>"
            "<i>This application was developed by the Hardware and Software Platform at the Champalimaud Foundation.</i>"
        )
        help_text.setWordWrap(True)
        help_layout.addWidget(help_text)

        self.help_window.setLayout(help_layout)
        self.help_window.show()
    def load_config(self):

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Configuration File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as json_file:
                    config = json.load(json_file)
                    self.n_cycles.setValue(config.get("light_cycle", {}).get("n_cycles", 1))
                    self.delay_before_start.setValue(config.get("light_cycle", {}).get("delay_before_start", 0))
                    start_time_str = config.get("light_cycle", {}).get("start_time", "00:00:00")
                    self.start_time.setTime(QTime.fromString(start_time_str, "HH:mm:ss"))
                    self.n_patterns.setValue(config.get("light_cycle", {}).get("n_patterns", 1))
                    self.update_patterns()
                    for i, pattern in enumerate(config.get("light_cycle", {}).get("patterns", [])):
                        pattern_dur, pattern_unit, on_dur, on_unit, off_dur, off_unit = self.patterns[i]
                        pattern_dur.setValue(pattern.get("pattern_duration", 60))
                        on_dur.setValue(pattern.get("on_duration", 30))
                        off_dur.setValue(pattern.get("off_duration", 30))
            except Exception as e:
                print(f"Failed to load configuration: {e}")

    def get_available_com_ports(self):
            ports = serial.tools.list_ports.comports()
            return [port.device for port in ports]
    
    def _update_progress_bars(self, value: int):
        # Special case: if only one bar is filled, make it red
        is_critical = (value == 1)
        
        for i, bar in enumerate(self.bars):
            if i < value:
                bar.fill(True, is_critical=(is_critical and i == 0))
            else:
                bar.fill(False)

    def window_loading(self):
        
        # Create a dropdown menu for COM port selection
        self.com_port_dropdown = RefreshableComboBox(self.refresh_com_ports)
        
        port_label = QLabel("Port:")
        self.com_port_dropdown.currentIndexChanged.connect(self.update_com_port)
        com_port_layout = QHBoxLayout()
        self.com_port_dropdown.addItems(self.get_available_com_ports())

        com_port_layout.addWidget(port_label)
        com_port_layout.addWidget(self.com_port_dropdown)
        port_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        # add the connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.upload_sketch)
        com_port_layout.addWidget(self.connect_button)

        value = self.battery_value = 0
        self.bars = [Bar() for _ in range(5)]
        self._update_progress_bars(value)
        
        # Create the status bar layout with loading label and battery bars side by side
        status_layout = QHBoxLayout()
        status_layout.setSpacing(2)  # Use a small positive value for spacing

        # Add a label before the bars
        battery_label = QLabel("Device battery:")
        status_layout.addWidget(battery_label)

        # Add battery bars right after the label without any stretch or large spacing
        for bar in self.bars:
            status_layout.addWidget(bar)
        
        status_layout.addStretch()  # Add stretchable space to push the label to the right
        
        # Create a label to show loading status
        self.loading_label = QLabel("Not connected")
        self.loading_label.setStyleSheet("color: red;")
        status_layout.addWidget(self.loading_label)

        # Set alignment for the entire layout
        status_layout.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        
        self.main_layout.addLayout(com_port_layout)
        self.main_layout.addLayout(status_layout)
    
    def upload_sketch(self):
        # Upload the sketch to the ESP32
        try:
            # self.loading_timer = self.startTimer(500)
            if compile_and_upload(self.board_fqbn, self.serial_port, self.source_file):
                # self.killTimer(self.loading_timer)
                self.esp32.set_port(self.serial_port)
                self.battery_value = self.esp32.read_battery_value()
                if self.battery_value is not None:
                    self._update_progress_bars(self.battery_value)
                else:
                    self._update_progress_bars(0)
                self.esp32.sync_time_with_esp32()
                self.loading_label.setStyleSheet("color: green;")
                self.loading_label.setText("Connected")
            else:
                self.loading_label.setStyleSheet("color: red;")
                self.loading_label.setText("Connection failed")
        except Exception as e:
            print(f"An error occurred during compilation or upload: {e}")
            self.loading_label.setStyleSheet("color: red;")
            self.loading_label.setText("Connection failed")

    def refresh_com_ports(self):
        # Refresh the list of available COM ports
        self.com_port_dropdown.clear()
        self.com_port_dropdown.addItems(self.get_available_com_ports())

    def timerEvent(self, event):
        # Update the loading label with iterative dots
        current_text = self.loading_label.text()
        if current_text.endswith("..."):
            self.loading_label.setText("Connecting")
        else:
            self.loading_label.setText(current_text + ".")

    def update_com_port(self):
        # Update the COM port based on dropdown selection
        selected_port = self.com_port_dropdown.currentText()
        self.serial_port = selected_port

    def config_form(self):
        # Main configuration form
        self.main_settings_group = QGroupBox("Main Settings")
        form_layout = QFormLayout()

        # Load existing config if available
        try:
            with open('./config.json', 'r') as json_file:
                config = json.load(json_file)
                n_cycles = config.get("light_cycle", {}).get("n_cycles", 1)
                delay_before_start = config.get("light_cycle", {}).get("delay_before_start", 0)
                start_time_str = config.get("light_cycle", {}).get("start_time", "00:00:00")
                n_patterns = config.get("light_cycle", {}).get("n_patterns", 1)
                for pattern in config.get("light_cycle", {}).get("patterns", []):
                    pass    
        except FileNotFoundError:
            n_cycles = 1
            delay_before_start = 0
            start_time_str = "00:00:00"
            n_patterns = 1

        # Number of cycles
        self.n_cycles = QSpinBox()
        self.n_cycles.setValue(n_cycles)
        self.n_cycles.setRange(1, 100)
        form_layout.addRow("Number of Cycles", self.n_cycles)

        # Delay before start
        self.delay_before_start = QSpinBox()
        self.delay_before_start.setValue(delay_before_start)
        self.delay_before_start.setRange(0, 1000)
        self.delay_unit = QComboBox()
        self.delay_unit.addItems(["seconds", "minutes", "hours"])
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(self.delay_before_start)
        delay_layout.addWidget(self.delay_unit)
        form_layout.addRow("Delay Before Start", delay_layout)

        # Start time
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime.fromString(start_time_str, "HH:mm:ss"))
        self.start_time.setDisplayFormat("HH:mm:ss")
        form_layout.addRow("Start Time", self.start_time)

        # Number of patterns
        self.n_patterns = QSpinBox()
        self.n_patterns.setValue(n_patterns)
        self.n_patterns.setRange(1, 5)
        # update pattern beggining
        self.n_patterns.valueChanged.connect(self.update_patterns)
        form_layout.addRow("Number of Patterns", self.n_patterns)

        self.main_settings_group.setLayout(form_layout)
        self.main_layout.addWidget(self.main_settings_group)

    def update_patterns(self):
        # Clear existing pattern widgets 
        for i in reversed(range(self.pattern_container.count())):
            widget = self.pattern_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add pattern forms based on number of patterns
        n_patterns = self.n_patterns.value()
        self.patterns = []
        for i in range(n_patterns):
            group = QGroupBox(f"Pattern {i + 1}")
            layout = QFormLayout()

            # if pattern exists, load the values
            try:
                with open('./config.json', 'r') as json_file:
                    config = json.load(json_file)
                    if i < len(config.get("light_cycle", {}).get("patterns", [])):
                        pattern = config.get("light_cycle", {}).get("patterns", [])[i]
                        pattern_duration_value = pattern.get("pattern_duration", 60)
                        on_duration_value = pattern.get("on_duration", 30)
                        off_duration_value = pattern.get("off_duration", 30)
                    else:
                        pattern_duration_value = 0
                        on_duration_value = 0
                        off_duration_value = 0
            except FileNotFoundError:
                pattern_duration_value = 0
                on_duration_value = 0
                off_duration_value = 0

            # Pattern duration
            pattern_duration = QSpinBox()
            pattern_duration.setRange(0, 9999)
            pattern_duration.setValue(pattern_duration_value)
            pattern_duration_unit = QComboBox()
            pattern_duration_unit.addItems(["seconds", "minutes", "hours"])
            pattern_duration_layout = QHBoxLayout()
            pattern_duration_layout.addWidget(pattern_duration)
            pattern_duration_layout.addWidget(pattern_duration_unit)
            layout.addRow("Pattern Duration", pattern_duration_layout)

            # On duration
            on_duration = QSpinBox()
            on_duration.setRange(0, 9999)
            on_duration.setValue(on_duration_value)
            on_duration_unit = QComboBox()
            on_duration_unit.addItems(["seconds", "minutes", "hours"])
            on_duration_layout = QHBoxLayout()
            on_duration_layout.addWidget(on_duration)
            on_duration_layout.addWidget(on_duration_unit)
            layout.addRow("On Period", on_duration_layout)

            # Off duration
            off_duration = QSpinBox()
            off_duration.setRange(0, 9999)
            off_duration.setValue(off_duration_value)
            off_duration_unit = QComboBox()
            off_duration_unit.addItems(["seconds", "minutes", "hours"])
            off_duration_layout = QHBoxLayout()
            off_duration_layout.addWidget(off_duration)
            off_duration_layout.addWidget(off_duration_unit)
            layout.addRow("Off Period", off_duration_layout)

            group.setLayout(layout)
            self.pattern_container.addWidget(group)
            self.patterns.append((pattern_duration, pattern_duration_unit, on_duration, on_duration_unit, off_duration, off_duration_unit))

    def buttons(self):
        button_layout = QHBoxLayout()
        generate_json_btn = QPushButton("Configure")
        generate_json_btn.clicked.connect(self.generate_json)
        button_layout.addWidget(generate_json_btn)

        generate_plot_btn = QPushButton("Generate Plot")
        generate_plot_btn.clicked.connect(self.generate_plot)
        button_layout.addWidget(generate_plot_btn)
        self.main_layout.addLayout(button_layout)

    def setup_plot(self):
        # PyQtGraph PlotWidget for plotting
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.hideAxis('left')
        self.plot_widget.hideAxis('bottom')
        self.main_layout.addWidget(self.plot_widget)

    def generate_json(self):
        # Get the current local date
        current_date = datetime.datetime.now().date()
        
        # Get the time from the QTimeEdit widget
        local_time = self.start_time.time()
        
        # Convert QTime to Python datetime with today's date
        local_datetime = datetime.datetime(
            current_date.year, 
            current_date.month, 
            current_date.day,
            local_time.hour(),
            local_time.minute(),
            local_time.second()
        )
        
        # Convert to UTC
        utc_datetime = local_datetime.astimezone(datetime.timezone.utc)
        
        # Format as string in HH:MM:SS format
        utc_time_str = utc_datetime.strftime("%H:%M:%S")
        
        # Generate JSON configuration
        config = {
            "light_cycle": {
                "n_cycles": self.n_cycles.value(),
                "delay_before_start": self.get_seconds(self.delay_before_start.value(), self.delay_unit.currentText()),
                "start_time": utc_time_str,  # Use the UTC time string
                "n_patterns": self.n_patterns.value(),
                "patterns": []
            }
        }
        for (pattern_dur, pattern_unit, on_dur, on_unit, off_dur, off_unit) in self.patterns:
            pattern = {
                "pattern_duration": self.get_seconds(pattern_dur.value(), pattern_unit.currentText()),
                "on_duration": self.get_seconds(on_dur.value(), on_unit.currentText()),
                "off_duration": self.get_seconds(off_dur.value(), off_unit.currentText())
            }
            config["light_cycle"]["patterns"].append(pattern)

        # Save JSON to file
        with open('./config.json', 'w') as json_file:
            json.dump(config, json_file, indent=4)
        data = json.dumps(config)
        print('Here data:' + data)
        self.esp32.upload_config(data)

    def get_seconds(self, value, unit):
        # Convert value to seconds based on unit
        if unit == "minutes":
            return value * 60
        elif unit == "hours":
            return value * 3600
        return value

    def generate_plot(self):
        # Generate plot of light cycle states
        
        self.plot_widget.clear()
        
        self.plot_widget.setTitle("Light Cycle Plot")
        self.plot_widget.setLabel('left', 'State (On/Off)')
        self.plot_widget.setLabel('bottom', 'Time (seconds)')

        timeline = []
        time = self.get_seconds(self.delay_before_start.value(), self.delay_unit.currentText())

        for _ in range(self.n_cycles.value()):
            for pattern_dur, pattern_unit, on_dur, on_unit, off_dur, off_unit in self.patterns:
                pattern_duration = self.get_seconds(pattern_dur.value(), pattern_unit.currentText())
                on_duration = self.get_seconds(on_dur.value(), on_unit.currentText())
                off_duration = self.get_seconds(off_dur.value(), off_unit.currentText())

                pattern_start_time = time
                while time - pattern_start_time < pattern_duration:
                    if time - pattern_start_time + on_duration <= pattern_duration:
                        time += on_duration
                        timeline.append((time - on_duration, 1))  # Start of 'on' state
                        timeline.append((time, 1))                # End of 'on' state
                    else:
                        remaining_on_time = pattern_duration - (time - pattern_start_time)
                        time += remaining_on_time
                        timeline.append((time - remaining_on_time, 1))  # Start of 'on' state
                        timeline.append((time, 1))                      # End of 'on' state

                    if time - pattern_start_time + off_duration <= pattern_duration:
                        time += off_duration
                        timeline.append((time - off_duration, 0))  # Start of 'off' state
                        timeline.append((time, 0))                 # End of 'off' state
                    else:
                        remaining_off_time = pattern_duration - (time - pattern_start_time)
                        time += remaining_off_time
                        timeline.append((time - remaining_off_time, 0))  # Start of 'off' state
                        timeline.append((time, 0))                       # End of 'off' state

        # Ensure the times list has one more element than the states list
        if timeline:
            times, states = zip(*timeline)
            times = list(times)
            states = list(states)
            times.append(times[-1] + 1)  # Add an additional time point

            # Plot the state transitions
            self.plot_widget.plot(times, states, stepMode=True, fillLevel=0, brush=(24, 168, 246))
            self.plot_widget.hideAxis('left')
