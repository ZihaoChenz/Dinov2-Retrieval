import argparse
import os
from collections import defaultdict
from utils.txt_operation import load_txt_to_tensor
import numpy as np
from tqdm import tqdm
from pathlib import Path


# get a list contain all file path
def get_all_file_path(target_folder):
    file_list = []
    # walk all file path and save to list
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_list.append(os.path.join(root, file))

    return file_list

def get_cls_dict(file_list):
    # 初始化一个字典来保存结果
    result_dict = defaultdict(list)

    # 遍历文件列表
    for file_path in file_list:
        # 分割路径，提取倒数第三层目录和文件名称
        path_parts = file_path.split(os.sep)
        if "ref" in path_parts:  # 只考虑路径中包含'ref'的文件
            third_last_dir = path_parts[-3]  # 倒数第三层路径
            # 将文件路径添加到对应的key中
            result_dict[third_last_dir].append(file_path)

    # 将defaultdict转换为普通dict并打印结果
    result_dict = dict(result_dict)
    return result_dict

def embedding_process(result_dict):
    # create embedding dict to record each class ref txt file's tensor
    # embedding_dict = {}
    centroids = []
    pids_centroids_inds = list(result_dict.keys())

    pbar = tqdm(total=len(result_dict.keys()), desc=f'Calculating class centroid')
    # Calculate the centroid for each category separately
    for cls in result_dict.keys():
        cls_file = result_dict[cls]

        # Temporarily save the tensor data in a list
        cls_data = []
        for txt_file in cls_file:
            cls_data.append(np.array(load_txt_to_tensor(txt_file)))
        # Get the number of vector in cls_data
        data_length = len(cls_data)

        # Convert cls_data to a NumPy array of shape (n_samples, embedding_dimension)
        # n_samples is the number of vectors belonging to a certain category (usually it can be multiple).
        # embedding_dimension is the dimension of each vector.
        pids_vecs = np.array(cls_data)
        # calculate centroid
        centroid = np.sum(pids_vecs, 0) / data_length
        # save centroid data to centroids
        centroids.append(centroid)
        # update pbar
        pbar.update(1)
    pbar.close()
    '''
    用的论文中的原代码处理数据，这个处理数据的方式不一定适合（保存数据的格式)
    原文代码使用两个二维的array来保存数据，将所有类别的centroids转换为二维array。
    要结合原文代码的load embedding的data的function使用
    在可视化的时候注意数据类型
    '''
    # Use np.vstack to convert the list of centroids for all categories into a 2D array where each row is the centroid vector for a category.
    centroids_arr = np.vstack(np.array(centroids))
    # Convert the list of category identifiers pids_centroids_inds to a NumPy array and make the data type a string ( np.str_ ) for consistency.
    pids_centroids_inds = np.array(pids_centroids_inds, dtype=np.str_)

    return centroids_arr, pids_centroids_inds


# Save embedding data
def save_embedding_data(centroids_arr, cls_array, save_path):
    SAVE_DIR = Path(save_path)
    SAVE_DIR.mkdir(exist_ok=True, parents=True)

    print(f"Saving embeddings and index to {str(SAVE_DIR)}")
    np.save(SAVE_DIR / "embeddings.npy", centroids_arr)
    np.save(SAVE_DIR / "cls.npy", cls_array)





def create_embedding(target_folder, save_folder):
    file_list = get_all_file_path(target_folder)
    result_dict = get_cls_dict(file_list)
    centroids_arr, cls_array = embedding_process(result_dict)
    save_embedding_data(centroids_arr, cls_array, save_folder)

