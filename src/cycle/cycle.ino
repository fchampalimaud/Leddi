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
int offDuration[10];
int onDuration[10];
String startTime;


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



    // Loop through each pattern and load its parameters
    for (int i = 0; i < nPatterns; i++) {
        PatternDuration[i] = preferences.getInt(("pat_" + String(i) + "_dur").c_str(), 0);
        onDuration[i] = preferences.getInt(("pat_" + String(i) + "_on_dur").c_str(), 0);
        offDuration[i] = preferences.getInt(("pat_" + String(i) + "_off_dur").c_str(), 0);
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
            
            unsigned long patternStartTime = millis();
            while ((millis() - patternStartTime) < (PatternDuration[i] * 1000)) {

                ledcWrite(LED_PIN, 0);
                delay(onDuration[i] * 1000);


                ledcWrite(LED_PIN, 255);
                delay(offDuration[i] * 1000);

            }
     
        }

    }
}
