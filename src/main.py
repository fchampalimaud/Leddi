from gui import GUI
from serial_esp32 import SerialESP32
from ino_utils import compile_and_upload



if __name__ == '__main__':

    # Specify board details
    board_fqbn = "esp32:esp32:XIAO_ESP32S3"
    serial_port = 'COM5'
    baud_rate = 115200
    source_file = "configuration/configuration.ino"

    compile_and_upload(board_fqbn, serial_port, source_file)

    json_file = 'light_cycle_config.json'
    
    esp32 = SerialESP32(serial_port, baud_rate)
    
    gui = GUI(esp32)
    gui.window_aspect(json_file)
    esp32.sync_time_with_esp32()
    gui.window.mainloop()
    esp32.close()

    print("Uploading cycle configuration...")
    source_file = "cycle/cycle.ino"
    compile_and_upload(board_fqbn, serial_port, source_file)