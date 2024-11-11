import cv2
import numpy as np

import cv2
import numpy as np

import cv2
import numpy as np

import cv2
import numpy as np

def smooth_edge1(img_path, kernel_size=3, alpha=128):
    """
    平滑mask边缘并生成带有透明度的图像。

    参数：
    - img_path: 输入的mask图路径。
    - kernel_size: 形态学操作的核大小。
    - alpha: 半透明像素的透明度值（0-255）。
    """
    # 读取二值化的mask图
    mask = cv2.imread(img_path, 0)

    # 定义结构元素，形态学操作的核大小
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # 开操作：去除小噪声点
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 闭操作：填充小孔洞，平滑边缘
    mask_smoothed = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

    # 创建与原图像相同大小的结果图像（RGBA格式），初始颜色为(254, 220, 156) + 透明度
    result_image = np.full((*mask_smoothed.shape, 4), (254, 220, 156, alpha), dtype=np.uint8)

    # 创建黑色像素的掩码
    black_mask = mask_smoothed == 0

    # 将黑色像素设为完全透明
    result_image[black_mask] = (0, 0, 0, 0)  # 黑色区域变为完全透明

    # 将白色像素设为预设颜色并应用不透明度
    white_mask = mask_smoothed == 255
    result_image[white_mask] = (254, 220, 156, alpha)  # 白色区域设为指定透明度的颜色

    # 保存结果为PNG文件，支持透明度
    cv2.imwrite('mask_cleaned_transparent.png', result_image)

# 调用示例
# smooth_edge1('mask.png', kernel_size=3, alpha=128)  # 设置半透明度为128



def smooth_edge2(img_path, window_size=5):

    mask = cv2.imread(img_path, 0)
    # 中值滤波
    mask_smoothed = cv2.medianBlur(mask, window_size)  # 5x5的滤波窗口

    cv2.imwrite('mask_median_filtered.png', mask_smoothed)

def smooth_edge3(img_path, min_size=100):
    # 读取二值化的mask图
    mask = cv2.imread(img_path, 0)

    # 寻找连通域
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    # 过滤小区域，阈值可以根据实际情况调整
    #   # 最小区域大小
    new_mask = np.zeros(mask.shape, dtype=np.uint8)

    for i in range(1, num_labels):  # 从1开始，因为0是背景
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            new_mask[labels == i] = 255  # 保留大于阈值的区域

    cv2.imwrite('mask_filtered.png', new_mask)

smooth_edge1("./ID_0188_Z_0137.png")