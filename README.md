# **Leddi - Lighting Control System**

## **Overview**
Leddi is a programmable LED light control system designed to manage lighting schedules using an internal Real-Time Clock (RTC). This system synchronizes the clock via serial communication, enabling automatic time updates to maintain consistent schedules. The schedules are stored in the microcontroller's flash memory, allowing the system to operate autonomously. This makes Leddi particularly useful for applications such as circadian rhythm studies.

## **Usage Instructions**  

### **1. Connect the Device**  
- Plug the **Leddi** device into your computer using a **USB** cable.   


### **2. Launch the Application**  
1. Open **PowerShell** (or your preferred terminal).  
2. Navigate to the directory where the program is installedand run:  

   ```bash
   ./run_leddi.cmd
   ```  

### **3. Establish Connection**  
- When the application window opens, select the correct **COM port** for your device.  
- Click `Connect` and wait for the status to change from **Not Connected** to **Connected** (this may take up to **30 seconds**).  
  - During this time, the interface may be **unresponsive**.  

### **4. Configure Settings**  
- Adjust the **main settings** and **lighting patterns** as needed.  
- (Optional) Load a pre-saved configuration from a **JSON file**.  

### **5. Preview (Optional)**  
- Click `Generate Plot` to visualize the lighting pattern before applying it.  

### **6. Apply Configuration**  
- Press `Configure` to upload the settings to the device.  

### **7. Safely Disconnect**  
- Close the application window.  
- Wait **30 seconds** before unplugging the device to ensure proper shutdown.  

---

## **Code Organization**

#### Root Directory
- **`.gitignore`**
- **`.python-version`**: Indicates the Python version used for the project.
- **`config.json`**: Default configuration file for the application.
- **`config_2.json`**: Alternate configuration file (optional).
- **`pyproject.toml`**: Configuration file for Python project dependencies and build settings.
- **`README.md`**
- **`run_leddi.cmd`**: Windows command script to run the application.
- **`run_leddi.ps1`**: Windows PowerShell script to run the application.
- **`uv.lock`**: Lock file for dependency management.

---

#### `src` Directory
Contains the main source code for the application.

- **`ino_utils.py`**: Utility functions for working with `.ino` files.
- **`interface_pysite.py`**: Main graphical user interface (GUI) implementation for the application.
- **`json_utils.py`**: Utility functions for reading, writing, and manipulating JSON files.
- **`main.py`**: Entry point for the application. Initializes and runs the GUI.
- **`serial_esp32.py`**: Handles serial communication with the ESP32 device (e.g., connecting, sending/receiving data).

---

#### `src/configuration` and `src/cycle`
Contains firmware-related files for the ESP32 device.

- **`configuration.ino`**: Arduino sketch for configuring the ESP32 device, including syncing the RTC with the computer's clock and saving the light pattern configuration onto the flash memory.
- **`cycle.ino`**: Arduino sketch for controlling the light cycle.

---