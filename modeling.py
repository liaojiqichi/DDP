from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import csv
import joblib

def extract_sm(reader):
    lines = []
    for row in reader:
        line = '\t'.join(row)
        lines.append(line)

    data_string = '\n'.join(lines)

    lines = data_string.split('\n')

    sm_utilization = []

    for line in lines:
        parts = line.split('\t')[0].split(',')
        if len(parts) >= 5:
            sm_utilization.append(float(parts[5]))

    return sm_utilization

def extract_data(file):

    lines = file.readlines()

    gpu_used = []
    batch_size = None
    batch_sizes = []
    model_size = None
    model_sizes = []
    avg_generation_throughputs = []

    for line in lines:
        if "Batch size is" in line:
            batch_size_str = line.split("Batch size is ")[1].strip()
            batch_size = int(batch_size_str.rstrip('.'))
        elif "Model size (MB) is" in line:
            model_size = float(line.split("Model size (MB) is ")[1].strip())
        elif "GPU_Used:" in line:
            gpu_used.append(int(line.split("GPU_Used:")[1].split()[0]))
            batch_sizes.append(batch_size)
            model_sizes.append(model_size)
        elif "Avg generation throughput" in line:
            avg_gen_throughput = line.split(": ")[2]
            avg_generation_throughputs.append(float(avg_gen_throughput))

    return gpu_used, batch_sizes, model_sizes, avg_generation_throughputs

def extract_info(file):

    lines = file.readlines()

    avg_generation_throughputs = []

    for line in lines:
        if "Avg generation throughput" in line:
            avg_gen_throughput = line.split(": ")[2]
            avg_generation_throughputs.append(float(avg_gen_throughput))

    return avg_generation_throughputs

with open("data.txt", "r") as file:
    throughput = extract_info(file)

with open("data50.txt", "r") as file1:
    gpu_used1, batch_size1, model_size1, throughput1 = extract_data(file1)

for i in range(len(throughput)):
    if throughput[i] < 2:
        throughput[i] = throughput[i] + 40

for i in range(len(throughput1)):
    if throughput1[i] < 2:
        throughput1[i] = throughput1[i] + 40

with open('sm_info.csv', 'r') as file2:
    reader = csv.reader(file2, delimiter='\t')
    sm_data = extract_sm(reader)

with open('GPU_info.csv', 'r') as file3:
    reader1 = csv.reader(file3, delimiter='\t')
    sm_data1 = extract_sm(reader1)

num_bins = len(throughput)

rep_points = np.interp(np.linspace(0, len(sm_data)-1, num_bins), np.arange(len(sm_data)), sm_data)
rep_points1 = np.interp(np.linspace(0, len(sm_data1)-1, num_bins), np.arange(len(sm_data1)), sm_data1)


sm_escalating_rate = []
for i in range(len(rep_points)):
    sm_escalating_rate.append((rep_points1[i]-rep_points[i])/rep_points[i])

throughput_reduction_rate = []
for i in range(len(throughput)):
    throughput_reduction_rate.append((throughput[i]-throughput1[i])/throughput[i])




x = []

for i in range(len(throughput)):
    row = [0, 0, 0, 0]
    row[0] = gpu_used1[i]
    row[1] = batch_size1[i]
    row[2] = model_size1[i]
    row[3] = sm_escalating_rate[i]
    
    x.append(row)

y = throughput_reduction_rate

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)



linear_regressor = LinearRegression()

linear_regressor.fit(X_train, y_train)

y_pred = linear_regressor.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)


joblib.dump(linear_regressor, 'linear_regression_model.pkl')


random_forest_regressor = RandomForestRegressor()

random_forest_regressor.fit(X_train, y_train)

y_pred_rf = random_forest_regressor.predict(X_test)

mse_rf = mean_squared_error(y_test, y_pred_rf)
print("Random Forest Mean Squared Error:", mse_rf)

gradient_boosting_regressor = GradientBoostingRegressor()

gradient_boosting_regressor.fit(X_train, y_train)

y_pred_gb = gradient_boosting_regressor.predict(X_test)

mse_gb = mean_squared_error(y_test, y_pred_gb)
print("Gradient Boosting Mean Squared Error:", mse_gb)

