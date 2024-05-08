import subprocess
import time
import csv

def run_nvidia_smi(interval, duration, script_name):
    try:
        script_process = subprocess.Popen(['python3', script_name])

        for _ in range(duration // interval):
            result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,utilization.memory,clocks.sm,clocks.max.sm,timestamp',
                                     '--format=csv,noheader,nounits'], capture_output=True, text=True)

            sm_info = result.stdout.strip().split(',')
            timestamp = sm_info[-1]
            gpu_utilization = sm_info[0]
            memory_utilization = sm_info[1]
            sm_clock = sm_info[2]
            max_sm_clock = sm_info[3]
            sm_utilization = int(gpu_utilization)*int(sm_clock)/int(max_sm_clock)

            csv_writer.writerow([timestamp, gpu_utilization, memory_utilization, sm_clock, max_sm_clock, sm_utilization])

            print(result.stdout)

            time.sleep(interval)

        script_process.terminate()
        script_process.wait()

        print("Data collection finished.")

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping the data collection.")
        script_process.terminate()
        script_process.wait()

if __name__ == "__main__":
    interval = 1
    duration = 7200
    script_name = "shell.py"

    run_nvidia_smi(interval, duration, script_name)
