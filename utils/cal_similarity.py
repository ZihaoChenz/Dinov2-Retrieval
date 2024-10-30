import os
import torch
import torch.nn.functional as F
from pathlib import Path
from tqdm import tqdm
from utils.txt_operation import load_txt_to_tensor
from utils.load_data import load_centroids_data


def compute_similarity(feature1, feature2, method='cosine'):
    """
    计算两个图片特征之间的相似性。

    参数:
    feature1 (torch.Tensor): 第一张图片的特征向量。
    feature2 (torch.Tensor): 第二张图片的特征向量。
    method (str): 计算相似度的方法。可选 'cosine' 或 'euclidean'。默认是 'cosine'。

    返回:
    float: 两个特征之间的相似性值。
    """
    if method == 'cosine':
        # 使用PyTorch的余弦相似度计算
        similarity = F.cosine_similarity(feature1, feature2, dim=1)
        return similarity.item()

    elif method == 'euclidean':
        # 计算欧氏距离
        distance = torch.dist(feature1, feature2, p=2)  # p=2 代表欧氏距离
        return distance.item()

    else:
        raise ValueError("不支持的计算方法。请使用 'cosine' 或 'euclidean'")

def compare_similarity(image_type, result_folder):
    # get check and ref path
    check_path = os.path.join(result_folder, 'check')
    ref_path = os.path.join(result_folder, 'ref')
    # list all txt name
    check_txt = os.listdir(check_path)
    ref_txt = os.listdir(ref_path)
    total_top3_dict = {}
    total_dict = {}
    # for each check_txt, cal the similarity with all ref_txt
    for c_txt in check_txt:
        # save similarity between c_txt and all ref_txt
        similarity_dict = {}
        for r_txt in tqdm(ref_txt, desc=f'Calculating {c_txt} similarity'):
            feature_c = load_txt_to_tensor(os.path.join(check_path, c_txt))
            feature_r = load_txt_to_tensor(os.path.join(ref_path, r_txt))
            # compute similarity
            similarity_dict[os.path.splitext(r_txt)[0] + '.' + image_type] = compute_similarity(feature_c, feature_r)
            total_dict[os.path.splitext(c_txt)[0] + '.' + image_type] = similarity_dict
        # get top three similarity ref_txt
        top_three = dict(sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)[:3])
        total_top3_dict[os.path.splitext(c_txt)[0] + '.' + image_type] = top_three

    return total_top3_dict, total_dict


# Classify the class that all input file belong through compare input file feature and each class centroid
def classify_centroids_cls(input_folder, centroids_data_dit):
    check_path = os.path.join(input_folder)
    check_txt = os.listdir(check_path)

    file_cls_dict = {}

    # compare each input file
    for c_txt in tqdm(check_txt, desc="classify all check file"):
        check_full_path = Path(os.path.join(check_path, c_txt)).as_posix()
        # get the input txt feature
        feature_c = load_txt_to_tensor(check_full_path)
        # Create a dict to record each class similarity value
        cls_similarity_dict = {}

        for cls in centroids_data_dit:
            # Compute similarity of all class
            cls_similarity_dict[cls] = compute_similarity(centroids_data_dit[cls], feature_c)
        # Get the max similarity class
        max_similarity_cls = max(cls_similarity_dict, key=cls_similarity_dict.get)
        file_cls_dict[check_full_path] = {"class": max_similarity_cls, "class_similarity": cls_similarity_dict[max_similarity_cls], "check_feature": feature_c}

    return file_cls_dict

def compare_centroid_similarity(image_type, base_folder, file_cls_dict):
    total_top3_dict = {}
    total_dict = {}
    # Calculate each check file
    for file in file_cls_dict:
        similarity_dict = {}
        # Get reference folder path
        cls_ref_folder = os.path.join(base_folder, file_cls_dict[file]["class"])
        ref_check_folder = os.path.join(cls_ref_folder, "ref")
        ref_txt = os.listdir(ref_check_folder)

        # Compute similarity in reference folder
        for r_txt in tqdm(ref_txt, desc=f'Calculating {file} similarity'):
            # Get feature of reference file and check file
            feature_c = file_cls_dict[file]["check_feature"]
            feature_r = load_txt_to_tensor(os.path.join(ref_check_folder, r_txt))

            # Refactor the ref check path
            ref_refactor_path = Path(ref_check_folder)
            # Get the path of the image file corresponding to the txt file
            txt2image_path = Path(str(os.path.join(ref_refactor_path, os.path.splitext(r_txt)[0] + '.' + image_type)).replace('output', 'data')).as_posix()
            # save the image path and it's similarity
            similarity_dict[txt2image_path] = compute_similarity(feature_c, feature_r)

        # Get top three similarity reference image
        top_three = dict(sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)[:3])
        # Save the check images, and it's corresponding top three similarity ref images
        total_top3_dict[Path(str((os.path.splitext(file)[0] + '.' + image_type).replace('output', 'data'))).as_posix()] = top_three

    return total_top3_dict



# for testing
if __name__ == '__main__':
    # feature_1 = load_txt_to_tensor('D:\\Github_Project\\Downstream-Dinov2\\output\\check\\IMG_4287.txt')
    # feature_2 = load_txt_to_tensor('D:\\Github_Project\\Downstream-Dinov2\\output\\check\\IMG_4288.txt')
    # print(feature_1)
    # print(feature_2)
    # similarity = compute_similarity(feature_1, feature_2, method='cosine')
    # print("similarity: ", similarity)
    centroid_cls_dict = load_centroids_data(r"D:\Github-my\Dinov2\Dinov2_Matching\embedding\surrounding", normalize=False)
    file_cls_dict = classify_centroids_cls(r"D:\Github-my\Dinov2\Dinov2_Matching\output\surrounding\Shek-Tong-Tsui\check", centroid_cls_dict)
