import serial
import time
import datetime

def get_current_timestamp():
    return int(time.time())

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
    
    
    # Send timestamp to ESP32
    def sync_time_with_esp32(self):
        if self.ser.is_open:
            # Get current timestamp
            timestamp = get_current_timestamp()
            print(f"Sending timestamp: {timestamp} ({datetime.datetime.fromtimestamp(timestamp)})")

            # Send timestamp to ESP32
            self.ser.write(f"{timestamp}\n".encode())

            # Wait for ESP32 to confirm sync
            time.sleep(0.5) 
            response = self.ser.readline().decode().strip()
            if response:
                print(f"ESP32 Response: {response}")
            else:
                print("No response from ESP32")
        else:
            print("Serial port is not open")


    def close(self):
        self.ser.close()
        print("Serial connection closed.")


