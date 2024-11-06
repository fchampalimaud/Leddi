#include <time.h>

// Define LED pin and constants
const int LED_PIN = LED_BUILTIN; 
bool isSynced = false;  // Flag to track if sync has already occurred
const int PWM_FREQUENCY = 5000; // Frequency in Hz
const int PWM_RESOLUTION = 8;   // 8-bit resolution: duty cycle range from 0 to 255

// Configuration for light cycle
const int START_HOUR = 11;         // Start time (hours, 24-hour format)
const int START_MINUTE = 3;        // Start time (minutes)
const int CYCLES = 5;              // Number of light cycles
const int DELAY_BEFORE_START = 2;  // Delay before starting cycle in seconds
const int ON_DURATION = 5;         // ON duration in seconds
const int OFF_DURATION = 2;        // OFF duration in seconds
const int FADE_IN_DURATION = 1;    // Fade-in duration in seconds
const int FADE_OUT_DURATION = 1;   // Fade-out duration in seconds

void setTimeFromTimestamp(time_t timestamp) {
    struct timeval tv;
    tv.tv_sec = timestamp;  // Seconds since epoch
    tv.tv_usec = 0;         // Microseconds (not used)
    settimeofday(&tv, NULL);
    Serial.println("Clock synchronized with PC time.");
}

void fadeLED(int start, int end, int duration) {
    int stepDelay = duration * 1000 / abs(end - start);
    for (int dutyCycle = start; dutyCycle != end; dutyCycle += (end > start ? 1 : -1)) {
        ledcWrite(LED_PIN, dutyCycle);
        delay(stepDelay);
    }
    ledcWrite(LED_PIN, end);  // Ensure it reaches the final state
}

void setup() {
    ledcAttach(LED_PIN, PWM_FREQUENCY, PWM_RESOLUTION);
    ledcWrite(LED_PIN, 255);  // Ensure LED is off by default
}

void loop() {
    struct tm timeInfo;
    getLocalTime(&timeInfo);
    // if (timeInfo.tm_hour == START_HOUR && timeInfo.tm_min >= START_MINUTE) {

    delay(DELAY_BEFORE_START * 1000);

    // Execute light cycles
    for (int cycle = 0; cycle < CYCLES; cycle++) {

        // Fade-in or turn ON LED
        if (FADE_IN_DURATION > 0) {
            fadeLED(255, 0, FADE_IN_DURATION);
        } else {
            ledcWrite(LED_PIN, 0);
        }
        delay(ON_DURATION * 1000);

        // Fade-out or turn OFF LED
        if (FADE_OUT_DURATION > 0) {
            fadeLED(0, 255, FADE_OUT_DURATION);
        } else {
            ledcWrite(LED_PIN, 255);
        }
        delay(OFF_DURATION * 1000);   
    }
}
