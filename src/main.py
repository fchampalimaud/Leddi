import serial
import time
import yaml
import datetime

# Load YAML configuration
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load light cycle configuration
config = load_config('light_cycle_config.yaml')
light_cycle = config['light_cycle']

# Initialize serial connection to COM5
ser = serial.Serial(
    port='COM5',        
    baudrate=115200,    # Same baud rate as ESP32 program
    timeout=1
)

# Check if the serial connection is open
if ser.is_open:
    print("Connection established on COM5")
else:
    ser.open()
    print("Opening serial connection on COM5")

# Function to get the current Unix timestamp
def get_current_timestamp():
    return int(time.time())

# Send timestamp to ESP32
def sync_time_with_esp32():
    if ser.is_open:
        # Get current timestamp
        timestamp = get_current_timestamp()
        print(f"Sending timestamp: {timestamp} ({datetime.datetime.fromtimestamp(timestamp)})")

        # Send timestamp to ESP32
        ser.write(f"{timestamp}\n".encode())

        # Wait for ESP32 to confirm sync
        time.sleep(0.5)  # Short delay for response
        response = ser.readline().decode().strip()
        if response:
            print(f"ESP32 Response: {response}")
        else:
            print("No response from ESP32")
    else:
        print("Serial port is not open")
        # Continuously try to sync time with ESP32 until successful
        



# Function to send command to ESP32
def control_led(command):
    if ser.is_open:
        ser.write((command + '\n').encode())  # Send command with newline
        print(f"Sent command: {command}")
        time.sleep(0.1)  # Short delay for ESP32 to process

        # Read the ESP32's response
        response = ser.readline().decode().strip()
        if response:
            print(f"ESP32 Response: {response}")
        return response
    else:
        print("Serial port is not open")

try:


    sync_time_with_esp32()
    response = ser.readline().decode().strip()
    if response:
        print(f"ESP32 Response: {response}")
    else:
        print("No response from ESP32")


    # Wait until the specified start time
    start_time_str = light_cycle['start_time']
    start_time = datetime.datetime.strptime(start_time_str, "%H:%M:%S").time()
    now = datetime.datetime.now().time()

    while now < start_time:
        print(f"Waiting for start time: {start_time_str}. Current time: {now}")
        time.sleep(1)  # Check every 30 seconds
        now = datetime.datetime.now().time()

    # Delay before starting the light cycle
    time.sleep(light_cycle['delay_before_start'])

    # Execute light cycles
    for cycle in range(light_cycle['cycles']):
        print(f"Starting cycle {cycle + 1}/{light_cycle['cycles']}")

        # Inverted behaviour: The LED will only turn off when the user LED pin on the XIAO ESP32S3 is set to a high level
        # and it will only turn on when the pin is set to a low level.

        control_led("OFF")
        time.sleep(light_cycle['on_duration'])

        # Turn OFF the LED
        control_led("ON")
        time.sleep(light_cycle['off_duration'])


except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Close the serial connection
    ser.close()
    print("Serial connection closed")
