#include <Preferences.h>

Preferences preferences;

// Variables to store loaded configuration
int cycles;
int delayBeforeStart;
int fadeInDuration;
int fadeOutDuration;
int offDuration;
int onDuration;
String startTime;

void setup() {
  Serial.begin(115200);
  Serial.println("Loading configuration...");
  while (!Serial);  // Wait for the serial connection

  // Initialize preferences with the same namespace
  preferences.begin("config", true);  // `true` means read-only mode

  // Load each parameter
  cycles = preferences.getInt("cycles", -1);  // -1 is the default if not found
  delayBeforeStart = preferences.getInt("delay_before_start", -1);
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
}
