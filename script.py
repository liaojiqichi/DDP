import os
import pickle
import numpy as np
from PIL import Image

# CIFAR-10 class names
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

def unpickle(file):
    with open(file, 'rb') as fo:
        data = pickle.load(fo, encoding='bytes')
    return data

def save_image(image_array, label, index, save_dir):
    class_dir = os.path.join(save_dir, class_names[label])
    os.makedirs(class_dir, exist_ok=True)
    image = Image.fromarray(image_array)
    image.save(os.path.join(class_dir, f'{index}.png'))

def process_data_batch(data_batch_file, save_dir):
    data = unpickle(data_batch_file)
    images = data[b'data']
    labels = data[b'labels']
    for i, (image, label) in enumerate(zip(images, labels)):
        image_array = np.transpose(np.reshape(image, (3, 32, 32)), (1, 2, 0))
        save_image(image_array, label, i, save_dir)

def convert_cifar_to_image_folder(data_dir, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    for i in range(1, 5):  # There are 5 data batches
        data_batch_file = os.path.join(data_dir, f'data_batch_{i}')
        process_data_batch(data_batch_file, save_dir)

# Usage example
cifar_data_dir = '/DDP/DDP/cifar-10-batches-py'
save_dir = '/DDP/DDP/cifar/train'
convert_cifar_to_image_folder(cifar_data_dir, save_dir)
