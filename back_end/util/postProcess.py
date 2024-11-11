import os
import shutil

import cv2
import numpy as np
from back_end.util import *

def post_process_image(input_path, output_path, alpha=255):
    """
    后处理函数，使图像中黑色部分变为纯透明，黑色以外的部分变为半透明。

    :param input_path: 输入图像路径
    :param output_path: 输出图像路径
    :param alpha: 黑色以外部分的透明度（0-255）
    """
    # 读取图像
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)

    # 获取图像的形状
    height, width, _ = image.shape

    # 创建透明通道
    alpha_channel = np.zeros((height, width), dtype=np.uint8)

    # 设置黑色部分为纯透明，其他部分为半透明
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    alpha_channel[gray_image == 0] = 0  # 黑色部分透明
    alpha_channel[gray_image != 0] = alpha  # 其他部分半透明

    # 合并为四通道图像
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_rgba[:, :, 3] = alpha_channel

    # 保存图像
    cv2.imwrite(output_path, image_rgba)


def overlay_images(folder1, folder2, output_folder, alpha=0.5):
    """
    将一个文件夹中的图像叠加到另一个文件夹中的同名图像上。

    :param folder1: 第一个文件夹路径，包含要叠加的图像
    :param folder2: 第二个文件夹路径，包含基础图像
    :param output_folder: 输出文件夹路径，保存叠加后的图像
    :param alpha: 叠加图像的透明度（0.0-1.0）
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取第一个文件夹中的所有文件名
    files = os.listdir(folder1)

    for file in files:
        # 构建完整的文件路径
        path1 = os.path.join(folder1, file)
        path2 = os.path.join(folder2, file)
        output_path = os.path.join(output_folder, file)

        # 检查文件是否存在
        if not os.path.isfile(path1) or not os.path.isfile(path2):
            print(f"文件 {file} 在其中一个文件夹中不存在，跳过。")
            continue

        # 读取图像
        image1 = cv2.imread(path1, cv2.IMREAD_UNCHANGED)
        image2 = cv2.imread(path2, cv2.IMREAD_UNCHANGED)

        # 确保图像大小相同
        if image1.shape[:2] != image2.shape[:2]:
            print(f"文件 {file} 的尺寸不匹配，跳过。")
            continue

        # 叠加图像
        overlaid_image = cv2.addWeighted(image1, alpha, image2, 1, 0)

        # 保存叠加后的图像
        cv2.imwrite(output_path, overlaid_image)


OVERLAY_DIR = config['overlay_dir']


def process_image(alpha=0.5):
    for i in [DEEPLAB_DIR, UNET_DIR, WECLIP_DIR]:
        for image in os.listdir(i):
            path = os.path.join(i, image)
            post_process_image(input_path=path, output_path=path)
    if os.path.exists(OVERLAY_DIR):
        shutil.rmtree(OVERLAY_DIR)
    os.makedirs(OVERLAY_DIR)
    os.makedirs(os.path.join(OVERLAY_DIR, 'original'), exist_ok=True)
    for image in os.listdir(ORIGINAL_DIR):
        src_path = os.path.join(ORIGINAL_DIR, image)
        dst_path = os.path.join(OVERLAY_DIR, 'original', image)
        shutil.copy2(src_path, dst_path)

    # 一个模型叠加
    os.makedirs(os.path.join(OVERLAY_DIR, 'deeplab'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'Unet'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'WeClip'), exist_ok=True)

    overlay_images(DEEPLAB_DIR, ORIGINAL_DIR, os.path.join(OVERLAY_DIR, 'deeplab'), alpha)
    overlay_images(UNET_DIR, ORIGINAL_DIR, os.path.join(OVERLAY_DIR, 'Unet'), alpha)
    overlay_images(WECLIP_DIR, ORIGINAL_DIR, os.path.join(OVERLAY_DIR, 'WeClip'), alpha)

    # 两个模型叠加
    os.makedirs(os.path.join(OVERLAY_DIR, 'deeplab_Unet'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'deeplab_WeClip'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'Unet_WeClip'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'), exist_ok=True)

    overlay_images(DEEPLAB_DIR, UNET_DIR, os.path.join(OVERLAY_DIR, 'deeplab_Unet'), alpha)
    overlay_images(DEEPLAB_DIR, WECLIP_DIR, os.path.join(OVERLAY_DIR, 'deeplab_WeClip'), alpha)
    overlay_images(UNET_DIR, WECLIP_DIR, os.path.join(OVERLAY_DIR, 'Unet_WeClip'), alpha)

    # 三个模型叠加
    overlay_images(os.path.join(OVERLAY_DIR, 'deeplab_Unet'), WECLIP_DIR, os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'), alpha)
