import yaml

with open('back_end/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

STATIC_DIR = config['static_dir']

UPLOADED_DIR = config['uploaded_dir']
ORIGINAL_DIR = config['original_dir']
ONE_CHANNEL_DIR = config['one_channel_dir']
THREE_CHANNEL_DIR = config['three_channel_dir']

RESULT_DIR = config['result_dir']
DEEPLAB_DIR = config['deeplab_dir']
UNET_DIR = config['Unet_dir']
WECLIP_DIR = config['WeClip_dir']
