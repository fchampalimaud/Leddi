# Leddi - Lighting Control System

### Overview
Leedi is a programmable LED light control system designed to manage lighting schedules using an internal Real-Time Clock (RTC). This system synchronizes the clock via serial communication, enabling automatic time updates to maintain consistent schedules. The schedules are stored in the microcontroller's flash memory, allowing the system to operate autonomously. This makes Leedi particularly useful for applications such as circadian rhythm studies.

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
