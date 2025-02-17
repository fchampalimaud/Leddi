try {
    $uvVersion = uv --version
} catch {
    # If `uv` is not found, install it
    Write-Host "UV is not installed. Installing UV..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") # Update the PATH environment variable
}

$EnvPath = ".venv\Scripts\activate"
# Check if the virtual environment activation script exists
if (!(Test-Path $EnvPath)) {
    # If not found, run `uv` to create the virtual environment
    uv venv

    # Activate the virtual environment
    & $EnvPath

} else {
    # Activate the existing virtual environment
    & $EnvPath
}

# Define local directories for Arduino CLI configuration and libraries
$localArduinoDir = ".arduino"  # Local directory for Arduino CLI configuration
$localLibrariesDir = "$localArduinoDir\libraries"  # Local libraries directory
$localCoresDir = "$localArduinoDir\cores"  # Local cores directory

# Create local directories if they don't exist
if (!(Test-Path $localArduinoDir)) {
    New-Item -ItemType Directory -Path $localArduinoDir | Out-Null
}
if (!(Test-Path $localLibrariesDir)) {
    New-Item -ItemType Directory -Path $localLibrariesDir | Out-Null
}
if (!(Test-Path $localCoresDir)) {
    New-Item -ItemType Directory -Path $localCoresDir | Out-Null
}

# Check if arduino-cli.exe is already in the virtual environment's Scripts folder
if (!(Test-Path ".venv\Scripts\arduino-cli.exe")) {
    # If not, download and install arduino-cli
    Write-Host "Downloading arduino-cli..."
    Invoke-WebRequest "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip" -OutFile "temp.zip"

    Write-Host "Extracting arduino-cli to .venv\Scripts..."
    Expand-Archive "temp.zip" -DestinationPath ".venv\Scripts" -Force
    Remove-Item -Path "temp.zip"
}

# Ensure the arduino-cli.exe is in the correct location
if (Test-Path ".venv\Scripts\arduino-cli.exe") {
    Write-Host "arduino-cli installed successfully."

    # Create a custom configuration file for local installation
    $configFile = "$localArduinoDir\arduino-cli.yaml"
    if (!(Test-Path $configFile)) {
        Write-Host "Creating local Arduino CLI configuration file..."
        .venv\Scripts\arduino-cli.exe config init --dest-dir $localArduinoDir

        # Manually set the directories in the configuration file
        @"
directories:
  data: $localArduinoDir
  downloads: $localArduinoDir
  user: $localArduinoDir
  libraries: $localLibrariesDir
  packages: $localCoresDir
"@ | Set-Content -Path $configFile
    }

    # Update the library index
    Write-Host "Updating library index..."
    .venv\Scripts\arduino-cli.exe --config-file $configFile lib update-index

    # Install the ESP32 core locally
    Write-Host "Installing ESP32 core locally..."
    .venv\Scripts\arduino-cli.exe --config-file $configFile core install esp32:esp32@3.0.7

    # Install the ArduinoJson library locally
    Write-Host "Installing ArduinoJson library locally..."
    .venv\Scripts\arduino-cli.exe --config-file $configFile lib install "ArduinoJson"
} else {
    Write-Host "Error: arduino-cli.exe was not found after extraction."
}

# Activate the environment (adjust if using virtual environments)
uv run .\src\main.py
