import os
import shutil
import json

import cv2
import numpy as np
import matplotlib.pyplot as plt
# import tensorflow as tf

from back_end.predict.Unet import predict_Unet
# from back_end.predict.WeClip import predict_WeClip
from back_end.predict.deeplab import predict_deeplab
# from back_end.predict.WeClip import predict_WeClip
from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
from back_end.api import api
import yaml

from back_end.util.postProcess import post_process_image

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
PROJECT_ROOT = os.path.join(PROJECT_ROOT, 'front_end')
# static目录
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')

# 上传目录
UPLOADED_DIR = os.path.join(STATIC_DIR, 'uploaded')
ORIGINAL_DIR = os.path.join(UPLOADED_DIR, 'original')
ONE_CHANNEL_DIR = os.path.join(UPLOADED_DIR, 'one_channel')
THREE_CHANNEL_DIR = os.path.join(UPLOADED_DIR, 'three_channel')

# 预测结果目录
RESULT_DIR = os.path.join(STATIC_DIR, 'result')
DEEPLAB_DIR = os.path.join(RESULT_DIR, 'deeplab')
UNET_DIR = os.path.join(RESULT_DIR, 'Unet')
WECLIP_DIR = os.path.join(RESULT_DIR, 'WeClip')


# # 定义预测结果目录
# UNET_PREDICT_DIR = os.path.join(STATIC_DIR, 'Unet_predict_result', 'predict_unet', 'vis')
# UNET_RGB_DIR = os.path.join(STATIC_DIR, 'Unet_RGB_img')


@api.route("upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    # for file in request.files.getlist('file'):
    file = request.files['file']
    print(file.filename)
    original_img_path = os.path.join(ORIGINAL_DIR, file.filename)
    one_channel_path = os.path.join(ONE_CHANNEL_DIR, file.filename)
    three_channel_path = os.path.join(THREE_CHANNEL_DIR, file.filename)
    file.save(original_img_path)
    print(5656)
    image = Image.open(original_img_path)
    if len(image.split()) == 1:
        print(file.filename + "为单通道图片，保存三通道副本到three_channel")
        shutil.copy2(original_img_path, one_channel_path)

        img_gray = cv2.imread(original_img_path, cv2.IMREAD_GRAYSCALE)
        img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
        cv2.imwrite(three_channel_path, img_rgb)
    else:
        print(file.filename + "为三通道图片，保存单通道副本到one_channel")
        shutil.copy2(original_img_path, three_channel_path)
        img = cv2.imread(original_img_path, cv2.IMREAD_GRAYSCALE)  # 读取灰度图
        cv2.imwrite(one_channel_path, img)
    return jsonify({'message': 'File uploaded successfully'}), 200


@api.route("clear", methods=["GET"])
def clear():
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
    data = request.json
    image_path = data.get('image_url')
    models = data.get('models')
    if 'deeplab' in models:
        predict_deeplab(PROJECT_ROOT, ONE_CHANNEL_DIR, THREE_CHANNEL_DIR, DEEPLAB_DIR)
        print("deeplab predict finish")
    if 'Unet' in models:
        predict_Unet(PROJECT_ROOT, ONE_CHANNEL_DIR, THREE_CHANNEL_DIR, UNET_DIR)
        print("Unet predict finish")
    # if 'WeClip' in models:
    #     predict_WeClip(PROJECT_ROOT, ONE_CHANNEL_DIR, THREE_CHANNEL_DIR, WECLIP_DIR)
    #     print("WeClip predict finish")
    for i in [DEEPLAB_DIR, UNET_DIR, WECLIP_DIR]:
        for image in os.listdir(i):
            path = os.path.join(i, image)
            post_process_image(input_path=path, output_path=path)
    unet_images = os.listdir(UNET_DIR)
    deeplab_images = os.listdir(DEEPLAB_DIR)
    # weclip_images = os.listdir(WECLIP_DIR)

    unet_image_urls = [f'./static/result/Unet/{image}' for image in unet_images]
    deeplab_image_urls = [f'./static/result/deeplab/{image}' for image in deeplab_images]
    # weclip_image_urls = [f'./static/result/WeClip/{image}' for image in weclip_images]

    response_data = {
        "Unet": unet_image_urls,
        "deeplab": deeplab_image_urls,
        # "WeClip": weclip_image_urls
    }

    return jsonify(response_data)


@api.route('static/result/<model_name>/<path:filename>', methods=['GET'])
def send_image(model_name, filename):
    if model_name == 'U-net':
        return send_from_directory(UNET_DIR, filename)
    elif model_name == 'DeepLab':
        return send_from_directory(DEEPLAB_DIR, filename)
    elif model_name == 'WeClip':
        return send_from_directory(WECLIP_DIR, filename)
    else:
        return "Invalid model name", 404
