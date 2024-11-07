import subprocess

# Specify board details
board_fqbn = "esp32:esp32:XIAO_ESP32S3"
port = "COM5"
source_file = "configuration/configuration.ino"

def compile_and_upload():
    try:
        # Compile the sketch
        print("Compiling the sketch...")
        compile_command = [
            "arduino-cli", "compile", "--fqbn", board_fqbn, source_file
        ]
        subprocess.run(compile_command, check=True)
        print("Compilation successful!")

        # Upload the sketch
        print("Uploading the sketch to the board...")
        upload_command = [
            "arduino-cli", "upload", "-p", port, "--fqbn", board_fqbn, source_file
        ]
        subprocess.run(upload_command, check=True)
        print("Upload successful!")

    except subprocess.CalledProcessError as e:
        print("An error occurred during compilation or upload.")
        print(e)

if __name__ == "__main__":
    compile_and_upload()
