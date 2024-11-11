import os
from PIL import Image

def replace_color_and_save(input_tif_path, output_png_path):
    # 打开TIF图片
    image = Image.open(input_tif_path)
    
    # 将图片转换为RGB模式，以防它是其他模式
    image = image.convert('RGB')
    
    # 加载图片数据
    pixels = image.load()
    
    # 获取图片的尺寸
    width, height = image.size
    
    # 遍历图片中的每个像素
    for x in range(width):
        for y in range(height):
            # 如果像素颜色为白色，则更改为指定的颜色
            if pixels[x, y] == (255, 255, 255):
                pixels[x, y] = (2, 2, 2)
    pixels[0, 0] = (255,255,255)
    
    # 将图片另存为PNG格式
    image.save(output_png_path, 'PNG')

def process_directory(input_directory, output_directory):
    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.tif', '.tiff')):
            input_path = os.path.join(input_directory, filename)
            # 为输出文件定义一个文件名，保持原始文件名但更改扩展名为.png
            output_filename = os.path.splitext(filename)[0] + '.png'
            output_path = os.path.join(output_directory, output_filename)
            
            # 调用替换颜色并保存的函数
            replace_color_and_save(input_path, output_path)
            print(f"Processed and saved: {output_path}")

# 使用方法
input_directory = r'C:\Users\q\Downloads\2d_masks'
output_directory = r'C:\Users\q\Downloads\out_2d_masks'
process_directory(input_directory, output_directory)