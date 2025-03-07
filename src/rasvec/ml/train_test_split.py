import glob
import os
import random
import shutil

def shuffle_data(img_list, label_list):
    paired_list = list(zip(img_list, label_list))
    random.shuffle(paired_list)
    img_list, label_list = zip(*paired_list)
    return img_list, label_list

def get_label_path(img_path):
    filename = os.path.basename(img_path)
    label_path = os.path.split(os.path.split(img_path)[0])[0] + rf'\label\{filename}'
    return label_path

def copy_files(file_list, dest):
    for file in file_list:
        shutil.copy(file, dest)

def train_test_split(data_path, label_path, train_size, split_path=None):
    """ This split the dataset whcih consist of data and label into training and testing set.
        Note: This wont work if there are mutiple directories inside data_path or label_path
    Args:
        data_path (str): Path consisting the data.
        label_path (str): Path consisting the labels.
        train_size (float): Ratio of the train_size. Range from 0 - 1.
        split_path (str, optional): If this is provided the data and label and splited and transfered to this directory.
                                    Defaults to None.

    Returns:
        list (str): training_data, training_label, testing_data, testing_label.
    """
    img_list = [i for i in glob.glob(os.path.join(data_path + "/*.tif"))]
    label_list = [i for i in glob.glob(os.path.join(label_path + "/*.tif"))]

    img_list, label_list = shuffle_data(img_list, label_list)
    train_size = int(len(img_list) * train_size)
    print(f'Train Size: {train_size}, Test Size: {len(img_list)-train_size}')
    trainx = img_list[:train_size]
    trainy = label_list[:train_size]

    testx = img_list[train_size:]
    testy = label_list[train_size:]

    if split_path is not None:
            trainx_path = os.path.join(split_path, r'train\data')
            trainy_path = os.path.join(split_path, r'train\label')
            testx_path = os.path.join(split_path, r'val\data')
            testy_path = os.path.join(split_path, r'val\label')

            os.makedirs(trainx_path)
            os.makedirs(trainy_path)
            os.makedirs(testx_path)
            os.makedirs(testy_path)

            copy_files(trainx, r"data\train\data")
            copy_files(trainy, r"data\train\label")
            copy_files(testx, r"data\val\data")
            copy_files(testy, r"data\val\label")

    return trainx, trainy, testy, testy