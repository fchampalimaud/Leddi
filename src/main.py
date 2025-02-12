
from serial_esp32 import SerialESP32
from ino_utils import compile_and_upload
from PySide6.QtWidgets import QApplication
import sys
from interface_pysite import LightCycleConfigurator



if __name__ == "__main__":

    # Specify board details
    board_fqbn = "esp32:esp32:XIAO_ESP32S3"
    baud_rate = 115200

    esp32 = SerialESP32()

    app = QApplication(sys.argv)
    window = LightCycleConfigurator(esp32)

    window.show()
    app.exec()

    if esp32.ser is not None:
        esp32.close()
        print("Uploading cycle configuration...")
        source_file = "src/cycle/cycle.ino"
        compile_and_upload(board_fqbn, window.serial_port, source_file)