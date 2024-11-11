import numpy as np
import os
import torch
import torch.nn.functional as F
import imageio.v2 as imageio
from utils.imutils import encode_cmap
import matplotlib.pyplot as plt

def visualize_npy(npy_dir, output_dir, img_dir, cmap_output_dir, image_format="png"):
    """
    可视化保存的 .npy 文件并生成对应的图片

    :param npy_dir: 保存 .npy 文件的路径
    :param output_dir: 保存输出可视化图片的路径
    :param img_dir: 原始图片文件夹的路径
    :param cmap_output_dir: 保存经过cmap编码的图片
    :param image_format: 输出图片格式, 默认 "png"
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(cmap_output_dir):
        os.makedirs(cmap_output_dir)

    # 获取npy文件列表
    npy_files = [f for f in os.listdir(npy_dir) if f.endswith('.npy')]

    for npy_file in npy_files:
        # 加载npy文件
        npy_path = os.path.join(npy_dir, npy_file)
        data = np.load(npy_path, allow_pickle=True).item()
        segs = data['segs']
        msc_segs = data['msc_segs']

        # 获取图片名
        image_name = npy_file.replace('.npy', '.jpg')
        img_path = os.path.join(img_dir, image_name)

        # 加载原始图片
        image = imageio.imread(img_path).astype(np.uint8)

        # 可视化segmentation的结果
        seg_pred = np.argmax(segs, axis=1)[0]
        msc_seg_pred = np.argmax(msc_segs, axis=1)[0]

        # 可视化原始图片和segmentation结果的叠加
        visualize_predictions(image, seg_pred, msc_seg_pred, image_name, output_dir, cmap_output_dir, image_format)

def visualize_predictions(image, seg_pred, msc_seg_pred, image_name, output_dir, cmap_output_dir, image_format):
    """
    显示并保存原始图片与分割结果

    :param image: 原始图片
    :param seg_pred: 分割预测结果
    :param msc_seg_pred: msc 分割预测结果
    :param image_name: 图片名
    :param output_dir: 保存输出路径
    :param cmap_output_dir: 保存 cmap 编码图片的路径
    :param image_format: 输出图片格式
    """
    # 保存原始分割结果
    seg_path = os.path.join(output_dir, image_name.replace('.jpg', f'_seg.{image_format}'))
    msc_seg_path = os.path.join(output_dir, image_name.replace('.jpg', f'_msc_seg.{image_format}'))

    imageio.imsave(seg_path, seg_pred.astype(np.uint8))
    imageio.imsave(msc_seg_path, msc_seg_pred.astype(np.uint8))

    # 保存经过 cmap 编码的图片
    cmap_seg_pred = encode_cmap(seg_pred)
    cmap_msc_seg_pred = encode_cmap(msc_seg_pred)

    cmap_seg_path = os.path.join(cmap_output_dir, image_name.replace('.jpg', f'_seg_cmap.{image_format}'))
    cmap_msc_seg_path = os.path.join(cmap_output_dir, image_name.replace('.jpg', f'_msc_seg_cmap.{image_format}'))

    imageio.imsave(cmap_seg_path, cmap_seg_pred)
    imageio.imsave(cmap_msc_seg_path, cmap_msc_seg_pred)

    # 可视化叠加的分割图像
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    axes[0].imshow(image)
    axes[0].set_title('Original Image')

    axes[1].imshow(seg_pred, cmap='jet')
    axes[1].set_title('Segmentation')

    axes[2].imshow(msc_seg_pred, cmap='jet')
    axes[2].set_title('MSC Segmentation')

    for ax in axes:
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, image_name.replace('.jpg', f'_visualization.{image_format}')))
    plt.close()


if __name__ == "__main__":
    npy_dir = r"I:\weclip\WeCLIP\results\val\temp_npy"  # 存放npy文件的目录
    output_dir = "./re/visualization"  # 存放生成的分割结果图片
    img_dir = r"I:\weclip\DataSet\VOCdevkit\VOC2012\JPEGImages"  # 原始图片目录
    cmap_output_dir = "./re/visualization_cmap"  # 存放经过cmap编码的图片

    visualize_npy(npy_dir, output_dir, img_dir, cmap_output_dir)
