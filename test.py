import os

import cv2

from back_end.predict.Unet import predict_Unet
# from back_end.predict.WeClip import predict_WeClip
from back_end.predict.deeplab import predict_deeplab
from PIL import Image

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# static目录
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')

# 上传目录
UPLOADED_DIR = os.path.join(STATIC_DIR, 'uploaded')
ORIGINAL_DIR = os.path.join(UPLOADED_DIR, 'original')
ONE_CHANNEL_DIR = os.path.join(UPLOADED_DIR, 'one_channel')
THREE_CHANNEL_DIR = os.path.join(UPLOADED_DIR, 'three_channel')

# 预测结果目录
RESULT_DIR = os.path.join(STATIC_DIR, 'result')
DEEPLAB_DIR = os.path.join(RESULT_DIR, 'deeplab')
UNET_DIR = os.path.join(RESULT_DIR, 'Unet')
WECIP_DIR = os.path.join(RESULT_DIR, 'WeClip')

def process_images():
    for filename in os.listdir(ORIGINAL_DIR):
            original_img_path = os.path.join(ORIGINAL_DIR, filename)
            one_channel_path = os.path.join(ONE_CHANNEL_DIR, filename)
            three_channel_path = os.path.join(THREE_CHANNEL_DIR, filename)

            try:
                image = Image.open(original_img_path)
                if len(image.split()) == 1:
                    print(f"{filename} 为单通道图片，保存三通道副本到 three_channel")
                    image.save(one_channel_path)
                    img_gray = cv2.imread(original_img_path, cv2.IMREAD_GRAYSCALE)
                    img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
                    cv2.imwrite(three_channel_path, img_rgb)
                else:
                    print(f"{filename} 为三通道图片，保存单通道副本到 one_channel")
                    image.save(three_channel_path)
                    img = cv2.imread(original_img_path, cv2.IMREAD_GRAYSCALE)  # 读取灰度图
                    cv2.imwrite(one_channel_path, img)
            except Exception as e:
                print(f"处理 {filename} 时发生错误: {e}")

process_images()
# predict_deeplab(PROJECT_ROOT, ONE_CHANNEL_DIR, THREE_CHANNEL_DIR, DEEPLAB_DIR)
predict_Unet(project_root= PROJECT_ROOT, one_channel_dir= ONE_CHANNEL_DIR, three_channel_dir= THREE_CHANNEL_DIR, Unet_dir=UNET_DIR)
# predict_WeClip(PROJECT_ROOT, ONE_CHANNEL_DIR, THREE_CHANNEL_DIR, WECIP_DIR)