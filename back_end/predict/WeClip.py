import os
import yaml
import subprocess
import shutil
from PIL import Image




def predict_WeClip(project_root, one_channel_dir, three_channel_dir, WeClip_dir):


    # TODO : 使用WeClip预测
    weclip_config_path = os.path.join(project_root, r'back_end\WeClip\configs\voc_attn_reg.yaml')
    with open(weclip_config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    config['dataset']['root_dir'] = os.path.join(project_root, r'back_end\WeClip\voc_data')
    config['dataset']['name_list_dir'] = os.path.join(project_root, r'back_end\WeClip\datasets\voc')
    config["clip_init"]["clip_pretrain_path"] = os.path.join(project_root, r'back_end/models/WeClip/ViT-B-16.pt')
    with open(weclip_config_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(config, file, default_flow_style=False)


    val_text_path =  os.path.join(project_root, r'back_end\WeClip\datasets\voc\val.txt')
    val_files_name_list = []
    for file_name in os.listdir(one_channel_dir):
        val_files_name_list.append(os.path.splitext(file_name)[0])
        source_file = os.path.join(one_channel_dir, file_name)
        target_file = os.path.join(project_root, r'back_end\WeClip\voc_data\JPEGImages', os.path.splitext(file_name)[0]+'.jpg')

        # 确保是文件而不是文件夹
        if os.path.isfile(source_file):
            with Image.open(source_file) as img:
                # 确保图像是RGB模式
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(target_file, 'JPEG')
            png_file = os.path.join(project_root, r"back_end\WeClip\voc_data\SegmentationClassAug",os.path.splitext(file_name)[0]+'.png')
            png_img = Image.new('RGB', (512, 512), (0, 0, 0))
            png_img.putpixel((0, 0), (1, 1, 1))
            png_img.save(png_file, 'PNG')


    with open(val_text_path, 'w', encoding='utf-8') as file:
        for file_name in val_files_name_list:
            file.write(file_name + '\n')

    inference_py_path = os.path.join(project_root, r'back_end\WeClip\inference.py')
    model_path = os.path.join(project_root, r'back_end/models/WeClip/test.pth')

    command = "C:/Users/q/.conda/envs/py38/python.exe " + inference_py_path + " --config " + weclip_config_path + " --model_path " + model_path
    print(command)

    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    # print(result.stdout)

    first_prediction_save_dir = os.path.join(project_root, r'back_end\WeClip\results\val\prediction_cmap')
    for file_name in os.listdir(first_prediction_save_dir):
        source_file = os.path.join(first_prediction_save_dir, file_name)
        target_file = os.path.join(WeClip_dir, file_name)

        if os.path.isfile(source_file):
            shutil.move(source_file, target_file)



    
if __name__ == '__main__':
    predict_WeClip(r"C:\Users\q\Downloads\Aggregate_Lung_Segmentation",2,r"C:\Users\q\Downloads\Aggregate_Lung_Segmentation\static\uploaded\three_channel",r"C:\Users\q\Downloads\Aggregate_Lung_Segmentation\static\result\WeClip")
    