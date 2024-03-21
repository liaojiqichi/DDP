import subprocess
import time

def collect_sm_info(interval, duration, output_file):
    try:
        with open(output_file, 'w') as f:
            for _ in range(duration // interval):
                # Run nvidia-smi and collect SM information
                result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,utilization.memory,clocks.sm,clocks.max.sm,timestamp',
                                         '--format=csv,noheader,nounits'], capture_output=True, text=True)

                # Write SM information to the output file
                f.write(result.stdout)

                # Sleep for the specified interval
                time.sleep(interval)
    except KeyboardInterrupt:
        print("Data collection stopped due to keyboard interrupt.")

def main():
    # Start collecting SM information in the background
    interval = 5  # Interval in seconds
    duration = 3600  # Duration in seconds
    output_file = "sm_info.csv"  # Output file name

    sm_process = subprocess.Popen(['python3', 'tsmi_print.py', str(interval), str(duration), output_file])

    # Start training task
    training_process = subprocess.Popen(['python3', 'training.py', 'cifar'])

    # Wait for the training task to finish
    training_process.communicate()

    # Terminate the SM information collection process
    sm_process.terminate()
    sm_process.wait()
    print("Training and data collection finished.")

if __name__ == "__main__":
    main()
