import os
from PIL import Image, ImageOps

def convert_tif_to_png(directory):
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(".tif") or filename.lower().endswith(".tiff"):
            # 构建完整的文件路径
            file_path = os.path.join(directory, filename)
            # 打开图像文件
            with Image.open(file_path) as img:
                # 如果图像模式是'I'，转换为'RGB'
                if img.mode == 'I':
                    img = img.convert('RGB')
                # 反转图像颜色
                inverted_img = ImageOps.invert(img)
                # 构建新的文件名，替换扩展名为.png
                new_filename = os.path.splitext(filename)[0] + '.png'
                new_file_path = os.path.join(directory, new_filename)
                # 转换图像并保存为PNG格式
                inverted_img.save(new_file_path, 'PNG')
                print(f"Converted {filename} to {new_filename}")

# 指定需要转换的目录
directory_path = r'C:\Users\q\Downloads\2d_images'
convert_tif_to_png(directory_path)