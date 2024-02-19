from vllm import LLM, SamplingParams
from datasets import load_dataset
import random
import subprocess
import time
import requests
import json
def run_nvprof(interval, duration, output_file):
    # Command to run nvprof and collect SM data at the specified interval
    nvprof_command = f"nvprof --metrics sm_efficiency,achieved_occupancy --print-summary --csv --interval={interval} --log-file={output_file}"

    # Start nvprof in a separate process
    nvprof_process = subprocess.Popen(nvprof_command, shell=True)

    # Sleep for the specified duration
    time.sleep(duration)

    # Terminate nvprof process after the specified duration
    nvprof_process.terminate()

def main():
    # Set parameters
    interval 2  # Interval in seconds
    duration = 100  # Duration in seconds (adjust as needed)
    output_file = "nvprof_output.csv"

    # Start nvprof in a separate process
    run_nvprof(interval, duration, output_file)

    dataset1 = load_dataset("nateraw/parti-prompts")
    dataset2 = load_dataset("succinctly/midjourney-prompts")

    while duration > 0:
        random_choose1 = random.randint(1, 1632)
        sentence1 = dataset1["train"]["Prompt"][random_choose1].split()
        len1 = random.randint(0, len(sentence1))
        part1 = random.choices(sentence1, k=len1)

        random_choose2 = random.randint(1, 12320)
        sentence2 = dataset2["test"]["text"][random_choose2].split()
        len2 = random.randint(0, len(sentence2))
        part2 = random.choices(sentence2, k=len2)

        prompts = ' '.join(part1 + part2)

        url = "http://0.0.0.0:8000/generate"
        data = {"prompt": prompts}  # Corrected data format

        res = requests.post(url, json=json.dumps(data))  # Use json parameter for sending JSON data

        print(res.text)

        time.sleep(1)
        duration -= 1

if __name__ == "__main__":
    main()
