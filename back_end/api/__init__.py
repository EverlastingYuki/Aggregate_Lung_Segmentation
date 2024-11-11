from flask import Blueprint
import yaml

api = Blueprint('api', __name__, url_prefix='/api')

# 读取配置文件
with open('back_end/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 从配置文件中读取路径
STATIC_DIR = config['static_dir']

UPLOADED_DIR = config['uploaded_dir']
ORIGINAL_DIR = config['original_dir']
ONE_CHANNEL_DIR = config['one_channel_dir']
THREE_CHANNEL_DIR = config['three_channel_dir']

RESULT_DIR = config['result_dir']
DEEPLAB_DIR = config['deeplab_dir']
UNET_DIR = config['Unet_dir']
WECLIP_DIR = config['WeClip_dir']


# import写在最后防止循环导入
from back_end.api import predict