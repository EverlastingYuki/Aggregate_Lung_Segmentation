import os
import shutil
import json
import yaml

import cv2
import numpy as np
import matplotlib.pyplot as plt
# import tensorflow as tf

from back_end.predict.Unet import predict_Unet
from back_end.predict.deeplab import predict_deeplab
from back_end.predict.WeClip import predict_WeClip
from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
from back_end.api import *
import yaml

from back_end.util.clear_results import clear_results
from back_end.util.post_process import post_process_image, process_image, deeplab_postprocess

STATIC_DIR = os.path.abspath(os.path.join(os.getcwd(), 'front_end/static'))


@api.route("start", methods=["POST"])
def start():
    """
    开始预测接口，根据请求中的模型列表调用相应的预测函数，并返回预测结果的路径。

    ### 参数
    | 参数名       | 必填 | 请求类型 | 类型   | 说明                           |
    |--------------|------|----------|--------|--------------------------------|
    | image_url    | 是   | json     | list   | 图像文件路径                   |
    | models       | 是   | json     | list   | 需要使用的模型列表             |

    ### 请求示例
    ```
json
    {
        "image_url": [
            "http://localhost:5000/api/static/uploaded/three_channel/ID_0188_Z_0137.png",
            "http://localhost:5000/api/static/uploaded/three_channel/ID_0189_Z_0132.png",
            "http://localhost:5000/api/static/uploaded/three_channel/ID_0190_Z_0070.png",
            "http://localhost:5000/api/static/uploaded/three_channel/ID_0191_Z_0140.png"
        ],
        "models": [
            "U-net",
            "DeepLab",
            "WeClip"
        ]
    }
    ```
    ### 返回示例
    ```
json
    {
        "Unet": [
            "./static/result/Unet/ID_0188_Z_0137.png"
        ],
        "Unet_WeClip": [],
        "WeClip": [],
        "deeplab": [
            "./static/result/deeplab/ID_0188_Z_0137.png"
        ],
        "deeplab_Unet": [
            "./static/result/deeplab_Unet/ID_0188_Z_0137.png"
        ],
        "deeplab_Unet_WeClip": [],
        "deeplab_WeClip": [],
        "original": [
            "./static/result/original/ID_0188_Z_0137.png"
        ]
    }
    ```
    - 返回一个 JSON 对象，包含原始图像路径和每个模型的预测结果路径。

    """
    data = request.json
    image_urls = data.get('image_url')
    models = data.get('models')

    clear_results()
    temp_dir = os.path.join(STATIC_DIR, 'temp')
    shutil.rmtree(temp_dir)

    one_channel_temp_dir = os.path.join(temp_dir, 'one_channel')
    three_channel_temp_dir = os.path.join(temp_dir, 'three_channel')

    os.makedirs(one_channel_temp_dir, exist_ok=True)
    os.makedirs(three_channel_temp_dir, exist_ok=True)

    # 复制图片到临时文件夹
    for url in image_urls:
        image_path = url.split('/')[-1]
        print('Copying image:', image_path)
        original_one_channel = os.path.join(ONE_CHANNEL_DIR, image_path)
        original_three_channel = os.path.join(THREE_CHANNEL_DIR, image_path)
        shutil.copy(original_one_channel, one_channel_temp_dir)
        shutil.copy(original_three_channel, three_channel_temp_dir)

    # 调用预测函数
    if 'U-net' in models:
        predict_Unet(PROJECT_ROOT, one_channel_temp_dir, three_channel_temp_dir, UNET_DIR)
    if 'DeepLab' in models:
        predict_deeplab(PROJECT_ROOT, one_channel_temp_dir, three_channel_temp_dir, DEEPLAB_DIR)
        # deeplab_postprocess()
    if 'WeClip' in models:
        predict_WeClip(PROJECT_ROOT, one_channel_temp_dir, three_channel_temp_dir, UNET_DIR)
    process_image(three_channel_temp_dir)
    shutil.rmtree(temp_dir)

    response_data = {}
    for i in os.listdir(OVERLAY_DIR):
        response_data[i] = [f'http://localhost:5000/api/static/result/overlay/{i}/{j}' for j in
                            os.listdir(os.path.join(OVERLAY_DIR, i))]

    return jsonify(response_data)


@api.route('/static/<path:filename>')
def static_file(filename):
    """
    发送静态文件接口，根据请求中的文件名返回相应的静态文件。

    ### 参数
    | 参数名       | 必填 | 请求类型 | 类型   | 说明                           |
    |--------------|------|----------|--------|--------------------------------|
    | filename     | 是   | path     | str    | 文件名                         |

    ### 请求示例
    - GET 请求，URL 中包含文件名。
    - 例如：`http://localhost:5000/api/static/three_channel/ID_0188_Z_0137.png`

    ### 返回
    - 返回指定的静态文件。
    - 如果文件不存在，返回 404 错误。
    """
    print("发送图片: " + filename)
    return send_from_directory(STATIC_DIR, filename)
