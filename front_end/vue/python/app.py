from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageFilter, ImageOps
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = './results'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)

# 模型列表
MODEL_LIST = ['U-net', 'DeepLab', 'WeClip']

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify(MODEL_LIST), 200

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

@app.route('/inference', methods=['POST'])
def inference():
    data = request.json
    image_path = data.get('image_url')
    models = data.get('models')

    if not image_path or not models:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        # 打开服务器上存储的图片
        img = Image.open(image_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # 简单的推理：应用一些图像处理操作
    result_images = []
    for model in models:
        if model == 'U-net':
            result = img.filter(ImageFilter.GaussianBlur(5))
        elif model == 'DeepLab':
            result = ImageOps.grayscale(img)
        elif model == 'WeClip':
            result = img.convert('L').point(lambda x: 0 if x < 128 else 255, '1')  # 二值化

        result_path = os.path.join(RESULT_FOLDER, f'result_{model}.png')
        result.save(result_path)
        result_images.append(result_path)

    return jsonify({'result_images': result_images}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
