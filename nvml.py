import pynvml
import subprocess
import time

def collect_and_print_gpu_metrics(interval, duration, command_to_run):
    pynvml.nvmlInit()

    try:
        print("Time\tSM_Utilization\tSM_Occupancy")

        start_time = time.time()
        current_time = start_time

        while current_time - start_time < duration:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assuming one GPU, change index if needed

            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            occupancy_info = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)

            print(f"{current_time:.2f}\t{utilization.gpu}\t\t{occupancy_info.current}")

            time.sleep(interval)
            current_time = time.time()

    finally:
        pynvml.nvmlShutdown()

if __name__ == "__main__":
    interval = 2  # Interval in seconds
    duration = 60  # Duration in seconds
    command_to_run = "python shell.py"  # Replace with the actual command to run your inference script

    # Start collecting GPU metrics and print them during the inference process
    collect_and_print_gpu_metrics(interval, duration, command_to_run)
