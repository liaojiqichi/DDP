import subprocess
import time
import tempfile
import os

def run_nsight_compute(interval, duration, python_executable, script_name):
    # Construct the full command to run the Python script with python3
    command_to_run = f"{python_executable} {script_name}"

    # Create a temporary file to store the nsight compute output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
        tmp_file_path = tmp_file.name

        # Start nsight compute in a separate process with output redirected to the temporary file
        nsight_compute_command = f"nsys profile -t nvtx,mpi,cuda --output {tmp_file_path} {command_to_run}"
        nsight_compute_process = subprocess.Popen(nsight_compute_command, shell=True)
        
        try:
            for _ in range(duration // interval):
                time.sleep(interval)

            # Terminate nsight compute process after the specified duration
            nsight_compute_process.terminate()
            nsight_compute_process.wait()

            # Print the captured output file path for reference
            print(f"Nsight Compute output saved to: {tmp_file_path}")
            
        except KeyboardInterrupt:
            # Handle keyboard interrupt (Ctrl+C) gracefully
            print("Keyboard interrupt detected. Terminating nsight compute.")
            nsight_compute_process.terminate()
            nsight_compute_process.wait()

    # The output file is automatically saved by nsight compute, and you can analyze it separately

if __name__ == "__main__":
    interval = 2  # Interval in seconds
    duration = 100  # Duration in seconds
    python_executable = "/usr/bin/python3"  # Replace with your Python 3 executable path
    script_name = "/DDP/shell.py"  # Replace with the actual path to your Python script

    # Start nsight compute and capture the output directly
    run_nsight_compute(interval, duration, python_executable, script_name)
