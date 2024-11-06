import serial
import json
import time

# Configuration
PORT = 'COM5'  # Adjust to your ESP32 port (e.g., '/dev/ttyUSB0' on Linux)
BAUD_RATE = 115200
JSON_FILE = 'light_cycle_config.json'

# Load JSON data from file
with open(JSON_FILE, 'r') as file:
    config_data = json.load(file)

# Convert JSON data to a string
json_data = json.dumps(config_data)

# Establish serial connection
try:
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)  # Wait for serial connection to initialize
        print("Sending JSON data to ESP32:")
        print(json_data)
        
        # Send JSON data over serial
        ser.write(json_data.encode('utf-8'))
        ser.write(b'\n')  # Send newline to signal end of data
        print("Data sent successfully.")

        # Optional: read response from ESP32
        response = ser.readline().decode('utf-8').strip()
        if response:
            print("Received response:", response)
except serial.SerialException as e:
    print(f"Serial error: {e}")
