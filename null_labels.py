import os
import glob
import shutil
from PIL import Image
import numpy as np
import random

def remove_null():
    data_paths = {
            'train': r"data\train\data", 
            'label_train': r"data\train\label",
            'val': r"data\val\data",
            'label_val': r"data\val\label"
            }
    
    label_paths_train = [i for i in glob.glob(data_paths['label_train'] + "/*.tif")]
    label_paths_validation = [i for i in glob.glob(data_paths['label_val'] + "/*.tif")]

    train_null = []
    val_null = []
    for idx, which_label in enumerate([label_paths_train, label_paths_validation]):
        
        for path in which_label:
            label = Image.open(path)
            label = np.asarray(label)
            filename = os.path.basename(path)
    
            if label.sum() == 0 :
                try:
                    os.remove(path)
                    if idx == 0:
                        os.remove(os.path.join(data_paths['train'], f'{filename}'))
                        train_null.append(filename)
                    else:
                        os.remove(os.path.join(data_paths['val'], f'{filename}'))
                        val_null.append(filename)
                        
                except:
                    continue
    return train_null, val_null

def seg_null_and_data(data_path):
    """
    This function will remove the files which have null values in them
    data+labels

    the data_path should be the path of the folder containing the images and labels
    """
    # data_path = [i for i in glob.glob(data_path + "images/*.tif")]

    null_label = []
    nonnull_label = []
    label_path = [i for i in glob.glob(data_path + r'/labels/*.tif')]

    for path in label_path:
        label = Image.open(path)
        label = np.asarray(label)

        if label.sum() == 0 :

            null_label.append(path)
            # try:
            #     shutil.copy(path, os.path.join(output_path, 'labels'))
            #     shutil.copy(os.path.join(data_path, 'images', f'{filename}'), os.path.join(output_path, 'images'))
            # except:
            #     continue
        else:
            nonnull_label.append(path)
    return nonnull_label, null_label

def keep_list_ratio(null_label, ratio):
    random.shuffle(null_label)
    return null_label[:int(len(null_label)*ratio)]


def get_label_path(img_path):
    filename = os.path.basename(img_path)
    label_path = os.path.split(os.path.split(img_path)[0])[0] + rf'\label\{filename}'
    return label_path

def copy_files(file_list, dest):
    # os.mkdir()
    for file in file_list:
        filename = os.path.basename(file)

        shutil.copy(file, os.path.join(dest, 'labels'))
        shutil.copy(os.path.join('data_raw', 'patched', 'images', f'{filename}'), os.path.join(dest, 'images'))


if __name__ == "__main__":


    train_null, val_null =  remove_null()
    print(train_null, val_null)
    # nonnull_label, null_label = seg_null_and_data(r"data_raw\patched")

    # null_label = keep_list_ratio(null_label, 0.3)



    # comb_data = [*nonnull_label, *null_label]



    # copy_files(comb_data, r"data_raw\patched_cln")