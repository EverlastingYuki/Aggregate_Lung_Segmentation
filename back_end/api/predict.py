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


@api.route("start", methods=["POST"])
def start():
    """
    开始预测接口，根据请求中的模型列表调用相应的预测函数，并返回预测结果的路径。

    ### args
    |  args          | required | request type | type |  remarks                  |
    |----------------|----------|--------------|------|---------------------------|
    | image_url      |  true    |    json      | str  | 图像文件路径  |
    | models         |  true    |    json      | list | 需要使用的模型列表  |

    ### request
    ```
json
    {"image_url": "", "models": ["U-net", "DeepLab", "WeClip"]}
    ```
    ### return
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
    image_path = data.get('image_url')
    models = data.get('models')
    clear_results()
    if 'U-net' in models:
        predict_Unet(PROJECT_ROOT, ONE_CHANNEL_DIR, THREE_CHANNEL_DIR, UNET_DIR)
    if 'DeepLab' in models:
        predict_deeplab(PROJECT_ROOT, ONE_CHANNEL_DIR, THREE_CHANNEL_DIR, DEEPLAB_DIR)
        # deeplab_postprocess()
    if 'WeClip' in models:
        predict_WeClip(PROJECT_ROOT, ONE_CHANNEL_DIR, THREE_CHANNEL_DIR, UNET_DIR)
    process_image()
    response_data = {}
    for i in os.listdir(OVERLAY_DIR):
        response_data[i] = [f'./static/result/overlay/{i}/{j}' for j in os.listdir(os.path.join(OVERLAY_DIR, i))]
    return jsonify(response_data)


@api.route('static/result/<model_name>/<path:filename>', methods=['GET'])
def send_image(model_name, filename):
    """
    发送图像，根据请求中的模型名称和文件名返回相应的图像文件。

    ### args
    |  args          | required | request type | type |  remarks                  |
    |----------------|----------|--------------|------|---------------------------|
    | model_name     |  true    |    path      | str  | 模型名称  |
    | filename       |  true    |    path      | str  | 文件名  |

    ### request
    - GET 请求，URL 中包含模型名称和文件名。

    ### return
    - 返回指定模型的预测结果图像文件。
    - 如果模型名称无效，返回错误信息和状态码 404。
    """
    if model_name == 'U-net':
        return send_from_directory(UNET_DIR, filename)
    elif model_name == 'DeepLab':
        return send_from_directory(DEEPLAB_DIR, filename)
    elif model_name == 'WeClip':
        return send_from_directory(WECLIP_DIR, filename)
    else:
        return "Invalid model name", 404


# @api.route('static/result/<model_name>/<path:filename>', methods=['GET'])
# def send_image(model_name, filename):
#     """
#     发送图像，根据请求中的模型名称和文件名返回相应的图像文件。
#
#     ### args
#     |  args          | required | request type | type |  remarks                  |
#     |----------------|----------|--------------|------|---------------------------|
#     | model_name     |  true    |    path      | str  | 模型名称  |
#     | filename       |  true    |    path      | str  | 文件名  |
#
#     ### request
#     - GET 请求，URL 中包含模型名称和文件名。
#
#     ### return
#     - 返回指定模型的预测结果图像文件。
#     - 如果模型名称无效，返回错误信息和状态码 404。
#     """
#     if model_name == 'U-net':
#         return send_from_directory(UNET_DIR, filename)
#     elif model_name == 'DeepLab':
#         return send_from_directory(DEEPLAB_DIR, filename)
#     elif model_name == 'WeClip':
#         return send_from_directory(WECLIP_DIR, filename)
#     else:
#         return "Invalid model name", 404


STATIC_DIR = os.path.abspath(os.path.join(os.getcwd(), 'front_end/static'))


# @api.route('/static/<path:filename>')
# def serve_static(filename):
#     print("发送图片: " + filename)
#
#     # 动态确定文件所在的目录
#     directory = os.path.join(STATIC_DIR, os.path.dirname(filename))
#
#     # 返回文件
#     print(directory)
#     print(os.path.basename(filename))
#     return send_from_directory(os.path.dirname(filename), os.path.basename(filename))


@api.route('/static/<path:filename>')
def static_file(filename):
    print("发送图片: " + filename)
    return send_from_directory(STATIC_DIR, filename)
