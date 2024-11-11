from PIL import Image

def process_image(image_path, rgb_tuple, alpha=128, save_path='output.png'):
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

# 示例调用
process_image(r'C:\Users\q\Downloads\Aggregate_Lung_Segmentation\static\result\WeClip\ID_0188_Z_0137.png', (255, 255, 0))  # 将黑色像素设置为透明，其他像素设置为红色
