#include <Preferences.h>
#include <time.h>
#include <esp_psram.h>
#include <esp_sleep.h>
#define uS_TO_S_FACTOR 1000000  // Microseconds to seconds conversion

const int LED_PIN = 1; // GPIO 1
bool isSynced = false;  // Flag to track if sync has already occurred


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
    pinMode(LED_PIN, OUTPUT);

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


    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    Serial.println("Current time: " + String(ctime(&tv_now.tv_sec)));

    // Get the current time
    struct tm timeinfo;
    Serial.println("Current time: " + String(ctime(&tv_now.tv_sec)));
    if (!getLocalTime(&timeinfo)) {
        Serial.println("Failed to obtain time");
        return;
    }

    // Parse the start time
    int startHour, startMinute, startSecond;
    sscanf(startTime.c_str(), "%d:%d:%d", &startHour, &startMinute, &startSecond);


    // Calculate seconds until the target time
    int currentTimeInSeconds = (timeinfo.tm_hour * 3600) + (timeinfo.tm_min * 60) + timeinfo.tm_sec;
    int targetTimeInSeconds = (startHour * 3600) + (startMinute * 60) + startSecond;

    if (currentTimeInSeconds < targetTimeInSeconds) {
        int sleepDuration = (targetTimeInSeconds - currentTimeInSeconds);
        Serial.printf("Sleeping for %d seconds...\n", sleepDuration);

        // Enable Timer Wakeup
        esp_sleep_enable_timer_wakeup(sleepDuration * uS_TO_S_FACTOR);
        Serial.println("Current time: " + String(ctime(&tv_now.tv_sec)));

        Serial.println("Entering Light Sleep Mode...");
        esp_light_sleep_start();  // Enter Light Sleep

        Serial.println("Woke up!");
    } else {




        delay(delayBeforeStart * 1000);

        // Execute light cycles
        for (int cycle = 0; cycle < cycles; cycle++) {

            Serial.printf("cycle %d\n", cycle); // this not a global variable
            // Loop through each pattern
            for (int i = 0; i < nPatterns; i++) {

                unsigned long patternStartTime = millis();
                while ((millis() - patternStartTime) < (PatternDuration[i] * 1000)) {

                    digitalWrite(LED_PIN, HIGH);
                    delay(onDuration[i] * 1000);

                    digitalWrite(LED_PIN, LOW);
                    delay(offDuration[i] * 1000);

                }

            }

        }

        esp_deep_sleep_start();

    }
}
