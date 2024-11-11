import numpy as np
import matplotlib.pyplot as plt


# 从 .npy 文件加载数据
data = np.load(r"I:\weclip\WeCLIP\results\val\logit\ID_0264_Z_0080.npy", allow_pickle=True).item()  # 确保数据是以字典形式存储的

# 提取 'segs' 和 'msc_segs' 数据
segs = data['segs']
msc_segs = data['msc_segs']

# 定义一个函数来可视化给定数据的特定通道
def visualize_slices(data, title, channel_idx, slice_idx, cmap='viridis'):
    """
    Visualize a specific channel and slice of 4D data (shape: [N, C, H, W]).
    
    Args:
        data (numpy array): 4D data array to visualize.
        title (str): Title of the plot.
        channel_idx (int): Index of the channel to visualize.
        slice_idx (int): Index of the slice along the first dimension.
        cmap (str): Color map to use for the plot (default: 'viridis').
    """
    plt.figure(figsize=(8, 6))
    plt.imshow(data[slice_idx, channel_idx, :, :], cmap=cmap)
    plt.colorbar()
    plt.title(f'{title} - Channel {channel_idx}, Slice {slice_idx}')
    plt.show()

# 可视化 segs 中的第 0 通道，第 0 个 slice
visualize_slices(segs, 'Segs', channel_idx=0, slice_idx=0)

# 可视化 msc_segs 中的第 0 通道，第 0 个 slice
visualize_slices(msc_segs, 'MSC Segs', channel_idx=0, slice_idx=0)

# 可视化 segs 中的第 1 通道，第 0 个 slice
visualize_slices(segs, 'Segs', channel_idx=1, slice_idx=0)

# 可视化 msc_segs 中的第 1 通道，第 0 个 slice
visualize_slices(msc_segs, 'MSC Segs', channel_idx=1, slice_idx=0)
