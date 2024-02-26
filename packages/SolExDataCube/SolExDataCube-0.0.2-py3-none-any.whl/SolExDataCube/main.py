from os.path import isfile, join
from os import listdir
import os
import numpy as np

def Dir_Read(key, path = None):
    if path: os.chdir(path)
    if key == 's':
        onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
        return onlyfiles
    else:
        folder = [f for f in listdir(os.getcwd()) if not isfile(join(os.getcwd(), f))]
        return folder

def padding(arr, pad_size, pad_freq):
    rows, cols = arr.shape
    padded_rows = (rows //pad_freq) * pad_size + rows # Calculate the number of rows in the padded array
    transformed_2d_list = np.ones((padded_rows, cols), dtype=arr.dtype)
    # transformed_2d_list = transformed_2d_list *15000
    
    for i in range(pad_freq):
        transformed_2d_list[i::(pad_size + pad_freq)] = arr[i::pad_freq]

    # # Use slicing for efficient copying
    # transformed_2d_list[::(pad + pad_freq)] = arr[::pad_freq]
    # transformed_2d_list[1::(pad + pad_freq)] = arr[1::pad_freq]
    # transformed_2d_list[2::(pad + 1)] = arr[2::pad_freq]

    return transformed_2d_list









