

# Leddi - Lighting Control System

### Overview
Leedi is a programmable LED light control system designed to manage lighting schedules using an internal Real-Time Clock (RTC). This system synchronizes the clock via serial communication, enabling automatic time updates to maintain consistent schedules. The schedules are stored in the microcontroller's flash memory, allowing the system to operate autonomously. This makes Leedi particularly useful for applications such as circadian rhythm studies.


## Features


## Requirements
- **Hardware**: Seeed Studio XIAO ESP32S3 microcontroller.
- **Software**: Arduino CLI installed on your computer. [Installation guide for Arduino CLI](https://arduino.github.io/arduino-cli/0.24/installation/)

### Getting Started
To compile and upload the code for the Lighting Control System to the Seeed Studio XIAO ESP32S3 microcontroller on COM5, you’ll need to use the Arduino CLI.



#### 1. Set up the Seeed Studio XIAO ESP32S3 Board Definition
To ensure that Arduino CLI recognizes the Seeed Studio XIAO ESP32S3, add the ESP32 core to Arduino CLI with these commands:

```bash
arduino-cli core update-index
arduino-cli core install esp32:esp32
```

