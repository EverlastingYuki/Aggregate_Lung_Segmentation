import os
from PIL import Image

def convert_png_to_jpg(directory):
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(".png"):
            # 构建完整的文件路径
            file_path = os.path.join(directory, filename)
            # 打开图像文件
            with Image.open(file_path) as img:
                # 构建新的文件名，替换扩展名为.jpg
                new_filename = os.path.splitext(filename)[0] + '.jpg'
                new_file_path = os.path.join(directory, new_filename)
                # 转换图像并保存为JPG格式
                img.convert('RGB').save(new_file_path, 'JPEG')
                print(f"Converted {filename} to {new_filename}")

# 指定需要转换的目录
directory_path = r'I:\weclip\DataSet\VOCdevkit\VOC2012\JPEGImages'
convert_png_to_jpg(directory_path)