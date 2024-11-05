// Define LED pin (you can use any GPIO that supports PWM, e.g., GPIO2)
const int LED_PIN = LED_BUILTIN;

// Define PWM settings
const int PWM_FREQUENCY = 5000; // Frequency in Hz
const int PWM_RESOLUTION = 8;   // 8-bit resolution: duty cycle range from 0 to 255

// Define fade parameters
const int fadeDelay = 10;       // Delay in ms for smooth fading (adjust for speed)
const int maxBrightness = 255;  // Max PWM duty cycle for full brightness (8-bit)
const int minBrightness = 0;    // Min PWM duty cycle for off

void setup() {
  // Initialize LED pin with LEDC, merging frequency, resolution, and channel into one setup
  ledcAttach(LED_PIN, PWM_FREQUENCY, PWM_RESOLUTION);

  Serial.begin(115200);
  Serial.println("Starting LED fade in and fade out...");
}

void loop() {
  // Fade in: increase brightness from min to max
  for (int dutyCycle = minBrightness; dutyCycle <= maxBrightness; dutyCycle++) {
    ledcWrite(LED_PIN, dutyCycle);  // Note: `channel` parameter is now `pin`
    Serial.println("Increasing brightness...");
    delay(fadeDelay);
  }

  // Fade out: decrease brightness from max to min
  for (int dutyCycle = maxBrightness; dutyCycle >= minBrightness; dutyCycle--) {
    ledcWrite(LED_PIN, dutyCycle);  // Note: `channel` parameter is now `pin`
    Serial.println("Decreasing brightness...");
    delay(fadeDelay);
  }
}
