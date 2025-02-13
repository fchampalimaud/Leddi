try {
    $uvVersion = uv --version
} catch {
    # If `uv` is not found, install it
    Write-Host "UV is not installed. Installing UV..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
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

# Check if arduino-cli.exe is already in the virtual environment's Scripts folder
if (!(Test-Path ".venv\Scripts\arduino-cli.exe")) {
    # If not, download and install arduino-cli
    Invoke-WebRequest "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip" -OutFile "temp.zip"
    Expand-Archive "temp.zip" -DestinationPath ".\.venv\Scripts" -Force
    Remove-Item -Path "temp.zip"

    arduino-cli lib update-index
    arduino-cli core install esp32:esp32@3.0.7
    .venv\Scripts\arduino-cli.exe lib install "ArduinoJson"
}

# Activate the environment (adjust if using virtual environments)
uv run .\src\main.py
