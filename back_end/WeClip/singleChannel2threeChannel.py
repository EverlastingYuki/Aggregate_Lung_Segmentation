from PIL import Image
import os
from tqdm import tqdm

# 指定包含单通道图像的目录
input_dir = r'I:\weclip\DataSet\VOCdevkit\VOC2012\JPEGImages'

# 确保输出目录存在
if not os.path.exists(input_dir):
    os.makedirs(input_dir)

# 获取所有单通道图像的列表
files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

# 使用tqdm创建进度条
for filename in tqdm(files, desc='Converting images'):
    # 打开图像
    img_path = os.path.join(input_dir, filename)
    img = Image.open(img_path)
    
    # 检查图像是否是单通道
    img = img.convert('RGB')
        
    # 覆盖保存图像
    img.save(img_path)
    print(f"Converted and saved: {img_path}")
        

print("Conversion complete.")