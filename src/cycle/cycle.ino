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
int nPatterns;
int PatternDuration[10];
int fadeInDuration[10];
int fadeOutDuration[10];
int offDuration[10];
int onDuration[10];
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
    Serial.println("Loading configuration...");
    Serial.println("Coucou");
    // Attach LED pin to PWM with specified frequency and resolution
    ledcAttach(LED_PIN, PWM_FREQUENCY, PWM_RESOLUTION);
    ledcWrite(LED_PIN, 255);  // Ensure LED is off by default

    // Initialize preferences with the same namespace
    preferences.begin("config", true);  // `true` means read-only mode

    // Load general parameters
    cycles = preferences.getInt("cycles", 0);
    delayBeforeStart = preferences.getInt("delay_b_start", 0);
    nPatterns = preferences.getInt("n_patterns", 0);
    startTime = preferences.getString("start_time", "00:00:00");
    Serial.printf("Loaded %d cycles, %d delay before start, %d patterns, and start time %s\n", 
                  cycles, delayBeforeStart, nPatterns, startTime.c_str());

    // // Initialize arrays to store pattern parameters
    // PatternDuration[nPatterns];
    // fadeInDuration[nPatterns];
    // fadeOutDuration[nPatterns];
    // offDuration[nPatterns];
    // onDuration[nPatterns];


    // // Loop through each pattern and load its parameters
    for (int i = 0; i < nPatterns; i++) {
        // Construct keys dynamically based on index
        PatternDuration[i] = preferences.getInt(("pat_" + String(i) + "_dur").c_str(), 0);
        onDuration[i] = preferences.getInt(("pat_" + String(i) + "_on_dur").c_str(), 0);
        offDuration[i] = preferences.getInt(("pat_" + String(i) + "_off_dur").c_str(), 0);
        fadeInDuration[i] = preferences.getInt(("pat_" + String(i) + "_fadein").c_str(), 0);
        fadeOutDuration[i] = preferences.getInt(("pat_" + String(i) + "_fadeout").c_str(), 0);

        // (Optional) You can store these values in an array or struct for later use
        Serial.printf("Pattern %d: Duration=%d, On=%d, Off=%d, FadeIn=%d, FadeOut=%d\n", 
                      i, PatternDuration[i], onDuration[i], offDuration[i], fadeInDuration[i], fadeOutDuration[i]);
    }

    // Print loaded values for debugging
    Serial.printf("Cycles: %d, Delay Before Start: %d, Patterns: %d, Start Time: %s\n", 
                  cycles, delayBeforeStart, nPatterns, startTime.c_str());

    // End preferences to free up space
    preferences.end();
    Serial.printf("cycles %d\n",cycles); // this not  aglobal variable
}

void loop() {

    // Get the current time
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        return;
    }



    // Parse the start time
    int startHour, startMinute, startSecond;
    sscanf(startTime.c_str(), "%d:%d:%d", &startHour, &startMinute, &startSecond);

    if (timeinfo.tm_hour < startHour || 
        (timeinfo.tm_hour == startHour && timeinfo.tm_min < startMinute) || 
        (timeinfo.tm_hour == startHour && timeinfo.tm_min == startMinute && timeinfo.tm_sec < startSecond)) {
        return;  // Exit the loop if the current time is before the start time
    }

    delay(delayBeforeStart * 1000);

    // Execute light cycles
    for (int cycle = 0; cycle < cycles; cycle++) {


        // Loop through each pattern
        for(int i = 0; i < nPatterns; i++) {
            // Serial.printf("Pattern %d: Duration=%d, On=%d, Off=%d, FadeIn=%d, FadeOut=%d\n", 
            //               i, PatternDuration[i], onDuration[i], offDuration[i], fadeInDuration[i], fadeOutDuration[i]);
            
            unsigned long patternStartTime = millis();
            while ((millis() - patternStartTime) < (PatternDuration[i] * 1000)) {
                // Fade-in or turn ON LED
                if (fadeInDuration[i] > 0) {
                    fadeLED(255, 0, fadeInDuration[i]);
                } else {
                    ledcWrite(LED_PIN, 0);
                }
                delay(onDuration[i] * 1000);

                // Fade-out or turn OFF LED
                if (fadeOutDuration[i] > 0) {
                    fadeLED(0, 255, fadeOutDuration[i]);
                } else {
                    ledcWrite(LED_PIN, 255);
                }
                delay(offDuration[i] * 1000);
                // PatternDuration[i]--;
            }

            // // Fade-in or turn ON LED
            // if (fadeInDuration[i] > 0) {
            //     fadeLED(255, 0, fadeInDuration[i]);
            // } else {
            //     ledcWrite(LED_PIN, 0);
            // }
            // delay(onDuration[i] * 1000);

            // // Fade-out or turn OFF LED
            // if (fadeOutDuration[i] > 0) {
            //     fadeLED(0, 255, fadeOutDuration[i]);
            // } else {
            //     ledcWrite(LED_PIN, 255);
            // }
            // delay(offDuration[i] * 1000);
            
        }


        // // Fade-in or turn ON LED
        // if (fadeInDuration > 0) {
        //     fadeLED(255, 0, fadeInDuration);
        // } else {
        //     ledcWrite(LED_PIN, 0);
        // }
        // delay(onDuration * 1000);

        // // Fade-out or turn OFF LED
        // if (fadeOutDuration > 0) {
        //     fadeLED(0, 255, fadeOutDuration);
        // } else {
        //     ledcWrite(LED_PIN, 255);
        // }
        // delay(offDuration * 1000);   
    }
}
