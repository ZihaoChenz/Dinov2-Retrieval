import os
import argparse
from tqdm import tqdm
from pathlib import Path
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description='parameter')
    # Batch evaluation of data
    parser.add_argument('--EvaluatedFolder', help='result txt folder path', required=False, type=str)
    args = parser.parse_args()
    return args



def get_info(eval_folder):
    total_dict = {}
    for txt_file in tqdm(os.listdir(eval_folder), desc="Loading similarity data"):
        result_dict = {}
        file_path = Path(os.path.join(eval_folder, txt_file)).as_posix()
        with open(file_path, "r") as file:
            current_key = None
            for line in file:
                line = line.strip()
                if line.startswith("Check file:"):
                    # 解析出Check file的文件名作为主键
                    current_key = line.split(": ")[1]
                    result_dict[current_key] = {}
                elif line and current_key:
                    # 将每张图片和数值作为当前主键的子字典
                    img_name, value = line.split(": ")
                    result_dict[current_key][img_name.strip()] = float(value.strip())
        total_dict[f"{txt_file}"] = result_dict
    return total_dict

def evaluate(eval_dict, top_similarity_num=3, adjacent_frame=4):
    correct_dict = {}

    top_similarity_frames = {}
    neighbors_dict = {}
    for check_file, values in eval_dict.items():
        check_frame_num = int(check_file.split('_')[-1].split('.')[0])

        # 计算每个frame的距离并存储
        frame_distances = []
        for file_name, similarity in values.items():
            frame_num = int(file_name.split('_')[-1].split('.')[0])
            distance = abs(frame_num - check_frame_num)
            frame_distances.append((frame_num, file_name, similarity, distance))

        # 按距离从小到大排序并取前4个
        neighbors = sorted(frame_distances, key=lambda x: x[3])[:adjacent_frame]

        # 将结果存入neighbors_dict
        neighbors_dict[check_file] = neighbors

        # 最相似的几个frames
        top_similarity_frames[check_file] = sorted(frame_distances, key=lambda x: x[2], reverse=True)[:top_similarity_num]

    for ck_file, dict in top_similarity_frames.items():
        for top_file in dict:
            if top_file in neighbors_dict[ck_file]:
                correct_dict[ck_file] = True
                break
            else:
                correct_dict[ck_file] = False


    count_true_values = sum(1 for value in correct_dict.values() if value)
    accuracy = count_true_values / len(eval_dict)
    return accuracy






if __name__ == '__main__':
    args = parse_args()
    eval_folder = args.EvaluatedFolder

    top_similarity_num = 3
    adjacent_frame = 4

    total_accuracy_dict = {}
    total_dict = get_info(eval_folder)
    for dataset, eval_dict in total_dict.items():
        accuracy = evaluate(eval_dict, top_similarity_num, adjacent_frame)
        total_accuracy_dict[dataset] = accuracy
    print("Each dataset accuracy: ", total_accuracy_dict)
    print("Average accuracy: ", sum(total_accuracy_dict.values()) / len(total_accuracy_dict))