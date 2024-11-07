import serial
import time

class SerialESP32:
    def __init__(self, serial_port = 'COM5', baud_rate=115200):
        self.ser = serial.Serial(
            port=serial_port,
            baudrate=baud_rate,
            timeout=1
        )

        if self.ser.is_open:
            print(f"Connection established on {serial_port}")
        else:
            self.ser.open()
            print(f"Opening serial connection on {serial_port}")

    def upload_config(self, json_data):
        """Uploads the JSON data to the ESP32 FLASH memory"""
        try:
            time.sleep(2)  # Wait for serial connection to initialize
            print("Sending JSON data to ESP32:")
            print(json_data)
            
            # Send JSON data over serial
            self.ser.write(json_data.encode('utf-8'))
            self.ser.write(b'\n')
            print("Data sent successfully.")

            # Optional: read response from ESP32
            response = self.ser.readline().decode('utf-8').strip()
            if response:
                print("Received response:", response)
        except serial.SerialException as e:
                print(f"Serial error: {e}")

    def close(self):
        self.ser.close()
        print("Serial connection closed.")


