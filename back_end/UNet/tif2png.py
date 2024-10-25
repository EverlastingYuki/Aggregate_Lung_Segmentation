
import os


def rename(path):
    for i in os.listdir(path):
        if i.endswith('tif'):
            os.rename(path + '/' + i, path + '/' + i.replace('tif', 'png'))


if __name__ == '__main__':
    path = 'G:/Hod/UNet_lungCT_segmentation-master/test'
    rename(path)