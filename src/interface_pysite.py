import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QSpinBox, QTimeEdit, QGroupBox, QFormLayout, QScrollArea, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QPixmap
import PySide6.QtSvg
from PySide6.QtSvgWidgets import QSvgWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from json_utils import *
import time

from serial_esp32 import SerialESP32
from ino_utils import compile_and_upload
import threading
from PySide6.QtWidgets import QFileDialog

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

        # Create the logo widget
        logo = QSvgWidget('./src/Assets/cf_hardware_software_logo.svg')
        # print(logo.size())
        # logo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # logo.setFixedSize(64, 64)  # Ensures the widget has a specific size (640, 480)

        # Create a layout to position the logo
        logo_layout = QHBoxLayout()
        # logo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        logo.setFixedSize(100, 40)
        logo.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        # logo.setFixedSize(100, 35)
        # logo_layout.addWidget(logo, alignment=Qt.AlignRight | Qt.AlignTop)
        self.main_layout.addWidget(logo, alignment=Qt.AlignRight | Qt.AlignTop)
        # Ensure no unwanted margins or spacing
        # logo_layout.setContentsMargins(1, 1, 1, 1)
        # logo_layout.setSpacing(0)
        # self.main_layout.addLayout(logo_layout)

        # logo
        # .setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



        # logo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # logo.setFixedSize(100, 35)  # Ensures the widget has a specific size

        # Create a spacer and a layout to position the logo
        # self.main_layout.addWidget(logo, alignment=Qt.AlignRight | Qt.AlignTop)  # Align logo to top-right corner

        title_label = QLabel("Light Cycle Configurator")
        font = title_label.font()
        title_label.setFixedHeight(25)
        font.setPointSize(12)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # Create a help button
        help_button = QPushButton("Help")
        help_button.clicked.connect(self.show_help)

        # Create a layout to position the title and help button
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(help_button, alignment=Qt.AlignRight)
        self.main_layout.addLayout(title_layout)
        

        # Create a load preexisting configuration button
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
        help_text = QLabel(" <b> Instructions on how to use the application:</b><br><br>"
                "<b>1.</b> Select the COM port and click 'Connect'.<br>"
                "<b>2.</b> Configure the main settings and patterns.<br>"
                "<b>3.</b> Click 'Configure' to generate the JSON configuration.<br>"
                "<b>4.</b> Click 'Generate Plot' to visualize the light cycle.<br>"
                "<b>5.</b> Upload the configuration to the ESP32 device.")
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



    def window_loading(self):
        
        # Create a dropdown menu for COM port selection
        self.com_port_dropdown = QComboBox()

        import serial.tools.list_ports

        def get_available_com_ports():
            ports = serial.tools.list_ports.comports()
            return [port.device for port in ports]

        
        port_label = QLabel("Port:")
        self.com_port_dropdown.currentIndexChanged.connect(self.update_com_port)
        com_port_layout = QHBoxLayout()
        self.com_port_dropdown.addItems(get_available_com_ports())

        com_port_layout.addWidget(port_label)
        com_port_layout.addWidget(self.com_port_dropdown)
        port_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        # add the connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.upload_sketch)
        com_port_layout.addWidget(self.connect_button)


  
      
        self.main_layout.addLayout(com_port_layout)

        # Create a label to show loading status
        self.loading_label = QLabel("Not connected")
        self.loading_label.setStyleSheet("color: red;")
        self.loading_label.setAlignment(Qt.AlignRight)
        self.main_layout.addWidget(self.loading_label)
        

        # Start a timer to update the loading label
        # self.loading_timer = self.startTimer(500)  # Update every 500 ms

        # Create a button to connect to the ESP32

        # self.connect_button.clicked.connect(self.esp32.connect)
        # self.main_layout.addWidget(self.connect_button)

        # # Create a label to show loading status
        # self.loading_label = QLabel("Loading...")
        # self.loading_label.setAlignment(Qt.AlignLeft)
        # self.main_layout.addWidget(self.loading_label)

        # # Start a timer to update the loading label
        # self.loading_timer = self.startTimer(500)  # Update every 500 ms
    
    def upload_sketch(self):
        # Upload the sketch to the ESP32
        try:
            # self.loading_timer = self.startTimer(500)
            if compile_and_upload(self.board_fqbn, self.serial_port, self.source_file):
                # self.killTimer(self.loading_timer)
                self.esp32.set_port(self.serial_port)
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
        # print(f"Selected COM port: {selected_port}")
        # self.esp32.set_port(selected_port)

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
        # # Clear existing pattern widgets 
        for i in reversed(range(self.pattern_container.count())):
            widget = self.pattern_container.itemAt(i).widget()
            # while len(self.patterns) > self.n_patterns.value():
            if widget:
                widget.deleteLater()
        #     if widget:
        #         # update the 
        #         while len(self.patterns) > self.n_patterns.value():
        #             self.patterns.pop()
        #         # self.n_patterns.value()
        #         widget.deleteLater()

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
            pattern_duration.setValue(pattern_duration_value)
            pattern_duration_unit = QComboBox()
            pattern_duration_unit.addItems(["seconds", "minutes", "hours"])
            pattern_duration_layout = QHBoxLayout()
            pattern_duration_layout.addWidget(pattern_duration)
            pattern_duration_layout.addWidget(pattern_duration_unit)
            layout.addRow("Pattern Duration", pattern_duration_layout)

            # On duration
            on_duration = QSpinBox()
            on_duration.setValue(on_duration_value)
            on_duration_unit = QComboBox()
            on_duration_unit.addItems(["seconds", "minutes", "hours"])
            on_duration_layout = QHBoxLayout()
            on_duration_layout.addWidget(on_duration)
            on_duration_layout.addWidget(on_duration_unit)
            layout.addRow("On Period", on_duration_layout)

            # Off duration
            off_duration = QSpinBox()
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
        # Matplotlib Canvas for plotting
        self.figure = Figure(figsize=(5, 4))  # Set the figure size
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(500, 400)  # Set the canvas size
        self.main_layout.addWidget(self.canvas)

    def generate_json(self):
        # Generate JSON configuration
        config = {
            "light_cycle": {
                "n_cycles": self.n_cycles.value(),
                "delay_before_start": self.get_seconds(self.delay_before_start.value(), self.delay_unit.currentText()),
                "start_time": self.start_time.text(),
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

        # if self.esp32.ser is not None:
        #     self.esp32.close()
        #     print("Uploading cycle configuration...")
        #     source_file = "src/cycle/cycle.ino"
        #     compile_and_upload(self.board_fqbn, self.serial_port, source_file)
        #     self.esp32.read()
        #     self.esp32.read()

    def get_seconds(self, value, unit):
        # Convert value to seconds based on unit
        if unit == "minutes":
            return value * 60
        elif unit == "hours":
            return value * 3600
        return value

    def generate_plot(self):
        # Generate plot of light cycle states
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title("Light Cycle Plot")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("State (On/Off)")
        
        timeline = []
        time = self.get_seconds(self.delay_before_start.value(), self.delay_unit.currentText())
        for _ in range(self.n_cycles.value()):
            for pattern_dur, pattern_init, on_dur, on_unit, off_dur, off_unit, *_ in self.patterns:
                pattern_duration = self.get_seconds(pattern_dur.value(), pattern_init.currentText())
                on_duration = self.get_seconds(on_dur.value(), on_unit.currentText())
                off_duration = self.get_seconds(off_dur.value(), off_unit.currentText())

                while pattern_duration > 0:
                    if pattern_duration >= on_duration:
                        if on_duration >= 0:
                            
                            print("on  " + str(on_duration))
                            time += on_duration
                            pattern_duration -= on_duration

                            timeline.append((time, 0))
                    else:
                        
                        time += pattern_duration
                        pattern_duration = 0
                        timeline.append((time, 0))

                    if pattern_duration >= off_duration:
                        if off_duration >= 0:
                            
                            print("off " + str(off_duration))
                            time += off_duration
                            pattern_duration -= off_duration
                            timeline.append((time, 1))
                    else:
                        
                        time += pattern_duration
                        pattern_duration = 0
                        timeline.append((time, 1))

        # Plot the state transitions
        times, states = zip(*timeline)
        ax.step(times, states, where='post')
        self.canvas.draw()



if __name__ == "__main__":

    # Specify board details
    board_fqbn = "esp32:esp32:XIAO_ESP32S3"
    serial_port = 'COM5'
    baud_rate = 115200

    # compile_and_upload(board_fqbn, serial_port, source_file)

    esp32 = SerialESP32()

    app = QApplication(sys.argv)
    window = LightCycleConfigurator(esp32)

    window.show()
    app.exec()

    if esp32.ser is not None:
        esp32.close()
        print("Uploading cycle configuration...")
        source_file = "src/cycle/cycle.ino"
        compile_and_upload(board_fqbn, serial_port, source_file)
