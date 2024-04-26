import subprocess
import time
import re

def run_nvidia_smi():
    result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,clocks.sm,clocks.max.sm,timestamp','--format=csv,noheader,nounits'], capture_output=True, text=True)
    sm_info = result.stdout.strip().split(',')
    timestamp = sm_info[-1]
    gpu_utilization = sm_info[0]
    sm_clock = sm_info[1]
    max_sm_clock = sm_info[2]
    sm_utilization = float(gpu_utilization)*int(sm_clock)/int(max_sm_clock)
    return sm_utilization

def extract_values(data):
    gpu_used = none
    lines = data.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith('Receive'):
            if i + 4 < len(lines):
                gpu_used = (int(lines[i + 3].split()[0].split(':')[1].strip()))
    return gpu_used
    
def extract_batch_size(data):
    batch_szie = none
    parts = data.split()
    batch_size = parts[3]
    return batch_size
    
def extract_convolutional_layer(data):
    convolutional_layer = none
    match = re.search(r'vgg(\d+)', data)
    if match:
        convolutional_layer = int(match.group(1))
    return convolutional_layer


def training(model):
    sm_utilization = None 
    try:
        start_time = time.time()
        script_process = subprocess.Popen(['python3', 'training1.py', '--gpu', '0', '-a', model, 'cifar'])
    
        while time.time() - start_time < 10:
            if script_process.poll() is not None:
                break
                
        with open("data.txt", "r") as file:
            data = file.read()
            kv_blocks = extract_values(data)
        with open("data1.txt", "r") as file1:
            data1 = file1.read()
            batch_size = extract_batch_size(data1)
        with open("data2.txt", "r") as file2:
            data2 = file2.read()
            convolutional_layer = extract_convolutional_layer(data2)
        
        sm_utilization = run_nvidia_smi()
        script_process.terminate()
        script_process.wait()
    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping the data collection.")
        script_process.terminate()
        script_process.wait()
    return sm_utilization
  
if __name__ == "__main__":
    model = 'vgg19'
    sm_origin = run_nvidia_smi()
    print(sm_origin)
    sm_new = training(model)
    print(sm_new)
    sm_degradation = (sm_origin - sm_new)/sm_origin
    model.load("model.pkl")
