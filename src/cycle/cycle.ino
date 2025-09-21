#include <Arduino.h>
#include <Preferences.h>
#include <time.h>
#include <sys/time.h>
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
String startDate;


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
    startDate = preferences.getString("start_date", "1970-01-01");
    Serial.printf("Loaded %d cycles, %d delay before start, %d patterns, start time %s, start date %s\n", 
                  cycles, delayBeforeStart, nPatterns, startTime.c_str(), startDate.c_str());

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
        Serial.println("Failed to obtain time");
        return;
    }

    // Parse the start time
    int startHour, startMinute, startSecond;
    sscanf(startTime.c_str(), "%d:%d:%d", &startHour, &startMinute, &startSecond);

    // Parse the start date
    int startYear, startMonth, startDay;
    sscanf(startDate.c_str(), "%d-%d-%d", &startYear, &startMonth, &startDay);

    // Check if we need to wait for the start date
    bool isStartDateReached = (timeinfo.tm_year + 1900) > startYear ||
        ((timeinfo.tm_year + 1900) == startYear && 
         ((timeinfo.tm_mon + 1) > startMonth || 
          ((timeinfo.tm_mon + 1) == startMonth && timeinfo.tm_mday >= startDay)));

    if (!isStartDateReached) {
        // Sleep until tomorrow and check again
        int sleepDuration = 24 * 3600; // Sleep for 24 hours
        Serial.printf("Current date %04d-%02d-%02d is before start date %04d-%02d-%02d. Sleeping for 24 hours...\n",
                     timeinfo.tm_year + 1900, timeinfo.tm_mon + 1, timeinfo.tm_mday,
                     startYear, startMonth, startDay);
        esp_sleep_enable_timer_wakeup(sleepDuration * uS_TO_S_FACTOR);
        esp_light_sleep_start();
        return;
    }

    // If we reached the correct date, check the time
    int currentTimeInSeconds = (timeinfo.tm_hour * 3600) + (timeinfo.tm_min * 60) + timeinfo.tm_sec;
    int targetTimeInSeconds = (startHour * 3600) + (startMinute * 60) + startSecond;

    // Only proceed with time-based sleep if we're on the exact start date
    if (timeinfo.tm_year + 1900 == startYear && 
        timeinfo.tm_mon + 1 == startMonth && 
        timeinfo.tm_mday == startDay) {
        
        if (currentTimeInSeconds < targetTimeInSeconds) {
            int sleepDuration = (targetTimeInSeconds - currentTimeInSeconds);
            Serial.printf("Waiting for start time. Sleeping for %d seconds...\n", sleepDuration);
            esp_sleep_enable_timer_wakeup(sleepDuration * uS_TO_S_FACTOR);
            esp_light_sleep_start();
            return;
        }
    }

    // If we've reached here, we're at or past both the start date and time
    if ((timeinfo.tm_year + 1900 == startYear && 
         timeinfo.tm_mon + 1 == startMonth && 
         timeinfo.tm_mday == startDay && 
         currentTimeInSeconds >= targetTimeInSeconds) ||
        isStartDateReached) {




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
