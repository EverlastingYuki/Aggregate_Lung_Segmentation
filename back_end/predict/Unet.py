
import os
import shutil
import sys

import cv2
import json
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from back_end.UNet.models import unet

Img_channel = 1
Height = 512
Width = 512


def walk_dir(dir):
    dir_list = []
    for image in os.listdir(dir):
        dir_list.append(os.path.join(dir, image))
    return dir_list


def predict_Unet(project_root, one_channel_dir, three_channel_dir, Unet_dir):
    print('Unet_dir：' + Unet_dir)

    try:
        shutil.rmtree(Unet_dir)
        os.remove(os.path.join(project_root, "back_end", "UNet", "txt", "test.txt"))
    except:
        pass
    os.makedirs(Unet_dir, exist_ok=True)
    img_test = walk_dir(one_channel_dir)
    with open(os.path.join(project_root, "back_end", "UNet", "txt", "test.txt"), 'w') as f:
        for index in range(len(img_test)):
            f.write(img_test[index] + '\t' + 'null' + '\n')

    with open(os.path.join(project_root, "back_end", "UNet", "flask_predict_config_Unet.json"),
              encoding='utf-8') as f:
        config = json.load(f)
    predict(config, Unet_dir)


def predict(config, Unet_dir):
    print('Unet_dir：' + Unet_dir)

    device = torch.device('cpu')
    model = unet.UNet(num_classes=config['num_classes'])

    check_point = os.path.join(config['save_model']['save_path'], 'unet_demo.pth')
    transform = transforms.Compose(
        [
            transforms.ToPILImage(),
            transforms.ToTensor()
            # transforms.Normalize(mean=[0.485, 0.456, 0.406],
            #                      std=[0.229, 0.224, 0.225])
        ]
    )
    model.load_state_dict(torch.load(check_point, map_location='cpu'), False)
    model.cpu()
    model.eval()

    with open(config['img_txt'], 'r', encoding='utf-8') as f:
        for line in f.readlines():
            print('正在处理' + line)
            image_name, _ = line.strip().split('\t')
            im = np.asarray(Image.open(image_name))
            im = im.reshape((Height, Width, Img_channel))
            im = transform(im).float().cpu()
            im = im.reshape((1, Img_channel, Height, Width))

            output = model(im)
            _, pred = output.max(1)
            pred = pred.view(Height, Width)
            mask_im = pred.cpu().numpy().astype(np.uint8)
            file_name = os.path.basename(image_name)  # 只提取文件名
            save_visual = os.path.join(Unet_dir, file_name)
            print('save_visual：' + save_visual)
            translabeltovisual(mask_im, save_visual)


def translabeltovisual(mask_im, path):
    # 将白色部分（值为 255）改为绿色（值为 [0, 255, 0]）
    visual_img = np.zeros((Height, Width, 3), dtype=np.uint8)
    visual_img[mask_im == 1] = [0, 255, 0]  # 绿色
    visual_img[mask_im == 0] = [0, 0, 0]  # 黑色

    cv2.imwrite(path, visual_img)
    print('保存路径：' + path)


# def translabeltovisual(mask_im, path):
#     visual_img = np.where(mask_im == 1, 255, 0).astype(np.uint8)
#     visual_img = visual_img.reshape((Height, Width))
#     visual_img = cv2.cvtColor(visual_img, cv2.COLOR_GRAY2RGB)
#     cv2.imwrite(path, visual_img)
#     print('保存路径：'+path)

#
# if __name__ == "__main__":
#     project_root = r'G:\Hod\Aggregate_Lung_Segmentation'
#     one_channel_dir = r'G:\Hod\Aggregate_Lung_Segmentation\static\uploaded\one_channel'
#     three_channel_dir = r'G:\Hod\Aggregate_Lung_Segmentation\static\uploaded\three_channel'
#     Unet_dir = r'G:\Hod\Aggregate_Lung_Segmentation\static\result\Unet'
#
#     predict_Unet(project_root, one_channel_dir, three_channel_dir, Unet_dir)