import csv

# Read the CSV file
with open('C:/Users/fyp/Desktop/sm_info5.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file, delimiter='\t')
    # Initialize an empty list to store the lines
    lines = []
    # Iterate over each row in the CSV file
    for row in reader:
        # Join the elements of the row with a tab separator
        line = '\t'.join(row)
        # Append the line to the list of lines
        lines.append(line)

# Join the lines with newline characters to create the data string
data_string = '\n'.join(lines)


# Split the data string by lines
lines = data_string.split('\n')

# Initialize an empty list to store the extracted data
sm_data = []

# Iterate over each line
for line in lines:
    # Split each line by tab (\t)
    parts = line.split('\t')[0].split(',')
    #print(parts)
    # Check if the line has enough parts
    if len(parts) >= 5:
        # Extract SM utilization and time
        sm_utilization = int(parts[1])
        time_parts = parts[0].split(' ')[2].split(':')
        #Round off the seconds part of the time
        seconds = int(float(time_parts[2]))
        #Convert hours, minutes, and seconds to total seconds
        total_seconds =(int(time_parts[1]) * 60) + seconds
        #Append to the extracted data list as a tuple
        sm_data.append((sm_utilization, total_seconds))

#print(sm_data)

# Open the .txt file
with open('C:/Users/fyp/Desktop/data5.txt', 'r') as file:
    # Read the lines
    lines = file.readlines()

# Initialize an empty list to store the extracted values
data_list = []


for line in lines:
    # Split the line by spaces
    parts = line.split()
    
    # Check if there are enough parts in the line
    if len(parts) >= 2:
        # Extract GPU_Used and Time is values
        gpu_used = parts[0].split(':')[1]
        time_is = parts[-2] + ' ' + parts[-1]
        
        # Append the values to the data list as a sublist
        data_list.append([gpu_used, time_is])
    else:
        print("Skipping line:", line)  # Print a message for lines with insufficient parts
        
# Initialize an empty list to store the extracted data
kv_blocks_data  = []

# Iterate over each sublist
for sublist in data_list:
    # Extract the GPU_Used value and convert it to an integer
    gpu_used = int(sublist[0])
    # Extract the time data and remove the "Time is:" prefix
    time_data = sublist[1].split(':')[-3:]
    # Round off the seconds to the nearest integer
    rounded_seconds = str(int(float(time_data[-1])))
    # Join the time components back together
    rounded_time = ':'.join(time_data[:-1]) + ':' + rounded_seconds
    # Append a tuple containing the GPU_Used value and the time data to the extracted data list
    time_parts = rounded_time.split(':')
    total_seconds = (int(time_parts[1]) * 60) + int(float(time_parts[2]))
    kv_blocks_data.append((gpu_used, total_seconds))

# Print the resulting list of tuples
#print(kv_blocks_data)


from scipy.interpolate import interp1d

# Assuming sm_data and kv_data are your lists of tuples
sm_values, sm_times = zip(*sm_data)
kv_blocks_values, kv_blocks_times = zip(*kv_blocks_data)

# Interpolate SM data to match KV times
f = interp1d(sm_times, sm_values, kind='linear', fill_value='extrapolate')
interpolated_sm_values = f(kv_blocks_times)

# Convert interpolated SM values to integers
interpolated_sm_values = [int(value) for value in interpolated_sm_values]

# Now you have interpolated SM values that match the timestamps of KV blocks data
print(interpolated_sm_values)


# Define the file path for the CSV file
file_path = "sm5.csv"

# Write the interpolated SM values to the CSV file
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write each value as a row in the CSV file
    for value in interpolated_sm_values:
        writer.writerow([value])

print("Interpolated SM values saved to:", file_path)