import tkinter as tk
from PIL import Image, ImageTk
import os



# 初始化UI
class ImageDisplay():
    def __init__(self, root, data, data_folder, centroid):
        self.data = data
        self.root = root
        self.index = centroid
        if self.index == False:
            self.base_check_path = os.path.join(data_folder, 'check')
            self.base_ref_path = os.path.join(data_folder, 'ref')
        self.root.title("Image Display")
        self.current_index = 0  # 用于跟踪当前展示的key
        self.keys = list(self.data.keys())

        # 创建显示主图像名称的Label
        self.main_image_name_label = tk.Label(root, font=("Arial", 16))
        self.main_image_name_label.pack()

        # 创建显示主图像的Label
        self.main_image_label = tk.Label(root)
        self.main_image_label.pack()

        # 创建较小图像和数值显示的框架
        self.small_image_frames = [tk.Frame(root) for _ in range(3)]
        self.small_image_name_labels = []
        self.small_image_labels = []
        self.value_labels = []

        for frame in self.small_image_frames:
            frame.pack(side=tk.LEFT, padx=10)

            # 图片名Label
            image_name_label = tk.Label(frame)
            image_name_label.pack()
            self.small_image_name_labels.append(image_name_label)

            # 较小的图片Label
            small_image_label = tk.Label(frame)
            small_image_label.pack()
            self.small_image_labels.append(small_image_label)

            # 数值Label
            value_label = tk.Label(frame)
            value_label.pack()
            self.value_labels.append(value_label)

        # 创建"下一张"按钮
        self.next_button = tk.Button(root, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.RIGHT)

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT)

        # 显示第一张图像
        self.show_image()

    def show_image(self):
        if self.index == False:
            # 获取当前主图像的路径
            main_image_filename = self.keys[self.current_index]
            main_image_path = os.path.join(self.base_check_path, main_image_filename)

        else:
            # 获取当前主图像的路径
            main_image_path = self.keys[self.current_index]
            # 分割路径
            path_parts = main_image_path.split('/')
            # 获取倒数第一层路径
            main_image_filename = path_parts[-1]

        # 显示主图像名称
        self.main_image_name_label.config(text=main_image_filename)

        # 显示主图像
        main_image = Image.open(main_image_path)
        main_image = main_image.resize((300, 300), Image.LANCZOS)
        main_image_tk = ImageTk.PhotoImage(main_image)
        self.main_image_label.config(image=main_image_tk)
        self.main_image_label.image = main_image_tk  # 防止垃圾回收

        if self.index == False:
            # 获取当前key的value
            value_dict = self.data[main_image_filename]
        else:
            value_dict = self.data[main_image_path]
        value_keys = list(value_dict.keys())

        # 显示三张较小图像、对应的数值和图片名
        for i in range(3):
            if self.index == False:
                small_image_filename = value_keys[i]
                small_image_path = os.path.join(self.base_ref_path, small_image_filename)

            else:
                small_image_path = value_keys[i]
                path_parts = small_image_path.split('/')
                small_image_filename = path_parts[-1]
            # 显示图片名
            self.small_image_name_labels[i].config(text=small_image_filename)



            # 显示较小图像
            small_image = Image.open(small_image_path)
            small_image = small_image.resize((200, 200), Image.LANCZOS)
            small_image_tk = ImageTk.PhotoImage(small_image)
            self.small_image_labels[i].config(image=small_image_tk)
            self.small_image_labels[i].image = small_image_tk

            if self.index == False:
                # 显示数值
                self.value_labels[i].config(text=f"{value_dict[small_image_filename]:.4f}")
            else:
                # 显示数值
                self.value_labels[i].config(text=f"{value_dict[small_image_path]:.4f}")

    def next_image(self):
        # 切换到下一张图片
        self.current_index = (self.current_index + 1) % len(self.keys)
        self.show_image()

    def prev_image(self):
        self.current_index = (self.current_index - 1) % len(self.keys)
        self.show_image()


# for testing
# if __name__ == "__main__":
#     # 数据 dictionary
#     data = {
#         'IMG_4287.JPG': {'IMG_4287_bg2.JPG': 0.8959329106295477, 'IMG_4287_bg1.JPG': 0.6955251740003494,
#                          'IMG_4335.JPG': 0.5684624571106598},
#         'IMG_4288.JPG': {'IMG_4287_bg2.JPG': 0.8720613035570646, 'IMG_4287_bg1.JPG': 0.6943158106847359,
#                          'IMG_4335.JPG': 0.6466266633474884},
#         'IMG_4291.JPG': {'IMG_4287_bg2.JPG': 0.735184318812665, 'IMG_4335.JPG': 0.7129120551084809,
#                          'IMG_4287_bg1.JPG': 0.707857540883853},
#         'IMG_4299.JPG': {'IMG_4287_bg2.JPG': 0.7090594189068824, 'IMG_4287_bg1.JPG': 0.6688264696750842,
#                          'IMG_4335.JPG': 0.6280110958045602}
#     }
#     root = tk.Tk()
#     app = ImageDisplay(root, data)
#     root.mainloop()


