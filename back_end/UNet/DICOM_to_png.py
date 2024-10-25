import os

import pydicom
import cv2
import numpy as np
import matplotlib.pyplot as plt


class ConvertClass(object):
    def __init__(self, ds):
        super(ConvertClass, self).__init__()

        self.pixel_array = ds.pixel_array
        if isinstance(ds.WindowCenter, pydicom.multival.MultiValue):
            self.wc = int(ds.WindowCenter[0])
            self.ww = int(ds.WindowWidth[0])
        else:
            self.wc = int(ds.WindowCenter)
            self.ww = int(ds.WindowWidth)

        self.ymax = 255
        self.ymin = 0

        self.slope = getattr(ds, 'RescaleSlope', 1)
        self.intercept = getattr(ds, 'RescaleIntercept', 0)
        self.PhotometricInterpretation = getattr(ds, 'PhotometricInterpretation', 'other')
        self.VOILUTFunction = getattr(ds, 'VOILUTFunction', 'LINEAR')

    def linear_exact(self):
        pixel_array = self.pixel_array * self.slope + self.intercept
        linear_exact_array = ((pixel_array - self.wc) / self.ww + 0.5) * (self.ymax - self.ymin) + self.ymin

        linear_exact_array[linear_exact_array < self.ymin] = self.ymin
        linear_exact_array[linear_exact_array > self.ymax] = self.ymax
        linear_exact_array = linear_exact_array.astype(np.uint8)

        if self.PhotometricInterpretation == 'MONOCHROME1':
            linear_exact_array = 255 - linear_exact_array
        return linear_exact_array

    def sigmoid(self):
        pixel_array = self.pixel_array * self.slope + self.intercept
        sigmoid_array = (self.ymax - self.ymin) / (1 + np.exp(-4 * (pixel_array - self.wc) / self.ww)) + self.ymin
        sigmoid_array = sigmoid_array.astype(np.uint8)

        if self.PhotometricInterpretation == 'MONOCHROME1':
            sigmoid_array = 255 - sigmoid_array
        return sigmoid_array

    def linear(self):
        pixel_array = self.pixel_array * self.slope + self.intercept
        linear_array = ((pixel_array - (self.wc - 0.5)) / (self.ww - 1) + 0.5) * (self.ymax - self.ymin) + self.ymin

        linear_array[linear_array < self.ymin] = self.ymin
        linear_array[linear_array > self.ymax] = self.ymax
        linear_array = linear_array.astype(np.uint8)

        if self.PhotometricInterpretation == 'MONOCHROME1':
            linear_array = 255 - linear_array

        return linear_array

    def noWW(self):
        min_value = np.min(self.pixel_array)
        max_value = np.max(self.pixel_array)
        pixel_array = (self.pixel_array - min_value) / (max_value - min_value) * 255
        pixel_array = pixel_array.astype(np.uint8)

        if self.PhotometricInterpretation == 'MONOCHROME1':
            pixel_array = 255 - pixel_array
        return pixel_array

    def convert(self):
        if self.VOILUTFunction == 'SIGMOID':
            return self.sigmoid()
        elif self.VOILUTFunction == 'LINEAR_EXACT':
            return self.linear_exact()
        else:
            return self.linear()


# try:
#     ds = pydicom.dcmread(r"1-01.dcm")
#     convert = ConvertClass(ds)
#     image_arr = convert.convert()
#
#     # 可视化图像
#     plt.imshow(image_arr, cmap='gray')
#     plt.axis('off')  # 不显示坐标轴
#     plt.show()
#
#     cv2.imwrite(r'1-01-image.png', image_arr)
#
# except Exception as e:
#     print(f"Error: {e}")
def convert_dcm_to_png(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.dcm'):
            dcm_path = os.path.join(input_folder, filename)
            try:
                ds = pydicom.dcmread(dcm_path)
                convert = ConvertClass(ds)
                image_arr = convert.convert()

                png_filename = os.path.splitext(filename)[0] + '.png'
                png_path = os.path.join(output_folder, png_filename)
                cv2.imwrite(png_path, image_arr)

                print(f"Converted {filename} to {png_filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")


# 设置输入和输出文件夹路径
input_folder = (r'G:\Hod\QIN-Multi-site-Lung-CTs-and-SEG-minus-Stanford\manifest-1545169187866\Lung Phantom\4482356\02-22-2015-1-NA-46623\1000.000000-QIN CT challengelesion1 alg01 run1 segmentation resul-31627')  # 替换为你的输入文件夹路径
output_folder = (r'G:\Hod\pngDataset')  # 替换为你的输出文件夹路径

convert_dcm_to_png(input_folder, output_folder)
