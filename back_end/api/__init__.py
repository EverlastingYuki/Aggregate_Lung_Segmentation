import os
from flask import Blueprint
import yaml

api = Blueprint('api', __name__, url_prefix='/api')

# 读取配置文件
with open('back_end/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 从配置文件中读取路径
STATIC_DIR = config['static_dir']
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '../..')

UPLOADED_DIR = config['uploaded_dir']
ORIGINAL_DIR = config['original_dir']
ONE_CHANNEL_DIR = config['one_channel_dir']
THREE_CHANNEL_DIR = config['three_channel_dir']

RESULT_DIR = config['result_dir']
DEEPLAB_DIR = config['deeplab_dir']
UNET_DIR = config['Unet_dir']
WECLIP_DIR = config['WeClip_dir']
OVERLAY_DIR = config['overlay_dir']

WORKSPACE_PATH = config['workspace_path']

# 定义公开接口
__all__ = [
    'api',
    'STATIC_DIR',
    'PROJECT_ROOT',
    'UPLOADED_DIR',
    'ORIGINAL_DIR',
    'ONE_CHANNEL_DIR',
    'THREE_CHANNEL_DIR',
    'RESULT_DIR',
    'DEEPLAB_DIR',
    'UNET_DIR',
    'WECLIP_DIR',
    'OVERLAY_DIR',
    'WORKSPACE_PATH'
]

# 延迟导入 predict 和 workspace
from back_end.api import predict
from back_end.api import workspace
