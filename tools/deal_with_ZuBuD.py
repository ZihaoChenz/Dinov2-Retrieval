import os
import shutil
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='parameter')
    parser.add_argument('--src_folder', help="dataset folder", required=True, type=str)
    parser.add_argument('--dst_folder', help="Output folder", required=True, type=str, default="../data/ZuBuD")
    args = parser.parse_args()
    return args



def organize_images(src_folder, dst_folder):
    # 获取源文件夹中的所有文件
    for filename in os.listdir(src_folder):
        # 只处理文件名以object开头且后缀为图片格式的文件
        if filename.startswith('object') and (filename.endswith('.jpg') or filename.endswith('.png')):
            # 提取文件名前缀(如 'object0001')作为文件夹名称
            folder_name = filename.split('.')[0]  # 提取 'object0001' 部分

            # 创建目标文件夹路径
            target_folder = os.path.join(dst_folder, folder_name)

            # 如果目标文件夹不存在，则创建它
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # 构建文件的源路径和目标路径
            src_file = os.path.join(src_folder, filename)
            dst_file = os.path.join(target_folder, filename)

            # 将文件复制到目标文件夹
            shutil.copy(src_file, dst_file)
            print(f"Copied {filename} to {target_folder}")


def organize_check_and_ref(src_folder):
    # 获取源文件夹中的所有objectXXXX文件夹
    for object_folder in os.listdir(src_folder):
        object_folder_path = os.path.join(src_folder, object_folder)

        # 确认这是一个文件夹
        if os.path.isdir(object_folder_path):
            # 获取该文件夹中的所有文件，按文件名排序
            files = sorted(os.listdir(object_folder_path))

            # 确保文件夹内至少有3个文件
            if len(files) >= 3:
                # 创建check和ref文件夹
                check_folder = os.path.join(object_folder_path, 'check')
                ref_folder = os.path.join(object_folder_path, 'ref')

                if not os.path.exists(check_folder):
                    os.makedirs(check_folder)
                if not os.path.exists(ref_folder):
                    os.makedirs(ref_folder)

                # 将第三张图片移动到check文件夹
                third_image = files[2]  # 第三张图片索引为2（0-based）
                third_image_src = os.path.join(object_folder_path, third_image)
                third_image_dst = os.path.join(check_folder, third_image)
                shutil.move(third_image_src, third_image_dst)
                print(f"Moved {third_image} to {check_folder}")

                # 将其他图片（除第三张）移动到ref文件夹
                for i, file in enumerate(files):
                    if i != 2:  # 跳过第三张图片
                        src_file = os.path.join(object_folder_path, file)
                        dst_file = os.path.join(ref_folder, file)
                        shutil.move(src_file, dst_file)
                        print(f"Moved {file} to {ref_folder}")


if __name__ == '__main__':
    # 使用示例，指定图片所在的源文件夹和目标文件夹
    args = parse_args()
    src_folder = args.src_folder
    dst_folder = args.dst_folder
    organize_images(src_folder, dst_folder)
    organize_check_and_ref(dst_folder)
