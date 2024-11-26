import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QProgressBar, QPushButton
from PySide6.QtCore import QTimer, QThread, Signal

# Simulate a long-running task
def long_running_task(duration):
    for _ in range(duration):
        time.sleep(1)  # Simulate work (1 second per iteration)

# Worker class to run the task in a separate thread
class WorkerThread(QThread):
    progress = Signal(int)  # Signal to send progress updates

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def run(self):
        for i in range(self.duration):
            time.sleep(1)  # Simulate work
            self.progress.emit((i + 1) * 100 // self.duration)  # Emit progress percentage

# Main application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup UI
        self.setWindowTitle("Progress Bar Example")
        self.setGeometry(100, 100, 400, 200)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.start_button = QPushButton("Start Task")
        self.start_button.clicked.connect(self.start_task)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_task(self):
        duration = 10  # Duration of the task in seconds

        # Disable the button to prevent multiple clicks
        self.start_button.setEnabled(False)

        # Create and start the worker thread
        self.worker = WorkerThread(duration)
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.finished.connect(self.task_finished)
        self.worker.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def task_finished(self):
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(100)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
