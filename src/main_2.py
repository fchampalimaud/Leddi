from gui import GUI
from serial_esp32 import SerialESP32


if __name__ == '__main__':

    json_file = 'light_cycle_config.json'
    serial_port = 'COM5'
    baud_rate = 115200
    esp32 = SerialESP32(serial_port, baud_rate)
    gui = GUI(esp32)
    gui.window_aspect(json_file)
    gui.window.mainloop()