import subprocess

def compile_and_upload(board_fqbn, port, source_file):
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

        return True

    except subprocess.CalledProcessError as e:
        print("An error occurred during compilation or upload.")
        print(e)
        return False
