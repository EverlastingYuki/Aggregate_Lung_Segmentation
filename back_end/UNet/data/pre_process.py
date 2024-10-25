import cv2 as cv
import numpy as np
import os

class Parameters():
    def __init__(self):
        # 输入label图片文件夹
        self.input_dir = r"G:/Hod/UNet_lungCT_segmentation-master/dataset/2d_masks/"
        # 输出label图片文件夹
        self.output_dir = r"G:/Hod/UNet_lungCT_segmentation-master/dataset/converted_label/"

para = Parameters()

def main():
    n=0
    op_dir = para.output_dir
    for each_image in os.listdir(para.input_dir):
        label_img = []
        image_fullpath = para.input_dir +  each_image
        image = cv.imread(image_fullpath,0)
        img_array = np.asarray(image)
        for i in img_array:
            for j in i:
                if j == 255:
                   label_img.append(1)
                else:
                   label_img.append(0)
        output_img = op_dir + each_image
        label_img = (image == 255).astype(np.uint8)
        label_img = np.array(label_img)
        label_img = label_img.reshape((512, 512))
        cv.imwrite(output_img, label_img)
        n = n + 1
        print("处理完成label: %d" % n)

if __name__ == '__main__':
    main()
