// Define LED pin
#include <time.h>
const int LED_PIN = LED_BUILTIN; 
bool isSynced = false; // Flag to track if sync has already occurred
const int PWM_FREQUENCY = 5000; // Frequency in Hz
const int PWM_RESOLUTION = 8;   // 8-bit resolution: duty cycle range from 0 to 255

void setTimeFromTimestamp(time_t timestamp) {
  struct timeval tv;
  tv.tv_sec = timestamp;  // Seconds since epoch
  tv.tv_usec = 0;         // Microseconds (not used)
  settimeofday(&tv, NULL);
  Serial.println("Clock synchronized with PC time.");
}

void setup() {
  // Initialize serial communication at 115200 baud rate
  ledcAttach(LED_PIN, PWM_FREQUENCY, PWM_RESOLUTION);
  Serial.begin(115200);

  // Initialize LED_BUILTIN pin as an output
  // pinMode(LED_PIN, OUTPUT);

  // Turn off the LED initially
  // digitalWrite(LED_PIN, LOW);

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

  
      if (command == "ON") {
        // digitalWrite(LED_PIN, HIGH);  // Turn on the LED
        ledcWrite(LED_PIN, 255);  // Note: `channel` parameter is now `pin`
        Serial.println("LED OFF");
      }
      else if (command == "ON_FADE")
      {
        // Fade in: increase brightness from min to max
        Serial.println("FADING IN");
        // for (int dutyCycle = 255; dutyCycle >= 0; dutyCycle--) {
        for (int dutyCycle = 0; dutyCycle <= 255; dutyCycle++) {
          ledcWrite(LED_PIN, dutyCycle);  // Note: `channel` parameter is now `pin`
          delay(10);
        }
      }
      else if (command == "OFF") {
        // digitalWrite(LED_PIN, LOW);   // Turn on the LED
        ledcWrite(LED_PIN, 0);  // Note: `channel` parameter is now `pin`
        Serial.println("LED ON");
      }
      else if (command == "OFF_FADE")
      {
        // Fade out: decrease brightness from max to min
        Serial.println("FADING OUT");
        // for (int dutyCycle = 0; dutyCycle <= 255; dutyCycle++) {
        for (int dutyCycle = 255; dutyCycle >= 0; dutyCycle--) {
          ledcWrite(LED_PIN, dutyCycle);  // Note: `channel` parameter is now `pin`
          delay(10);
        }
      }
      else {
        Serial.println("Unknown command");
      }
    }
  }
}

