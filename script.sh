#!/bin/bash
#
# Script to extract CIFAR-10 dataset
# CIFAR-10 dataset contains the following files:
#   - cifar-10-batches-py/data_batch_1
#   - cifar-10-batches-py/data_batch_2
#   - ...
#   - cifar-10-batches-py/data_batch_5
#   - cifar-10-batches-py/test_batch
#
# Make CIFAR-10 directory
#
mkdir cifar10
cd cifar10

# Download the CIFAR-10 dataset (binary version)
wget https://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz

# Extract the dataset
tar -xzvf cifar-10-binary.tar.gz

# Remove the compressed file
rm -f cifar-10-binary.tar.gz

# Change directory to the extracted folder
cd cifar-10-batches-bin

# Move all files to the parent directory
mv * ../

# Remove the extracted folder
cd ..
rm -rf cifar-10-batches-bin

# Change back to the original directory
cd ..
