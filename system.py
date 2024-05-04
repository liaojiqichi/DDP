import subprocess
import argparse
import time
import re
import joblib
import numpy as np
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
    gpu_used = None
    gpu_used = int(data.split()[0].split(':')[1])
    return gpu_used
    
def extract_batch_size(data):
    batch_size = None
    batch_size_str = data.split("Batch size is ")[1].strip()
    batch_size = int(batch_size_str.rstrip('.'))
    return batch_size
   
def extract_model_size(data):
    model_size = None
    parts = data.split()
    model_size = float(parts[4])
    return model_size


def training(model,batch):
    sm_utilization = None 
    try:
        start_time = time.time()
        script_process = subprocess.Popen(['python3', 'training.py', '--gpu', '0', '-b', str(batch), '-a', model, 'cifar'])
    
        while time.time() - start_time < 10:
            if script_process.poll() is not None:
                break
                
        with open("/DDP/data.txt", "r") as file:
            data = file.read()
            kv_blocks = extract_values(data)
        with open("/DDP/data1.txt", "r") as file1:
            data1 = file1.read()
            batch_size = extract_batch_size(data1)
        with open("/DDP/data2.txt", "r") as file2:
            data2 = file2.read()
            model_size = extract_model_size(data2)
        
        sm_utilization = run_nvidia_smi()
    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping the data collection.")
        script_process.terminate()
        script_process.wait()
    return kv_blocks, batch_size, model_size, sm_utilization, script_process
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run training with given model and threshold.")
    parser.add_argument("-m", "--model", default='vgg19', type=str, help="Model name")
    parser.add_argument("-t", "--threshold", default=0.3, type=float, help="Threshold for comparison with y_pred")
    parser.add_argument("-b", "--batch_size", default=128, type=int, help="Batch size")

    args = parser.parse_args()
    
    model = args.model
    threshold = args.threshold
    batch = args.batch_size
    if model is None or threshold is None:
        print("Please provide both model name and threshold.")
    else:
        sm_origin = run_nvidia_smi()
        print(sm_origin)
        kv_blocks, batch_size, model_size, sm_new, script_process = training(model,batch)
        print(sm_new)
        sm_escalating = (sm_new - sm_origin)/sm_origin
        # Load the trained linear regression model from file
        loaded_model = joblib.load('linear_regression_model.pkl')
        X_new = [[kv_blocks, batch_size, model_size, sm_escalating]]
        y_pred = loaded_model.predict(X_new)
        print("Predicted output:", y_pred)
        if y_pred[0] >= threshold:
            print("Threshold exceeded. Terminating training.")
            script_process.terminate()
            script_process.wait()
        else:
            print("Threshold not exceeded. Continuing training.")
    

