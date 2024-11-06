#include <Preferences.h>
#include <time.h>
// Define LED pin and constants
const int LED_PIN = LED_BUILTIN; 
bool isSynced = false;  // Flag to track if sync has already occurred
const int PWM_FREQUENCY = 5000; // Frequency in Hz
const int PWM_RESOLUTION = 8;   // 8-bit resolution: duty cycle range from 0 to 255


Preferences preferences;

// Variables to store loaded configuration
int cycles;
int delayBeforeStart;
int fadeInDuration;
int fadeOutDuration;
int offDuration;
int onDuration;
String startTime;

void fadeLED(int start, int end, int duration) {
    int stepDelay = duration * 1000 / abs(end - start);
    for (int dutyCycle = start; dutyCycle != end; dutyCycle += (end > start ? 1 : -1)) {
        ledcWrite(LED_PIN, dutyCycle);
        delay(stepDelay);
    }
    ledcWrite(LED_PIN, end);  // Ensure it reaches the final state
}

void setup() {
    Serial.begin(115200);
    //while (!Serial);

    Serial.println("COUCOU #1");

    ledcAttach(LED_PIN, PWM_FREQUENCY, PWM_RESOLUTION);
    ledcWrite(LED_PIN, 255);  // Ensure LED is off by default
    
    Serial.println("Loading configuration...");

    // Initialize preferences with the same namespace
    preferences.begin("config", true);  // `true` means read-only mode

    // Load each parameter
    cycles = preferences.getInt("cycles", -1);  // -1 is the default if not found
    delayBeforeStart = preferences.getInt("delay_before_start", 1);
    fadeInDuration = preferences.getInt("fade_in_duration", -1);
    fadeOutDuration = preferences.getInt("fade_out_duration", -1);
    offDuration = preferences.getInt("off_duration", -1);
    onDuration = preferences.getInt("on_duration", -1);
    startTime = preferences.getString("start_time", "00:00:00");

    // End preferences to free up space
    preferences.end();

    // Print loaded values to confirm
    Serial.println("Loaded Configuration:");
    Serial.printf("Cycles: %d\n", cycles);
    Serial.printf("Delay Before Start: %d\n", delayBeforeStart);
    Serial.printf("Fade In Duration: %d\n", fadeInDuration);
    Serial.printf("Fade Out Duration: %d\n", fadeOutDuration);
    Serial.printf("Off Duration: %d\n", offDuration);
    Serial.printf("On Duration: %d\n", onDuration);
    Serial.printf("Start Time: %s\n", startTime.c_str());
}

void loop() {
  // Use loaded configuration in your application

    Serial.println("COUCOU #2");

    Serial.printf("Cycles: %d\n", cycles);


    delay(delayBeforeStart * 1000);

    // Execute light cycles
    for (int cycle = 0; cycle < cycles; cycle++) {
        Serial.println("COUCOU #3");

        // Fade-in or turn ON LED
        if (fadeInDuration > 0) {
            fadeLED(255, 0, fadeInDuration);
        } else {
            ledcWrite(LED_PIN, 0);
        }
        delay(onDuration * 1000);

        // Fade-out or turn OFF LED
        if (fadeOutDuration > 0) {
            fadeLED(0, 255, fadeOutDuration);
        } else {
            ledcWrite(LED_PIN, 255);
        }
        delay(offDuration * 1000);   
    }
}
