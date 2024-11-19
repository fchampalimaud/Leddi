#include <Preferences.h>
#include <ArduinoJson.h>
#include <Arduino.h>
#include <esp_psram.h>

bool isSynced = false; 
Preferences preferences;

void setTimeFromTimestamp(time_t timestamp) {
  struct timeval tv;
  tv.tv_sec = timestamp;  // Seconds since epoch
  tv.tv_usec = 0;         // Microseconds (not used)
  settimeofday(&tv, NULL);
  Serial.println("Clock synchronized with PC time.");
}

void setup() {
  Serial.begin(115200);
  while (!Serial);  // Wait for serial connection
  Serial.println("Waiting for JSON data...");

  // Initialize preferences with a namespace
  preferences.begin("config", false);
}

void loop() {
  if (Serial.available()) {

    // Read the JSON string from serial
    String jsonString = Serial.readStringUntil('\n');
    

    while (!isSynced) {

      time_t timestamp = jsonString.toInt();

      // If the timestamp is valid, set the ESP32's time and mark as synced
      if (timestamp > 0) {
        setTimeFromTimestamp(timestamp);
        Serial.println("Time set to: " + String(ctime(&timestamp)));
        isSynced = true; // Mark sync as complete
      } else {
        Serial.println(timestamp + "Invalid timestamp received.");
      }
    }

    

    if (jsonString) {
        Serial.println("Received JSON: " + jsonString);

        // Parse JSON
        StaticJsonDocument<256> doc;
        DeserializationError error = deserializeJson(doc, jsonString);
        if (error) {
          Serial.print("JSON parse error: ");
          Serial.println(error.c_str());
          return;
        }

        // Access "light_cycle" object
        JsonObject lightCycle = doc["light_cycle"];

        // Store parameters from "light_cycle" in flash memory
        preferences.putInt("cycles", lightCycle["n_cycles"] | 0);
        preferences.putInt("delay_b_start", lightCycle["delay_before_start"] | 0);
        // Store number of patterns
        int nPatterns = lightCycle["n_patterns"] | 0;
        preferences.putInt("n_patterns", nPatterns);

        // Loop through each pattern and store its parameters
        for (int i = 0; i < nPatterns; i++) {
            // Access each pattern in the array
            JsonObject pattern = lightCycle["patterns"][i];
            
            // Create unique keys for each pattern's parameter based on the index
            preferences.putInt(("pat_" + String(i) + "_dur").c_str(), pattern["pattern_duration"] | 0);
            preferences.putInt(("pat_" + String(i) + "_on_dur").c_str(), pattern["on_duration"] | 0);
            preferences.putInt(("pat_" + String(i) + "_off_dur").c_str(), pattern["off_duration"] | 0);
            preferences.putInt(("pat_" + String(i) + "_fadein").c_str(), pattern["fade_in_duration"] | 0);
            preferences.putInt(("pat_" + String(i) + "_fadeout").c_str(), pattern["fade_out_duration"] | 0);
        }

        // Parse start_time as a string (e.g., "09:04:01")
        const char* startTime = lightCycle["start_time"];
        preferences.putString("start_time", startTime);


    }
    


  }
}
