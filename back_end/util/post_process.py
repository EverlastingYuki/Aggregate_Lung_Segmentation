import os
import shutil
import cv2
import numpy as np
from back_end.util import *
from PIL import Image


def deeplab_postprocess():
    for filename in os.listdir(DEEPLAB_DIR):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            file_path = os.path.join(DEEPLAB_DIR, filename)
            img = cv2.imread(file_path)
            blue_mask = (img[:, :, 0] > 150) & (img[:, :, 1] < 50) & (img[:, :, 2] < 50)
            img[~blue_mask] = [0, 0, 0]
            cv2.imwrite(file_path, img)

    print("deeplab结果处理完成")


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
    # add_weighted_overlay_images(folder1, folder2, output_folder, alpha)
    # add_overlay_images(folder1, folder2, output_folder)
    overlay2(folder1, folder2, output_folder, alpha)


def add_weighted_overlay_images(folder1, folder2, output_folder, alpha=0.5):
    """
    将一个文件夹中的图像叠加到另一个文件夹中的同名图像上。

    :param folder1: 第一个文件夹路径，包含要叠加的图像
    :param folder2: 第二个文件夹路径，包含基础图像
    :param output_folder: 输出文件夹路径，保存叠加后的图像
    :param alpha: 第一张图像的透明度（0.0-1.0）
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
            print(f"文件 {file} 的尺寸不匹配，调整尺寸。")
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        # 确保图像通道数相同
        if image1.shape[2] != image2.shape[2]:
            print(f"文件 {file} 的通道数不匹配，转换通道数。")
            if image1.shape[2] == 4:
                image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2BGRA)
            else:
                image1 = cv2.cvtColor(image1, cv2.COLOR_BGRA2BGR)

        # 叠加图像
        overlaid_image = cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)

        # 保存叠加后的图像
        cv2.imwrite(output_path, overlaid_image)


def add_overlay_images(folder1, folder2, output_folder, alpha=0.5):
    """
    将一个文件夹中的图像叠加到另一个文件夹中的同名图像上。

    :param folder1: 第一个文件夹路径，包含要叠加的图像
    :param folder2: 第二个文件夹路径，包含基础图像
    :param output_folder: 输出文件夹路径，保存叠加后的图像
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
        if not os.path.isfile(path1):
            print(f"文件 {file} 在{path1}中不存在，跳过。")
            continue
        if not os.path.isfile(path2):
            print(f"文件 {file} 在{path2}中不存在，跳过。")
            continue

        # 读取图像
        image1 = cv2.imread(path1, cv2.IMREAD_UNCHANGED)
        image2 = cv2.imread(path2, cv2.IMREAD_UNCHANGED)

        # 确保图像大小相同
        if image1.shape[:2] != image2.shape[:2]:
            print(f"文件 {file} 的尺寸不匹配，调整尺寸。")
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        # 确保图像通道数相同
        if image1.shape[2] != image2.shape[2]:
            print(f"文件 {file} 的通道数不匹配，转换通道数。")
            if image1.shape[2] == 4:
                image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2BGRA)
            else:
                image1 = cv2.cvtColor(image1, cv2.COLOR_BGRA2BGR)

        overlaid_image = cv2.add(image1, image2)
        cv2.imwrite(output_path, overlaid_image)


def overlay2(folder1, folder2, output_folder, alpha=0.5):
    """
    将folder1中的图片以alpha透明度叠加到folder2中的图片上，并保存到output_folder中。

    :param folder1: 包含要叠加的图片的文件夹路径
    :param folder2: 包含底图的文件夹路径
    :param output_folder: 输出结果的文件夹路径
    :param alpha: 图片1的透明度，范围从0.0到1.0
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取两个文件夹中的图片文件列表
    images1 = sorted([f for f in os.listdir(folder1) if f.endswith(('.png', '.jpg', '.jpeg'))])
    images2 = sorted([f for f in os.listdir(folder2) if f.endswith(('.png', '.jpg', '.jpeg'))])

    # 检查两个文件夹中的图片数量是否相同
    if len(images1) != len(images2):
        print(folder1 + "与" + folder2 + "两个文件夹中的图片数量不匹配，跳过")
        return 1

    # 遍历图片并进行叠加
    for img1, img2 in zip(images1, images2):
        # 打开图片
        image1 = Image.open(os.path.join(folder1, img1)).convert("RGBA")
        image2 = Image.open(os.path.join(folder2, img2)).convert("RGBA")

        # 调整image1的透明度
        image1 = image1.convert("RGBA")
        image1.putalpha(int(255 * alpha))

        # 叠加图片
        result = Image.alpha_composite(image2, image1)

        # 保存结果
        result.save(os.path.join(output_folder, img1))


def process_image(three_channel_dir, alpha=0.5):
    for i in [DEEPLAB_DIR, UNET_DIR, WECLIP_DIR]:
        if os.path.exists(i):
            for image in os.listdir(i):
                path = os.path.join(i, image)
                post_process_image(input_path=path, output_path=path)
    if os.path.exists(OVERLAY_DIR):
        shutil.rmtree(OVERLAY_DIR)
    os.makedirs(OVERLAY_DIR)
    os.makedirs(os.path.join(OVERLAY_DIR, 'original'), exist_ok=True)
    for image in os.listdir(three_channel_dir):
        src_path = os.path.join(three_channel_dir, image)
        dst_path = os.path.join(OVERLAY_DIR, 'original', image)
        shutil.copy2(src_path, dst_path)

    # 一个模型叠加
    os.makedirs(os.path.join(OVERLAY_DIR, 'deeplab'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'Unet'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'WeClip'), exist_ok=True)

    overlay_images(DEEPLAB_DIR, three_channel_dir, os.path.join(OVERLAY_DIR, 'deeplab'), alpha)
    overlay_images(UNET_DIR, three_channel_dir, os.path.join(OVERLAY_DIR, 'Unet'), alpha)
    overlay_images(WECLIP_DIR, three_channel_dir, os.path.join(OVERLAY_DIR, 'WeClip'), alpha)

    # 两个模型叠加
    os.makedirs(os.path.join(OVERLAY_DIR, 'deeplab_Unet'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'deeplab_WeClip'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'Unet_WeClip'), exist_ok=True)
    os.makedirs(os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'), exist_ok=True)

    add_overlay_images(DEEPLAB_DIR, UNET_DIR, os.path.join(OVERLAY_DIR, 'deeplab_Unet'), alpha)
    add_overlay_images(DEEPLAB_DIR, UNET_DIR, os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'), alpha)
    overlay_images(os.path.join(OVERLAY_DIR, 'deeplab_Unet'), three_channel_dir,
                   os.path.join(OVERLAY_DIR, 'deeplab_Unet'), alpha)
    add_overlay_images(DEEPLAB_DIR, WECLIP_DIR, os.path.join(OVERLAY_DIR, 'deeplab_WeClip'), alpha)
    overlay_images(os.path.join(OVERLAY_DIR, 'deeplab_WeClip'), three_channel_dir,
                   os.path.join(OVERLAY_DIR, 'deeplab_WeClip'), alpha)
    add_overlay_images(UNET_DIR, WECLIP_DIR, os.path.join(OVERLAY_DIR, 'Unet_WeClip'), alpha)
    overlay_images(os.path.join(OVERLAY_DIR, 'Unet_WeClip'), three_channel_dir,
                   os.path.join(OVERLAY_DIR, 'Unet_WeClip'), alpha)

    # 三个模型叠加
    if os.listdir(WECLIP_DIR):
        add_overlay_images(os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'), WECLIP_DIR,
                           os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'), alpha)
        overlay_images(os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'), three_channel_dir,
                       os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'), alpha)
    else:
        shutil.rmtree(os.path.join(OVERLAY_DIR, 'deeplab_Unet_WeClip'))
