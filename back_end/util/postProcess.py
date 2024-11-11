import cv2
import numpy as np


def post_process_image(input_path, output_path, alpha=128):
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
