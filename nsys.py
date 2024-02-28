import subprocess
import time
import tempfile

def run_nsight_system(interval, duration, python_executable, script_name):
    # Construct the full command to run the Python script with python3
    command_to_run = f"{python_executable} {script_name}"

    # Create a temporary file to store the nsight system output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
        tmp_file_path = tmp_file.name

        # Start nsight system in a separate process with output redirected to the temporary file
        nsight_system_command = f"nsys profile -t cuda,osrt,mpi --output {tmp_file_path} {command_to_run}"
        nsight_system_process = subprocess.Popen(nsight_system_command, shell=True)

        try:
            for _ in range(duration // interval):
                time.sleep(interval)

            # Terminate nsight system process after the specified duration
            nsight_system_process.terminate()
            nsight_system_process.wait()

            # Print the captured output file path for reference
            print(f"Nsight Systems output saved to: {tmp_file_path}")

        except KeyboardInterrupt:
            # Handle keyboard interrupt (Ctrl+C) gracefully
            print("Keyboard interrupt detected. Terminating nsight system.")
            nsight_system_process.terminate()
            nsight_system_process.wait()

if __name__ == "__main__":
    interval = 2  # Interval in seconds
    duration = 100  # Duration in seconds
    python_executable = "/usr/bin/python3"  # Replace with your Python 3 executable path
    script_name = "/DDP/shell.py"  # Replace with the actual path to your Python script

    # Start nsight system and capture the output directly
    run_nsight_system(interval, duration, python_executable, script_name)
