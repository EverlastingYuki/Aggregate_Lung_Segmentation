import numpy as np

# 检查 .npy 文件内容
def inspect_npy(file_path):
    data = np.load(file_path, allow_pickle=True)
    # 打印 .npy 文件中的内容
    with open("npy_file0.txt", 'w', encoding='utf-8') as f:
        f.write(str(data))
    # print("npy file content:", data)
    # 如果是字典，显示它的键
    if isinstance(data, dict):
        print("Keys in the npy file:", data.keys())
    return data

# 加载并检查 .npy 文件
npy_file_path = r"I:\weclip\WeCLIP\datasets\voc\cls_labels_onehot.npy"
# npy_file_path = r"I:\weclip\WeCLIP\datasets\voc\data00.npy"
data = inspect_npy(npy_file_path)
