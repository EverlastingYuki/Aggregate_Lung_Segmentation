from PIL import Image


class ProcessImg:

    @classmethod
    def get_colorful_mask(cls, image_path, rgb_tuple, save_path, alpha=128):
        """

        :param image_path: 输入的图片路径
        :param rgb_tuple: 图像的rgb值组成的元组
        :param save_path: 保存的路径（完整路径）
        :param alpha: 彩色遮罩的半透明度（0-255）默认128（半透明）
        :return: 无
        """
        img = Image.open(image_path).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                new_data.append((0, 0, 0, 0))  # 透明
            else:
                new_data.append((*rgb_tuple, alpha))  # 不透明

        img.putdata(new_data)

        img.save(save_path)


if __name__ == '__main__':
    # 示例调用
    ProcessImg.get_colorful_mask(r'C:\Users\q\Downloads\Aggregate_Lung_Segmentation\static\result\WeClip\ID_0188_Z_0137.png',
                  (255, 255, 0), r"./output.png")  # 将黑色像素设置为透明，其他像素设置为红色
