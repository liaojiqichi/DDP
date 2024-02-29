import subprocess
import time
import requests

def run_nvidia_smi(interval, duration, output_file):
    try:
        with open(output_file, 'w') as f:
            for _ in range(duration // interval):
                # Run nvidia-smi command and capture the output
                result = subprocess.run(['nvidia-smi', '--query-gpu=timestamp,sm', '--format=csv,noheader,nounits'],
                                        stdout=subprocess.PIPE, text=True)

                # Write the result to the output file
                f.write(result.stdout)

                # Execute your inference script (shell.py) here
                # For simplicity, let's assume shell.py is just sleeping for 1 second
                subprocess.run(['python', 'shell.py'])

                # Sleep for the specified interval
                time.sleep(interval)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping the data collection.")

if __name__ == "__main__":
    interval = 2  # Interval in seconds
    duration = 100  # Duration in seconds
    output_file = "nvidia_smi_output.csv"

    run_nvidia_smi(interval, duration, output_file)
