import os
from ..deeplabv3.deeplab import DeeplabV3
from PIL import Image
from pathlib import Path

def predict_deeplab(project_root, one_channel_dir, three_channel_dir, deeplab_dir):
    deeplab = DeeplabV3()
    count = False
    name_classes = ["background", "lung"]
    try:
        for filename in os.listdir(one_channel_dir):
            # 构建文件的完整路径
            file_path = os.path.join(one_channel_dir, filename)

            # 检查是否为文件
            if os.path.isfile(file_path):
                img = file_path
                try:
                    image = Image.open(img)
                except:
                    print('Open Error! Try again!')
                else:
                    r_image = deeplab.detect_image(image, count=count, name_classes=name_classes)
                    # r_image.show()
                    r_image.save(os.path.join(deeplab_dir, filename))
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == "__main__":
    project_root = r'G:\Hod\UNet_lungCT_segmentation-master'
    one_channel_dir = r'G:\Hod\UNet_lungCT_segmentation-master\static\uploaded\one_channel'
    three_channel_dir = r'G:\Hod\UNet_lungCT_segmentation-master\static\uploaded\three_channel'
    deeplab_dir = r'G:\Hod\UNet_lungCT_segmentation-master\static\result\deeplab'

    predict_deeplab(project_root, one_channel_dir, three_channel_dir, deeplab_dir)
