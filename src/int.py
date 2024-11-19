import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QSpinBox, QTimeEdit, QGroupBox, QFormLayout, QScrollArea
)
from PyQt5.QtCore import Qt, QTime
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from json_utils import *

class LightCycleConfigurator(QMainWindow):
    def __init__(self, esp32):
        super().__init__()
        self.setWindowTitle("Light Cycle Configurator")
        
        
        self.setGeometry(100, 100, 550, 800)

        self.esp32 = esp32

        # Enable scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        self.setCentralWidget(scroll_area)
        self.main_layout = QVBoxLayout(scroll_content)

        title_label = QLabel("Light Cycle Configurator")
        font = title_label.font()
        title_label.setFixedHeight(25)
        font.setPointSize(12) 
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Config form elements
        self.config_form()
        
        # Patterns container
        self.pattern_container = QVBoxLayout()
        self.main_layout.addLayout(self.pattern_container)

        self.update_patterns() # Add initial pattern form


        # Buttons for JSON generation and Plotting
        self.buttons()

        # Output JSON and Plot section
        # self.output_json_display = QLabel("")
        # self.output_json_display.setWordWrap(True)
        # self.main_layout.addWidget(self.output_json_display)
        self.setup_plot()

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

            # Pattern duration
            pattern_duration = QSpinBox()
            pattern_duration_unit = QComboBox()
            pattern_duration_unit.addItems(["seconds", "minutes", "hours"])
            pattern_duration_layout = QHBoxLayout()
            pattern_duration_layout.addWidget(pattern_duration)
            pattern_duration_layout.addWidget(pattern_duration_unit)
            layout.addRow("Pattern Duration", pattern_duration_layout)

            # On duration
            on_duration = QSpinBox()
            on_duration_unit = QComboBox()
            on_duration_unit.addItems(["seconds", "minutes", "hours"])
            on_duration_layout = QHBoxLayout()
            on_duration_layout.addWidget(on_duration)
            on_duration_layout.addWidget(on_duration_unit)
            layout.addRow("On Duration", on_duration_layout)

            # Off duration
            off_duration = QSpinBox()
            off_duration_unit = QComboBox()
            off_duration_unit.addItems(["seconds", "minutes", "hours"])
            off_duration_layout = QHBoxLayout()
            off_duration_layout.addWidget(off_duration)
            off_duration_layout.addWidget(off_duration_unit)
            layout.addRow("Off Duration", off_duration_layout)

            # Fade in duration
            fade_in_duration = QSpinBox()
            fade_in_duration_unit = QComboBox()
            fade_in_duration_unit.addItems(["seconds", "minutes", "hours"])
            fade_in_layout = QHBoxLayout()
            fade_in_layout.addWidget(fade_in_duration)
            fade_in_layout.addWidget(fade_in_duration_unit)
            layout.addRow("Fade In Duration", fade_in_layout)

            # Fade out duration
            fade_out_duration = QSpinBox()
            fade_out_duration_unit = QComboBox()
            fade_out_duration_unit.addItems(["seconds", "minutes", "hours"])
            fade_out_layout = QHBoxLayout()
            fade_out_layout.addWidget(fade_out_duration)
            fade_out_layout.addWidget(fade_out_duration_unit)
            layout.addRow("Fade Out Duration", fade_out_layout)

            group.setLayout(layout)
            self.pattern_container.addWidget(group)
            self.patterns.append((pattern_duration, pattern_duration_unit, on_duration, on_duration_unit, off_duration, off_duration_unit,
                                  fade_in_duration, fade_in_duration_unit, fade_out_duration, fade_out_duration_unit))

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
        # # Matplotlib Canvas for plotting
        # self.figure = Figure()
        # self.canvas = FigureCanvas(self.figure)
        # self.main_layout.addWidget(self.canvas)

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
        for (pattern_dur, pattern_unit, on_dur, on_unit, off_dur, off_unit, fade_in, fade_in_unit, fade_out, fade_out_unit) in self.patterns:
            pattern = {
                "pattern_duration": self.get_seconds(pattern_dur.value(), pattern_unit.currentText()),
                "on_duration": self.get_seconds(on_dur.value(), on_unit.currentText()),
                "off_duration": self.get_seconds(off_dur.value(), off_unit.currentText()),
                "fade_in_duration": self.get_seconds(fade_in.value(), fade_in_unit.currentText()),
                "fade_out_duration": self.get_seconds(fade_out.value(), fade_out_unit.currentText())
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

                # timeline.extend([(time, 1), (time + on_duration, 0)])
                # time += on_duration + off_duration
                while pattern_duration > 0:
                    if pattern_duration >= on_duration:
                        timeline.append((time, 1))
                        time += on_duration
                        pattern_duration -= on_duration
                    else:
                        timeline.append((time, 1))
                        time += pattern_duration
                        pattern_duration = 0

                    if pattern_duration >= off_duration:
                        timeline.append((time, 0))
                        time += off_duration
                        pattern_duration -= off_duration
                    else:
                        timeline.append((time, 0))
                        time += pattern_duration
                        pattern_duration = 0

        # Plot the state transitions
        times, states = zip(*timeline)
        ax.step(times, states, where='post')
        self.canvas.draw()

from serial_esp32 import SerialESP32
from ino_utils import compile_and_upload

if __name__ == "__main__":

    # Specify board details
    board_fqbn = "esp32:esp32:XIAO_ESP32S3"
    serial_port = 'COM5'
    baud_rate = 115200
    source_file = "configuration/configuration.ino"

    compile_and_upload(board_fqbn, serial_port, source_file)

    esp32 = SerialESP32(serial_port, baud_rate)


    app = QApplication(sys.argv)
    window = LightCycleConfigurator(esp32)
    esp32.sync_time_with_esp32()
    window.show()
    app.exec_()
    # sys.exit(app.exec_())

    esp32.close()
    
    print("Uploading cycle configuration...")
    source_file = "cycle/cycle.ino"
    compile_and_upload(board_fqbn, serial_port, source_file)
