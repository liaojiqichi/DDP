import subprocess
import time
import requests

def run_nvidia_smi(interval, duration, output_file):
    try:
        with open(output_file, 'w') as f:
            for _ in range(duration // interval):
                # Run nvidia-smi command and capture the output
                subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,utilization.memory',
                                '--format=csv,noheader,nounits'], stdout=f, text=True)

                # Execute your inference script (shell.py) here
                # For simplicity, let's assume shell.py is just sleeping for 1 second
                subprocess.run(['python3', 'shell.py'])

                # Sleep for the specified interval
                time.sleep(interval)
        print("Data collection finished. Check the output file:", output_file)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping the data collection.")

if __name__ == "__main__":
    interval = 2  # Interval in seconds
    duration = 100  # Duration in seconds
    output_file = "nvidia_smi_output.csv"

    run_nvidia_smi(interval, duration, output_file)
