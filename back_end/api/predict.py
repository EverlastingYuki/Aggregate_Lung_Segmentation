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


# # 定义预测结果目录
# UNET_PREDICT_DIR = os.path.join(STATIC_DIR, 'Unet_predict_result', 'predict_unet', 'vis')
# UNET_RGB_DIR = os.path.join(STATIC_DIR, 'Unet_RGB_img')


@api.route("upload", methods=["POST"])
def upload():
    """
    上传文件接口，用于接收前端上传的图像文件，并根据图像的通道数保存为不同的路径。

    ### args
    |  args          | required | request type | type |  remarks                  |
    |----------------|----------|--------------|------|---------------------------|
    | file           |  true    |    form-data | file | 需要上传的图像文件  |

    ### request
    - 表单数据，包含一个名为 `file` 的字段，用于上传图像文件。

    ### return
    ```
json
    {
        "message": "File uploaded successfully"
    }
    ```
    - 成功上传文件后返回的消息。
    - 如果请求中没有文件部分，则返回错误信息和状态码 400。
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    original_img_path = os.path.join(ORIGINAL_DIR, file.filename)
    one_channel_path = os.path.join(ONE_CHANNEL_DIR, file.filename)
    three_channel_path = os.path.join(THREE_CHANNEL_DIR, file.filename)
    file.save(original_img_path)
    image = Image.open(original_img_path)
    if len(image.split()) == 1:
        shutil.copy2(original_img_path, one_channel_path)
        img_gray = cv2.imread(original_img_path, cv2.IMREAD_GRAYSCALE)
        img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
        cv2.imwrite(three_channel_path, img_rgb)
    else:
        shutil.copy2(original_img_path, three_channel_path)
        img = cv2.imread(original_img_path, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(one_channel_path, img)
    return jsonify({'message': 'File uploaded successfully'}), 200


@api.route("clear", methods=["GET"])
def clear():
    """
    清理所有预测结果目录，重新创建这些目录。

    ### args
    - 无

    ### request
    - GET 请求，无需传递任何参数。

    ### return
    - 成功清理目录后返回字符串 `"0"`。
    - 如果在清理过程中发生错误，会捕获异常并继续执行后续操作。
    """
    try:
        shutil.rmtree(DEEPLAB_DIR)
        shutil.rmtree(UNET_DIR)
        shutil.rmtree(WECLIP_DIR)
        shutil.rmtree(ONE_CHANNEL_DIR)
        shutil.rmtree(THREE_CHANNEL_DIR)
        shutil.rmtree(ORIGINAL_DIR)
    except:
        pass
    os.makedirs(DEEPLAB_DIR, exist_ok=True)
    os.makedirs(UNET_DIR, exist_ok=True)
    os.makedirs(WECLIP_DIR, exist_ok=True)
    os.makedirs(ONE_CHANNEL_DIR, exist_ok=True)
    os.makedirs(THREE_CHANNEL_DIR, exist_ok=True)
    os.makedirs(ORIGINAL_DIR, exist_ok=True)
    return "0"


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
    original_image_urls = [f'./static/result/uploaded/{image}' for image in os.listdir(THREE_CHANNEL_DIR)]
    response_data = {
        "original": original_image_urls
    }
    for i in os.listdir(OVERLAY_DIR):
        response_data[i] = [f'./static/result/{i}/{j}' for j in os.listdir(os.path.join(OVERLAY_DIR, i))]
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
