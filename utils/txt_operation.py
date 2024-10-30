import os
import torch
import numpy as np
import chardet


def save_txt(filename, tensor_data, output_folder, process):
    """
    将tensor数据保存到txt文件中.

    参数:
    filename (str): 保存的文件名（包括路径和扩展名，例如 'data.txt'）。
    tensor_data (torch.Tensor): 要保存的tensor数据。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if process == 'inference':
        if not os.path.exists(os.path.join(output_folder,'check')):
            os.makedirs(os.path.join(output_folder,'check'))
        if not os.path.exists(os.path.join(output_folder,'ref')):
            os.makedirs(os.path.join(output_folder, 'ref'))

    # 确保传入的是tensor类型
    if not isinstance(tensor_data, torch.Tensor):
        raise ValueError("输入数据不是torch.Tensor类型")

    # 将tensor转换为numpy数组以便于保存
    numpy_data = tensor_data.cpu().numpy()

    # 保存到txt文件中
    with open(filename + ".txt", 'w') as f:
        for row in numpy_data:
            # 将每一行的数据转为字符串并用空格分隔，然后写入文件
            row_str = ' '.join(map(str, row))
            f.write(row_str + '\n')

    # print(f"数据已保存到 {os.path.join(filename)}")

def load_txt_to_tensor(filename):
    """
    自动检测编码格式并从txt文件中读取数据，将其转换为Tensor格式。

    参数:
    filename (str): 包含数据的txt文件名（包括路径）。

    返回:
    torch.Tensor: 转换后的Tensor数据。
    """
    with open(filename, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        # print(f"检测到的文件编码: {encoding}")

    # 从txt文件中读取数据
    with open(filename, 'r', encoding=encoding) as f:
        lines = f.readlines()

    # 解析读取的数据并转换为numpy数组
    data = []
    for line in lines:
        # 使用空格分隔符将每一行转换为浮点数
        row = list(map(float, line.strip().split()))
        data.append(row)

    # 将数据转换为numpy数组
    numpy_data = np.array(data)

    # 将numpy数组转换为PyTorch Tensor
    tensor_data = torch.from_numpy(numpy_data)

    return tensor_data

def generate_similarity_txt(save_path, total_dict):
    # 将数据写入txt文件
    with open(save_path, "w") as file:
        for key, value in total_dict.items():
            file.write("Check file: ")
            file.write(f"{key}:\n")
            for sub_key, sub_value in value.items():
                file.write(f"    {sub_key}: {sub_value}\n")
    print("Successfully save similarity")