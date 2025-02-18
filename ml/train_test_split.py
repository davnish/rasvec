import glob
import os
import random
import shutil

img_list = [i for i in glob.glob(r"data_raw\patched_cln\images" + "/*.tif")]
label_list = [i for i in glob.glob(r"data_raw\patched_cln\labels" + "/*.tif")]

def shuffle_data(img_list, label_list):
    paired_list = list(zip(img_list, label_list))
    random.shuffle(paired_list)
    img_list, label_list = zip(*paired_list)
    return img_list, label_list

def train_test_split(img_list, label_list, train_size):
    img_list, label_list = shuffle_data(img_list, label_list)
    train_size = int(len(img_list) * train_size)
    print(f'Train Size: {train_size}, Test Size: {len(img_list)-train_size}')
    train_data = img_list[:train_size]
    train_label = label_list[:train_size]

    test_data = img_list[train_size:]
    test_label = label_list[train_size:]

    return train_data, train_label, test_data, test_label

def get_label_path(img_path):
    filename = os.path.basename(img_path)
    label_path = os.path.split(os.path.split(img_path)[0])[0] + rf'\label\{filename}'
    return label_path

def copy_files(file_list, dest):
    for file in file_list:
        shutil.copy(file, dest)

trainx, trainy, testx, testy = train_test_split(img_list, label_list, 0.8)

copy_files(trainx, r"data\train\data")
copy_files(trainy, r"data\train\label")
copy_files(testx, r"data\val\data")
copy_files(testy, r"data\val\label")