import torch
import numpy as np

def eval_metrics(output, target, num_classes):
    # 对于每一条数据，选取预测概率最大的作为预测结果，即预测最大值的标签
    _, predict = output.max(1)

    # 0-1转化为1-2，为了后续计算不遗漏0
    predict = predict.long() + 1
    target = target.long() + 1

    # 统计图像中大于0的部分，target>0相当于图片大小
    pixel_labeled = (target > 0).sum()
    pixel_correct = ((predict == target)*(target > 0)).sum()

    # 预测部分
    predict = predict * (target > 0).long()
    intersection = predict * (predict == target).long()

    # torch.histc计算张量直方图，即每个类别的面积总和
    '''
    input (Tensor) -输入张量。  
    Bins (int) -直方图Bins的数量  
    Min (int) -范围的下端(包括在内)  
    Max (int) -范围的上端(包括在内)  
    '''
    area_inter = torch.histc(intersection.float(), num_classes, 1, num_classes)
    area_pred = torch.histc(predict.float(), num_classes, 1, num_classes)
    area_lab = torch.histc(target.float(), num_classes, 1, num_classes)
    area_union = area_pred + area_lab - area_inter

    # np.round:四舍五入
    correct = np.round(pixel_correct.cpu().numpy(), 5)
    labeld = np.round(pixel_labeled.cpu().numpy(), 5)
    inter = np.round(area_inter.cpu().numpy(), 5)
    union = np.round(area_union.cpu().numpy(), 5)

    #pixacc = 1.0 * correct / (np.spacing(1) + labeld)
    #mIoU = (1.0 * inter / (np.spacing(1) + union)).mean()
    return correct, labeld, inter, union