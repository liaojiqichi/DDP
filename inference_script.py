import subprocess
import time

def run_nvprof(interval, duration, output_file, command):
    # Start nvprof in a separate process with I/O redirection
    nvprof_command = f"nvprof --metrics sm_efficiency,achieved_occupancy --print-summary --csv -o {output_file} {command}"

    # Start nvprof in a separate process
    nvprof_process = subprocess.Popen(nvprof_command, shell=True)

    for _ in range(duration // interval):
        time.sleep(interval)

    # Terminate nvprof process after the specified duration
    nvprof_process.terminate()

if __name__ == "__main__":
    interval = 2  # Interval in seconds
    duration = 1000  # Duration in seconds
    output_file = "nvprof_output.csv"

    # Specify the command to run your Python script
    command_to_run = "shell.py"

    # Start nvprof in a separate process
    run_nvprof(interval, duration, output_file, command_to_run)
