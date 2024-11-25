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

@api.route("/history", methods=["GET"])
def get_history():
    """
    获取 dataSource 数据

    ### 参数
    - 无

    ### 请求示例
    - GET 请求，无需传递任何参数。
    ```
bash
    curl -X GET http://localhost:5000/api/workspace
    ```
    ### 成功响应
    - HTTP 状态码 200
    - 响应体（JSON 格式）: 包含工作区数据的 JSON 数组

    ### 失败响应
    - HTTP 状态码 500
    - 响应体（JSON 格式）: 空数组
    """
    try:
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            data_source = json.load(f)
        return jsonify(data_source), 200
    except Exception as e:
        return jsonify([]), 500