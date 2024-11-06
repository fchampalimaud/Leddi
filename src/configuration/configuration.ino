#include <Preferences.h>
#include <ArduinoJson.h>

Preferences preferences;

void setup() {
    Serial.begin(115200);

    // JSON string simulating the parsed YAML data
    const char* jsonConfig = R"json({
        "LED_PIN": 2,
        "PWM_FREQUENCY": 5000,
        "START_HOUR": 10,
        "ON_DURATION": 5,
        "OFF_DURATION": 2
    })json";

    // Load JSON data into flash memory
    if (loadConfigToFlash(jsonConfig)) {
        Serial.println("Configuration saved to flash memory.");
    } else {
        Serial.println("Failed to save configuration to flash memory.");
    }

    // Load data from flash memory for testing
    int ledPin = preferences.getInt("LED_PIN", -1); // Default to -1 if not found
    int pwmFreq = preferences.getInt("PWM_FREQUENCY", -1);
    Serial.printf("Loaded LED_PIN: %d, PWM_FREQUENCY: %d\n", ledPin, pwmFreq);
}

bool loadConfigToFlash(const char* jsonConfig) {
    // Begin preferences with a unique namespace
    if (!preferences.begin("my-app", false)) {
        Serial.println("Failed to initialize preferences");
        return false;
    }

    // Parse JSON data
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, jsonConfig);
    if (error) {
        Serial.print("JSON deserialization failed: ");
        Serial.println(error.c_str());
        preferences.end();
        return false;
    }

    // Store parameters in flash memory
    preferences.putInt("LED_PIN", doc["LED_PIN"] | 0);
    preferences.putInt("PWM_FREQUENCY", doc["PWM_FREQUENCY"] | 0);
    preferences.putInt("START_HOUR", doc["START_HOUR"] | 0);
    preferences.putInt("ON_DURATION", doc["ON_DURATION"] | 0);
    preferences.putInt("OFF_DURATION", doc["OFF_DURATION"] | 0);

    preferences.end(); // Close preferences
    return true;
}

void loop() {
    // Your loop code here
}
