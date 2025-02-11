

# Leddi - Lighting Control System

### Overview
Leedi is a programmable LED light control system designed to manage lighting schedules using an internal Real-Time Clock (RTC). This system synchronizes the clock via serial communication, enabling automatic time updates to maintain consistent schedules. The schedules are stored in the microcontroller's flash memory, allowing the system to operate autonomously. This makes Leedi particularly useful for applications such as circadian rhythm studies.




#

Configure cycles and patterns respectivly. A cycle in one complete repetition of a pattern. 


for in vitro light stimulation, cells were
stimulated at 24 h after transfection with a 30 s ON and 30 s OFF blue
light pulse (470 nm, 0.1–4 mW/cm2
; ThorLabs, Newton, NJ, USA) unless
otherwise noted. Light cycles were programmed by connecting to a
DC2100 LED driver with pulse modulation (ThorLabs, Newton, NJ,
USA). The light intensity was measured by using an optical power
meter from ThorLabs (Newton, NJ, USA)


# **Installation Instructions**

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




# **Usage Instructions**  

## **1. Connect the Device**  
- Plug the **Leedi** device into your computer using a **USB** cable.  

## **2. Launch the Application**  
1. Open **PowerShell** (or your preferred terminal).  
2. Navigate to the directory where the program is installedand run:  

   ```bash
   ./run_leddi.cmd
   ```  

## **3. Establish Connection**  
- When the application window opens, select the correct **COM port** for your device.  
- Click `Connect` and wait for the status to change from **Not Connected** to **Connected** (this may take up to **30 seconds**).  
  - During this time, the interface may be **unresponsive**.  

## **4. Configure Settings**  
- Adjust the **main settings** and **lighting patterns** as needed.  
- (Optional) Load a pre-saved configuration from a **JSON file**.  

## **5. Preview (Optional)**  
- Click `Generate Plot` to visualize the lighting pattern before applying it.  

## **6. Apply Configuration**  
- Press `Configure` to upload the settings to the device.  

## **7. Safely Disconnect**  
- Close the application window.  
- Wait **30 seconds** before unplugging the device to ensure proper shutdown.  

---
