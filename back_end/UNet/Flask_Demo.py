import os
import shutil
import json

import cv2
import numpy as np
import matplotlib.pyplot as plt
# import tensorflow as tf

from predict import predict as predict_Unet
from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from PIL import Image

app = Flask(__name__)


def walk_dir(dir):
    dir_list = []
    for image in os.listdir(dir):
        dir_list.append(os.path.join(dir, image))
    return dir_list


original_dir = r'G:\Hod\UNet_lungCT_segmentation-master\static\Unet_uploaded'
save_dir = r'G:\Hod\UNet_lungCT_segmentation-master\static\Unet_txt'


@app.route("/", methods=['GET', 'POST'])
def index():
    return redirect("/Unet_Predict")


@app.route("/Unet_Predict", methods=['GET', 'POST'])
def unet():
    return render_template("Unet_Demo.html")


@app.route("/Unet_upload", methods=["POST"])
def upload():
    for file in request.files.getlist('file'):
        print(file.filename)
        save_location = os.path.join(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_uploaded\test", file.filename)
        file.save(save_location)
        image = Image.open(save_location)
        if len(image.split()) == 1:
            print(file.filename+"为单通道图片，保存三通道副本到RGB_img")
            # img = np.array(image)
            # img = img.reshape(180, 1110, 1)
            # img_tensor = tf.convert_to_tensor(img)
            # img_tensor = tf.image.grayscale_to_rgb(img_tensor)
            # sess = tf.Session()
            # img = sess.run(img_tensor)
            # print(img_tensor.shape)
            img_gray = cv2.imread(save_location, cv2.IMREAD_GRAYSCALE)
            img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
            cv2.imwrite(os.path.join(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_RGB_img", file.filename), img_rgb)
    return "0"


@app.route("/Unet_clear", methods=["GET"])
def clear():
    try:
        shutil.rmtree(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_uploaded\test")
        shutil.rmtree(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_predict_result\predict_unet")
        shutil.rmtree(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_RGB_img")
    except:
        pass
    os.mkdir(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_uploaded\test")
    os.mkdir(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_RGB_img")
    return "0"


@app.route("/Unet_start", methods=["GET"])
def Unet_start():
    try:
        shutil.rmtree(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_predict_result\predict_unet")
        os.remove(r"G:\Hod\UNet_lungCT_segmentation-master\static\Unet_txt\test.txt")
    except:
        pass
    img_test = walk_dir(os.path.join(original_dir, 'test'))
    with open(os.path.join(save_dir, 'test.txt'), 'w') as f:
        for index in range(len(img_test)):
            f.write(img_test[index] + '\t' + 'null' + '\n')

    with open(r'G:\Hod\UNet_lungCT_segmentation-master\flask_predict_config_Unet.json', encoding='utf-8') as f:
        config = json.load(f)
    predict_Unet(config)
    image_folder = r'G:\Hod\UNet_lungCT_segmentation-master\static\Unet_predict_result\predict_unet\vis'
    images = os.listdir(image_folder)
    image_urls = [f'/static/Unet_predict_result/predict_unet/vis/{image}' for image in images]
    # image_urls = [r'/static/Unet_predict_result/predict_unet/vis/Hoshimachi   .png',r'/Unet_predict_result/predict_unet/vis/test1.png']

    return jsonify(image_urls)
    # return "0"


@app.route('/static/Unet_predict_result/predict_unet/vis/<path:filename>', methods=['GET'])
def send_Unet_image(filename):
    return send_from_directory(r'G:\Hod\UNet_lungCT_segmentation-master\static\Unet_predict_result\predict_unet\vis',
                               filename)

@app.route('/show_result/<module_name>', methods=['GET'])
def send_image(module_name):
    if module_name == 'Unet':
        image_urls={}
        for key in os.listdir(r'G:\Hod\UNet_lungCT_segmentation-master\static\Unet_RGB_img'):
            image_urls['/Unet_RGB_img/'+key] = r'/Unet_predict_result/predict_unet/vis/'+key
        return render_template("predict_result.html", image_urls=image_urls)



app.run()
