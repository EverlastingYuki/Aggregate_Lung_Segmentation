import os
import numpy as np


# {'2011_003271': array([0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,0., 0., 0.], dtype=float32)}
data = {
    '2011_003271': np.array([1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.], dtype=np.float32)
}

def get_filenames_without_extension(directory):
    # 存储不包含后缀的文件名
    filenames_without_extension = {}
    # 遍历目录中的所有文件
    for entry in os.listdir(directory):
        # 构建完整的文件路径
        full_path = os.path.join(directory, entry)
        # 确保是文件而不是目录
        if os.path.isfile(full_path):
            # 分离文件名和后缀名
            filename_without_extension = os.path.splitext(entry)[0]
            # 添加到列表中
            filenames_without_extension[filename_without_extension] = np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       1., 0., 0.], dtype=np.float32)
    return filenames_without_extension

# 指定需要获取文件名的目录
directory_path = r'I:\weclip\DataSet\VOCdevkit\VOC2012\JPEGImages'
filenames = get_filenames_without_extension(directory_path)
np.save('cls_labels_onehot.npy', filenames)