import subprocess
import argparse
import time
import re
import joblib

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
    gpu_used = int(data.split()[0].split(':')[1])
    return gpu_used
    
def extract_batch_size(data):
    batch_size = none
    batch_size_str = data.split("Batch size is ")[1].strip()
    batch_size = int(batch_size_str.rstrip('.'))
    return batch_size
    
def extract_model_size(data):
    model_size = none
    parts = data.split()
    model_size = parts[4]
    return model_size


def training(model):
    sm_utilization = none 
    try:
        start_time = time.time()
        script_process = subprocess.Popen(['python3', 'training.py', '--gpu', '0', '-a', model, 'cifar'])
    
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
            model_size = extract_model_size(data2)
        
        sm_utilization = run_nvidia_smi()
    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping the data collection.")
        script_process.terminate()
        script_process.wait()
    return kv_blocks, batch_size, model_size, sm_utilization, script_process
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run training with given model and threshold.")
    parser.add_argument("-m", "--model", type=str, help="Model name")
    parser.add_argument("-t", "--threshold", type=float, help="Threshold for comparison with y_pred")

    args = parser.parse_args()

    model = args.model
    threshold = args.threshold

    if model is None or threshold is None:
        print("Please provide both model name and threshold.")
    else:
        sm_origin = run_nvidia_smi()
        print(sm_origin)
        kv_blocks, batch_size, model_size, sm_new, script_process = training(model)
        print(sm_new)
        sm_degradation = (sm_origin - sm_new)/sm_origin

        # Load the trained linear regression model from file
        loaded_model = joblib.load('linear_regression_model.pkl')
        X_new = [0,0,0,0]
        X_new[0] = kv_blocks
        X_new[1] = batch_size
        X_new[2] = model_size
        X_new[3] = sm_degradation
        y_pred = loaded_model.predict(X_new)
        print("Predicted output:", y_pred)
        if y_pred[0] >= threshold:
            print("Threshold exceeded. Terminating training.")
            script_process.terminate()
            script_process.wait()
        else:
            print("Threshold not exceeded. Continuing training.")
    

