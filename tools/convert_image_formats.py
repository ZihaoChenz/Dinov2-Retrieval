from PIL import Image
import os


def convert_images(input_folder, output_folder, target_format):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 获取文件的完整路径
        file_path = os.path.join(input_folder, filename)

        # 检查文件是否为图片格式（可以根据需要增加其他扩展名）
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff')):
            # 打开图片
            with Image.open(file_path) as img:
                # 定义新的文件名和路径
                base_name = os.path.splitext(filename)[0]
                new_filename = f"{base_name}.{target_format.lower()}"
                new_file_path = os.path.join(output_folder, new_filename)

                # 确保正确的格式名被使用
                save_format = target_format.upper()
                if save_format == 'JPG':
                    save_format = 'JPEG'

                # 保存图片为目标格式
                img.convert('RGB').save(new_file_path, save_format)
                print(f"已转换: {filename} -> {new_filename}")


if __name__ == '__main__':
    # 示例使用
    input_folder = r'D:\Github_Project\Downstream-Dinov2\data\building\ref'  # 输入图片文件夹路径
    output_folder = r'D:\Github_Project\Downstream-Dinov2\data\building\test'  # 输出图片文件夹路径
    target_format = 'jpg'  # 目标格式，例如 'jpg', 'png', 等

    convert_images(input_folder, output_folder, target_format)
