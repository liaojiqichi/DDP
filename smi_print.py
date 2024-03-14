import subprocess
import time

def run_nvidia_smi(interval, duration, script_name):
    try:
        # Start the shell.py script in a separate process
        script_process = subprocess.Popen(['python3', script_name])

        for _ in range(duration // interval):
            # Run nvidia-smi and print the SM information to the command line
            result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,utilization.memory,clocks.sm,clocks.max.sm,timestamp',
                                     '--format=csv,noheader,nounits'], capture_output=True, text=True)

            # Print the collected SM information
            print(result.stdout)

            # Sleep for the specified interval
            time.sleep(interval)

        # Terminate the script process after the specified duration
        script_process.terminate()
        script_process.wait()

        print("Data collection finished.")

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping the data collection.")
        script_process.terminate()
        script_process.wait()

if __name__ == "__main__":
    interval = 2  # Interval in seconds
    duration = 100  # Duration in seconds
    script_name = "shell.py"  # Replace with the actual path to your Python script

    run_nvidia_smi(interval, duration, script_name)
