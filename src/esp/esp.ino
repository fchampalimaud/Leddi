// Define LED pin
#include <time.h>
const int LED_PIN = LED_BUILTIN; // On some boards, this is already defined as 13 or 2
bool isSynced = false; // Flag to track if sync has already occurred

void setTimeFromTimestamp(time_t timestamp) {
  struct timeval tv;
  tv.tv_sec = timestamp;  // Seconds since epoch
  tv.tv_usec = 0;         // Microseconds (not used)
  settimeofday(&tv, NULL);
  Serial.println("Clock synchronized with PC time.");
}

void setup() {
  // Initialize serial communication at 115200 baud rate
  Serial.begin(115200);

  // Initialize LED_BUILTIN pin as an output
  pinMode(LED_PIN, OUTPUT);

  // Turn off the LED initially
  digitalWrite(LED_PIN, LOW);

  // Wait for serial connection to be established (optional)
  while (!Serial) {
    ; // Wait for Serial to connect
  }

  Serial.println("ESP32 ready for initial clock sync...");
  // Sync the clock with the PC time


  Serial.println("ESP32 ready for commands...");
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming data as a string
    String command = Serial.readStringUntil('\n');

    if (!isSynced) {

      time_t timestamp = command.toInt();

      // If the timestamp is valid, set the ESP32's time and mark as synced
      if (timestamp > 0) {
        setTimeFromTimestamp(timestamp);
        Serial.println("Time set to: " + String(ctime(&timestamp)));
        isSynced = true; // Mark sync as complete
      } else {
        Serial.println("Invalid timestamp received.");
      }
    }

    else {

      // Process commands
      if (command == "ON") {
        digitalWrite(LED_PIN, HIGH);  // Turn on the LED
        Serial.println("LED OFF");
      }
      else if (command == "OFF") {
        digitalWrite(LED_PIN, LOW);   // Turn off the LED
        Serial.println("LED ON");
      }
      else {
        Serial.println("Unknown command");
      }
    }
  }
}

