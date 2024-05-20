import subprocess
import time
import csv

def run_nvidia_smi(interval, duration, script_name, output_file):
    try:
        # Start the shell.py script in a separate process
        script_process = subprocess.Popen(['python3', script_name, 'cifar'])

        # Open the CSV file for writing
        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            for _ in range(duration // interval):
                # Run nvidia-smi and collect the SM information
                result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,utilization.memory,clocks.sm,clocks.max.sm,timestamp',
                                         '--format=csv,noheader,nounits'], capture_output=True, text=True)

                # Parse the collected SM information
                sm_info = result.stdout.strip().split(',')
                timestamp = sm_info[-1]
                gpu_utilization = sm_info[0]
                memory_utilization = sm_info[1]
                sm_clock = sm_info[2]
                max_sm_clock = sm_info[3]

                # Write the data to the CSV file
                csv_writer.writerow([timestamp, gpu_utilization, memory_utilization, sm_clock, max_sm_clock])

                # Print the collected SM information
                print(timestamp, gpu_utilization, memory_utilization, sm_clock, max_sm_clock)

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
    interval = 1  # Interval in seconds
    duration = 7200  # Duration in seconds
    script_name = "training.py"  # Replace with the actual path to your Python script
    output_file = "sm_info.csv"  # Output CSV file name

    run_nvidia_smi(interval, duration, script_name, output_file)
