import glob
import numpy as np
import os

def load_encode_file():
    path = "./encode/*"
    file_list = glob.glob(path)
    encode_files = []
    for file_str in file_list:
        encode_files.append(np.load(file_str))

    return encode_files

def save_encode_file(encoded_list):
    path = "./encode/"
    num = 1
    
    file_list = glob.glob(path+'*')
    if file_list:
        num = len(file_list)+1
    np.save(path+str(num).zfill(6),encoded_list)

#def empty_encode_file(path):
#    if os.path.isfile(path):
#        os.remove(path)